from taskqueue import TaskQueue
from {{ cookiecutter.project_slug }}.task import run_task, filter_tasks
import os
import pandas as pd

task_df = pd.read_feather(
    f"{os.environ.get('TASK_PARAMETER_FILENAME', 'tasks')}.feather"
)
target_cloudpath = os.environ.get("CF_CLOUDPATH")

if "cloudpath" not in task_df.columns:
    task_df["cloudpath"] = target_cloudpath

# Filter out tasks that have already been completed
original_number = len(task_df)
task_df = filter_tasks(task_df, target_cloudpath)
print(f"Inserting {len(task_df)}/{original_number} tasks!")
task_args = task_df.to_dict(orient="records")

tq = TaskQueue(os.environ.get("TASKQUEUE_PATH"))

if __name__ == "__main__":
    if len(task_args) == 0:
        print("No tasks to insert!")
        exit(0)
    tasks = (run_task(**task) for task in task_args)
    tq.insert(tasks, total=len(task_args))