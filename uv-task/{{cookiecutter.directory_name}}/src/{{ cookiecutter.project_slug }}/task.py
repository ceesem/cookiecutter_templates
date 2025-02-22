import taskqueue
from cloudfiles import CloudFiles
from caveclient import CAVEclient, session_config
from functools import partial

session_config.set_session_defaults(
    max_retries=10,
    pool_block=True,
    pool_maxsize=10,
    backoff_factor=1,
)


@taskqueue.queueable
def _run_task():
    """
    Define your actual task function here.
    """
    pass


def run_task(*args, **kwargs):
    return partial(_run_task, *args, **kwargs)
