
import re
import sys
import subprocess
import time
import calendar
from datetime import datetime


def toUnicode(item):
  if isinstance(item, str):
    item_unicode = unicode(item, errors='ignore')
  else:
    item_unicode = unicode(item)
  return item_unicode


class TimeUtils:

  @staticmethod
  def utcSecondsSinceEpoch():
    seconds = int(round(calendar.timegm(time.gmtime())))
    return seconds
  
  @staticmethod
  def utcMillisecondsSinceEpoch():
    milliseconds = int(round(1000 * calendar.timegm(time.gmtime())))
    return milliseconds


class Logger(object):

  DEBUG_MODE = False
  LOG_FILE_PATH = None

  @staticmethod
  def enableDebugLog(enabled = True):
    Logger.DEBUG_MODE = enabled

  @staticmethod
  def setLogFolder(log_file_folder):
    Logger.LOG_FILE_PATH = log_file_folder + '/log_' + str(TimeUtils.utcSecondsSinceEpoch()) + '.txt'

  @staticmethod
  def printInfo(msg):
    printed_msg = str(datetime.now()) + '\033[97m [Info] ' + toUnicode(msg) + '\033[0m'
    Logger._writeToLogFile(printed_msg)
    print printed_msg
    sys.stdout.flush()
    return printed_msg

  @staticmethod
  def printWarning(msg):
    printed_msg = str(datetime.now()) + '\033[93m [Warning] ' + toUnicode(msg) + '\033[0m'
    Logger._writeToLogFile(printed_msg)
    print printed_msg
    sys.stdout.flush()
    return printed_msg

  @staticmethod
  def printError(msg):
    printed_msg = str(datetime.now()) + '\033[91m [Error] ' + toUnicode(msg) + '\033[0m'
    Logger._writeToLogFile(printed_msg)
    print printed_msg
    sys.stdout.flush()
    return printed_msg

  @staticmethod
  def printDebug(msg):
    printed_msg = str(datetime.now()) + '\033[50m [Debug] ' + toUnicode(msg) + '\033[0m'
    Logger._writeToLogFile(printed_msg)
    if Logger.DEBUG_MODE:
      print printed_msg
      sys.stdout.flush()
    return printed_msg

  @staticmethod
  def _writeToLogFile(msg):
    if Logger.LOG_FILE_PATH is not None:
      log_file = open(Logger.LOG_FILE_PATH, 'a', 0) 
      w_msg  = msg.encode('utf-8').strip() 
      log_file.write(w_msg + '\n')
      log_file.close()


class ErrorReporter:

  @staticmethod
  def reportError(error_message):
    printed_error_msg = Logger.printError(error_message)
    # TODO: send out email...


