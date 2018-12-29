from common.constants import ApiKey, ApiValue
from common.http.request import HttpRequest
from common.http.response import HttpSuccess, HttpError

class EthereumRpcService:

  def __init__(self, ethereum_rpc_url, smart_contract_address):
    self._http_request = HttpRequest(ethereum_rpc_url)
    self.smart_contract_address = smart_contract_address
    self.rpc_idx = 0

  def GetLogs(self, from_height, to_height):
    params = {
      ApiKey.JSONRPC: ApiValue.JSONRPC_VERSION,
      ApiKey.METHOD: ApiValue.ETH_GETLOGS,
      ApiKey.PARAMS: [{
        ApiKey.FROM_BLOCK: hex(from_height),
        ApiKey.TO_BLOCK: hex(to_height),
        ApiKey.ADDRESS: self.smart_contract_address
      }],
      ApiKey.ID: self.rpc_idx
    }
    self.rpc_idx += 1
    response = self._http_request.post('', params)
    return response
  
  def GetTokenBalance(self, smart_contract_address, account_address, target_height):
    BALANCE_OF_SIG = '0x70a08231' # signature of the ERC20 balanceOf() method
    data = BALANCE_OF_SIG + '000000000000000000000000' + account_address[2:]
    params = {
      ApiKey.JSONRPC: ApiValue.JSONRPC_VERSION,
      ApiKey.METHOD: ApiValue.ETH_CALL,
      ApiKey.PARAMS: [{
          ApiKey.FROM: account_address,
          ApiKey.TO: smart_contract_address,
          ApiKey.DATA: data
        },
        target_height
      ],
      ApiKey.ID: self.rpc_idx
    }
    self.rpc_idx += 1
    response = self._http_request.post('', params)
    balance = int(response.body, 16)
    return balance
 
