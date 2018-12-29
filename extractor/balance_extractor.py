from common.utils import Logger
from extractor.rpc import EthereumRpcService

class TokenBalanceExtractor:

  def __init__(self, ethereum_rpc_url, smart_contract_address):
    self.ethereum_rpc_service = EthereumRpcService(ethereum_rpc_url, smart_contract_address)
    self.smart_contract_address = smart_contract_address

  def Query(self, addresses, target_height):
    num_addresses = len(addresses)
    Logger.printInfo("Total number of addresses: %s"%(num_addresses))
    queried_balance_map = {}
    num_addresses_queried = 0
    for address in addresses:
      balance = self.ethereum_rpc_service.GetTokenBalance(
       smart_contract_address = self.smart_contract_address,
       account_address = address,
       target_height = hex(target_height)
      )
      balance_str = str(balance)
      queried_balance_map[address] = balance_str
      num_addresses_queried += 1
      if num_addresses_queried % 1000 == 0:
        Logger.printInfo("%s addresses queried."%(num_addresses_queried))
    Logger.printInfo("%s addresses queried."%(num_addresses_queried))
    return queried_balance_map

