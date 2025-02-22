from taskqueue import TaskQueue
from {{ cookiecutter.project_slug }}.task import run_task
import os
import pandas as pd

task_df = pd.read_feather(
    f"{os.environ.get('TASK_PARAMETER_FILENAME', 'tasks')}.feather"
)
if "cloudpath" not in task_df.columns:
    target_cloudpath = os.environ.get("CF_CLOUDPATH")
    task_df["cloudpath"] = target_cloudpath

task_args = task_df.to_dict(orient="records")

tq = TaskQueue(os.environ.get("TASKQUEUE_PATH"))

if __name__ == "__main__":
    tasks = (run_task(**task) for task in task_args)
    tq.insert(tasks, total=len(task_args))
