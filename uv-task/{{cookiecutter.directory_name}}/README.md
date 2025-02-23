Welcome to {{ cookiecutter.project_name }}!

Please set any blank environment variables in the `.env` file.

Notes:
  * src/YOUR_PROJECT/task.py is the entry point for your task. If you want to use all the defaults, don't modify the `run_task` function and instead put your detailed task definition in the `_run_task` function, which does the actual work.
  * The arguments are passed to the `_run_task` function as a pandas dataframe saved, by default at least, as a feather file. The keys are the names of the arguments and the values are the values of the arguments. Specify the name of this file in the `TASK_PARAMETER_FILENAME` environment variable (without the `.feather` extension).
  * A `.env` file must be present if you are using the `poe` commands, but it does not need to actually contain your environment variables if you have them set another way.
  