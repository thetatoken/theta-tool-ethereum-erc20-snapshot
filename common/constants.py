
from utils import Logger, ErrorReporter

class ApiStatus:
  OK      = 'OK'
  SUCCESS = 'SUCCESS'
  ERROR   = 'ERROR'


class ApiKey:
  STATUS     = 'status'
  ERROR_CODE = 'error_code'
  MESSAGE    = 'message'
  BODY       = 'body'
  
  ID         = 'id'
  JSONRPC    = 'jsonrpc'
  METHOD     = 'method'
  PARAMS     = 'params'
  FROM_BLOCK = 'fromBlock'
  TO_BLOCK   = 'toBlock'
  ADDRESS    = 'address'
  BLOCK_NUMBER = 'blockNumber'

  TOPICS     = 'topics'
  DATA       = 'data'
  FROM       = 'from'
  TO         = 'to'


class ApiValue:
  JSONRPC_VERSION = '2.0'
  ETH_GETLOGS = 'eth_getLogs'
  ETH_CALL    = 'eth_call'


class ApiErrorCode:
  NO_ERROR = 0

  # Generic errors
  GENERIC_ERROR           = 10000
  SERVER_CONNECTION_ERROR = 10001
  INVALID_RESPONSE_FORMAT = 10002
  
