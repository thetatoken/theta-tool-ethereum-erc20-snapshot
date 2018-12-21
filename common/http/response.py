
from common.constants import ApiStatus, ApiKey, ApiErrorCode


class HttpResponse:

  def __init__(self, status, error_code, message, body):
    self.status      = status
    self.error_code  = error_code
    self.message     = message
    self.body        = body
    self.is_parsed   = False
    self.parsed_body = None
  
  def isSuccess(self):
    return False
  
  def setParseSuccess(self, is_parsed = True):
    self.is_parsed = is_parsed

  def parseSuccess(self):
    return self.is_parsed

  def toJson(self):
    return {
      ApiKey.STATUS     : self.status,
      ApiKey.ERROR_CODE : self.error_code,
      ApiKey.MESSAGE    : self.message,
      ApiKey.BODY       : self.body
    }


class HttpSuccess(HttpResponse):
  
  def __init__(self, body):
    self.status      = ApiStatus.OK
    self.error_code  = ApiErrorCode.NO_ERROR
    self.message     = ''
    self.body        = body
    self.is_parsed   = False
    self.parsed_body = None
  
  def isSuccess(self):
    return True


class HttpError(HttpResponse):
  
  def __init__(self, error_code, message):
    self.status      = ApiStatus.ERROR
    self.error_code  = error_code
    self.message     = message
    self.body        = {}
    self.is_parsed   = False
    self.parsed_body = None

  def isSuccess(self):
    return False


