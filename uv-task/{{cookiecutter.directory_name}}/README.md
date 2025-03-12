# {{ cookiecutter.project_name }}!

## Task organization

This is a template for running python tasks using [python-task-queue](https://github.com/seung-lab/python-task-queue).
Task-queue is built around splitting up `tasks` that queue up a list of parameters defining work to be done and `workers` that listen to this queue and execute the tasks.
The workers can be run on a local machine, in a docker image, or in a cloud service like Google Cloud Platform.
This package is designed in particular to work with GCP, and has templates and scripts to help you Dockerize your worker and deploy it to a GKE cluster.

Please set any blank environment variables in the `config/task.env` file.

## Using this template 

The organization of this project is structured in a particular way to work with `python-task-queue` with minimal fuss using [`uv`](https://docs.astral.sh/uv/) and [`poe`](https://poethepoet.natn.io/index.html).

The main components are:

### 1. Tasks and queues

#### Defining the task function

`src/{{ cookiecutter.project_slug }}/task.py` is where your task is defined.
The `run_task` function defined here is a simple pass-through that implements the principle mechanism for building up the task queue and otherwise passes all arguments and keywords to the `_run_task` function.
The `_run_task` function is where the actual work of your individual task and its arguments should be defined.
By splitting up the task definition in this way, the details of task-queue can be ignored and `_run_task` can be written as a regular python function, plus the default scripts to populate the queue and run the workers can be used without modification.

#### Defining the queue

The config that define how to populate and run the queue should be set in an environment file, by default `config/task.env`.
By default, four values are needed to define a queue and task.

First, decide on what kind of queue you are using by reading the documentation for [python-task-queue](https://github.com/seung-lab/python-task-queue).
Once you decided on your queue, set the `TASKQUEUE_PATH` environment variable in `config/task.env` to the path that defines it (e.g. an https URL for an SQS queue or an fq:// path for a filequeue).

When workers run, they will look at this queue to find tasks.
A task will timeout if it takes longer than the `TQ_LEASE_SECONDS` environment variable.

To generate the queue, you should build a pandas dataframe where each row is one task, and column names match to function keywords that will be passed to `_run_task`.
Save this dataframe as a feather file and set the `TASK_PARAMETER_FILENAME` environment variable to the path of this file without the `.feather` extension.

The current template assumes you will use [CloudFiles](https://github.com/seung-lab/cloud-files) to store the processed data from the task queue, and the `CF_CLOUDPATH` environment variable should be set to the path of the CloudFiles directory or cloud bucket where the processed data will be stored.
The script `insert_tasks.py` uses this path, together with the `TASK_PARAMETER_FILENAME`, to add the cloudpath to each row, but assumes that `cloudpath` is an argument of your `_run_task` function.
Modify this as needed.

```python
task_df = pd.read_feather(
    f"{os.environ.get('TASK_PARAMETER_FILENAME', 'tasks')}.feather"
)
target_cloudpath = os.environ.get("CF_CLOUDPATH")

if "cloudpath" not in task_df.columns:
    task_df["cloudpath"] = target_cloudpath
```

#### Inserting Tasks

To insert tasks into the queue, run the `insert_tasks.py` script with the above environment variables set.

The easiest way to do this is to use `poe` to run the `insert_tasks` script in `uv` with an environment file.
Assuming you have already have an established python environment created with `uv sync` or anything else that generates a `uv.lock` file, you can insert tasks via:`poe insert_tasks`.
If you need to specify an environment file other than `config/task.env`, you can do so with `poe insert_tasks -e my_env_file.env`.
Note that this command will expect `config/task.env` (or your file) to exist relative to the root of the project directory.
If you don't want that for some reason, run via `uv run --frozen insert_tasks.py`.
Note that the `--frozen` flag is important to make sure that the tasks and the workers are running the same code.

##### Skipping finished tasks

Sometimes tasks will fail, and most likely your `_run_task` function will handle it via `try/except` blocks instead of raising an Exception that will kill a worker.
Because of this, after an initial run-through, you will often want to start from the same initial state and only add tasks that have not been completed previously.
To help set up a pattern to do this, there is a `filter_tasks` function in `tasks.py` that takes as an argument the task dataframe and a cloudpath and is intended to return a filtered dataframe that only includes tasks that have not been completed.

For example, if the presence of a file with a name `{root_id}.h5` in the cloudpath is a signal that the task has been completed, you could use the following code:

```python
def filter_tasks(task_df, cloudpath):
    cf = CloudFiles(cloudpath)
    curr_files = list(cf.list())
    done_ids = np.array([int(f.split(".")[0]) for f in curr_files if f.endswith(".h5")])
    return task_df[~task_df["root_id"].isin(done_ids)]
```

The `filter_tasks` function is automatically used in `insert_tasks.py`, but by default it is set to return the original dataframe unchanged.

### 2. Workers

Now that you have a queue, you need workers to process the tasks.
Once you have defined the tasks, the same environment files are used to define the workers and no additional configuration is needed.

To run a worker locally (for example, for testing), you can use the `run.py` script with the same environment file sourced.
As before, an easy approach is `poe launch_worker` (optionally `poe launch_worker -e my_env_file.env`, if using a file other than `config/task.env`).
Similar to above, this command will expect `config/task.env` (or your file) to exist in the root of the project directory, and otherwise you should run via `uv run --frozen run.py`.

#### Dockerizing workers

The Dockerfile is already set up to build and run a worker Docker without extra configuration.
Note that the current file is based on the `latest` tag for `uv` and the selected python version, and you should feel free to update or change those to other specific versions if desired.
To build the Docker image, run `docker buildx build --platform linux/amd64 -t YOUR_TAG .` in the root of the project directory.
If you are going to use this image for a GKE cluster, your tag should be of the form `username/projectname:tag` (with your dockerhub username) and then pushed to dockerhub via `docker push username/projectname:tag`.

To test the Docker image locally,

```bash
docker run \                           
    --platform linux/amd64 \
    --env-file config/task.env \
    -v /Users/YOUR_USERNAME/.cloudvolume/secrets:/root/.cloudvolume/secrets \
    YOUR_TAG 
```

will run the worker in the Docker image with the same environment variables as the queue as well as using your CAVE secrets and cloud credentials set up for CloudFiles.

Note: The `platform` flags here are useful if you are building on a Mac, but you can remove them if you are building on a Linux machine more similar to the cloud environment.

### 3. Deploying workers to Google Cloud

Now you want to spin up a bunch of workers on a Google Kubernetes Engine cluster to churn through tasks.
Note that you will need to install `gcloud` [command line tools](https://cloud.google.com/sdk/docs/install) before starting.
This template helps you define a cluster and deploy workers to it with minimal configuration using both `config/task.env` and `config/cluster.env`.

#### Configuring the cluster and template files

There are two scripts that you will need to run, the first to create the cluster (the compute resources) and the second to define the tasks that will run on it.
Once both `task.env` and `cluster.env` have been defined, you will need to apply these configuration files to the templates in the `templates` directory.
You can do this with `poe make_scripts`, which uses the default `config/task.env` and `config/cluster.env` files, or `poe make_scripts -e my_task.env -c my_cluster.env` if you are using different environment files.
These will create `kube-task.yaml` and `make_cluster.sh` files in the `scripts` directory.
Next, you can run `poe make_cluster` to create the cluster and `poe apply_task` to deploy the task to the cluster.
The make_cluster command will take several minutes to launch.

You can sequence these commands together with `poe deploy_task`, which will run `make_scripts`, `make_cluster`, and `apply_task` in sequence.
If you are using non-default environment files, you can run `poe deploy_task -e my_task.env -c my_cluster.env`.

#### Selecting deployment parameters

##### Kubernetes deployment parameters

Certain configuration parameters are fully defined by your project (project name, VPC subnetwork), and you have few options to chose.
Others are entirely your choice, like the task name or cluster name, and just affect how you see the task in the UI.
However, a few parameters will need to be tuned to the task at hand, like choosing the type of compute node or resource allocations. 

##### Compute type and resource allocation

There are a number of different types of compute node, each with [different CPU and memory resources and costs](https://cloud.google.com/compute/docs/machine-types).
For example, a `e2-standard-4` node has 4 CPU-equivalents and 16GB of RAM.
However, the actual resources available to your task will be slightly less than this, because Kubernetes and system management also take up some resources.
Estimate about 0.5 vCPU and up to 2GiB of RAM for each node will go to this overhead, but it may vary.
You will request both a number of nodes to create and the overall number of tasks to run across all nodes.
Ideally, the tasks will fill up the node resources as much as possible, since you pay per node hour, not per task hour.

Note that resources like memory and CPU can specify both a "request" and a "limit" value.
Generally speaking, the request values the minimum resources needed to put a pod with a task on a node, while the limit value sets a maximum value.
If the pod exceeds a resource limit, it will be terminated and a new one created.

*Tip*: There is no need to set a CPU limit, since you are reserving the whole node and CPU use will eventually come down.
However, it is useful to set a Memory limit, which will make Kubernetes kill a pod (that is, a worker) if it starts hogging too many resources and strangling the other pods.

#### Redeploying workers

You might need to redeploy workers to the cluster after adjusting the resource allocations or number of tasks.
Run `poe make_scripts` and `poe apply_task` again to update the cluster with the new configuration.

### 4. Tearing down your cluster

Once you are done with your tasks, you should delete your cluster to stop paying for its resources.
You can do this with `poe delete_cluster`, which will delete the cluster defined in `config/cluster.env`.
Alternatively, you can delete the cluster manually in the GCP console.

## Acknowledgements

Many thanks to Forrest Collman for piloting task distribution through task-queue, Ben Pedigo for allowing me to shamelessly copy his work in forming the basis of this template, and Will Silversmith for building amazing tools like python-task-queue and cloud-files.
