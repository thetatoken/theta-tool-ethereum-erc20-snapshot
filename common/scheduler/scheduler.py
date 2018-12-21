# Author: Jieyi Long (jieyi@sliver.tv)
# Date: Apr 2016

import sys
import time
import traceback
import logging
import schedule, time
from datetime import datetime
from common.utils import Logger
from threading import Thread, Lock


class SchedulerLogFilter(logging.Filter):
  def filter(self, record):
    return not 'maximum number of running instances reached' in record.msg


class JobScheduler:

  MAX_SECOND_COUNT = 3600 * 24 * 365 # num seconds in one year

  def __init__(self, wakeup_interval_in_seconds = 1, max_job_invocation_count = None):
    logging.basicConfig()
    logging.getLogger("apscheduler.scheduler")\
           .addFilter(SchedulerLogFilter())

    schedule.every(wakeup_interval_in_seconds)\
            .seconds\
            .do(self._executeJobs)

    if max_job_invocation_count is not None:
      self._max_job_invocation_count = int(max_job_invocation_count)
    else:
      self._max_job_invocation_count = None
    self._job_invocation_count = 0
    
    self._mutex = Lock()
    self._job_list = []
    self._enableJobs()
    self._second_counter = 0
    self._wakeup_interval_in_seconds = wakeup_interval_in_seconds 

  def run(self):
    try:
      while True:
          schedule.run_pending()
          time.sleep(1)
          
          if (self._max_job_invocation_count is not None) and \
             (self._job_invocation_count >= self._max_job_invocation_count):
            Logger.printInfo('Max job invocation count reached. Exiting...')
            break 

    except (KeyboardInterrupt, SystemExit):
      pass

  def clearJobs(self, job):
    self._job_list = []

  def addJob(self, job):
    self._job_list.append(job)

  def addJobs(self, job_list):
    self._job_list += job_list
  
  def _enableJobs(self):
    self._mutex.acquire()
    self._jobs_enabled = True
    self._mutex.release()

  def _disableJobs(self):
    self._mutex.acquire()
    self._jobs_enabled = False
    self._mutex.release()
  
  def _executeJobs(self):
    if self._jobs_enabled:
      self._disableJobs()
      for job in self._job_list:
        try:
          
          job.execute(self._second_counter)

        except Exception as e:
          Logger.printError('Caught job exception: ' + str(e))
          traceback.print_exc()
          pass
        
        self._job_invocation_count += 1
    
      self._enableJobs()

    self._second_counter += self._wakeup_interval_in_seconds
    if self._second_counter >= JobScheduler.MAX_SECOND_COUNT:
      self._second_counter = 0

  def _shutdown(self):
    exit(1)


