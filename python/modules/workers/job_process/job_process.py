import multiprocessing

class JobProcess:
  job = None
  # TODO: Instead of sending env_vars and kwargs, send arguments (argparse)
  def __init__(self, fn_reference, arg_flags):
    job = multiprocessing.Process(
      target=fn_reference,
      kwargs={'arg_flags': arg_flags}
    )
    job.start()

    self.job = job
  def terminate(self):
    self.job.terminate()