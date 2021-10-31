import multiprocessing
import os

class JobProcess:
  job = None
  # TODO: Instead of sending env_vars and kwargs, send arguments (argparse)
  def __init__(self, fn_reference, env_vars, **kwargs):
    env_vars = {**os.environ, **env_vars}
    job = multiprocessing.Process(
      target=fn_reference,
      kwargs={'env': env_vars, **kwargs}
    )
    job.start()

    self.job = job
  def terminate(self):
    self.job.terminate()