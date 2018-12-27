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
      ApiKey.JSONRPC: "2.0",
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

