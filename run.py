import os
import sys
import json
from common.utils import Logger
from common.config_manager import ConfigManager
from extractor.event_extractor import EthereumEventExtractor
from extractor.balance_extractor import TokenBalanceExtractor
from analyzer.event_analyzer import EthereumEventAnalyzer


def exportTokenBalance(ethereum_rpc_url, smart_contract_address, expected_total_supply, genesis_height, target_height, balance_file_path):
  export_folder = "./data/events"
  if not os.path.exists(export_folder):
    os.makedirs(export_folder)

  Logger.printInfo('')
  Logger.printInfo('Start exporting Ethereum events...')
  eee = EthereumEventExtractor(ethereum_rpc_url, smart_contract_address, export_folder)
  eee.Export(genesis_height, target_height)
  Logger.printInfo('Ethereum events exported.')
  Logger.printInfo('')

  Logger.printInfo('Start extracting token holders...')
  eea = EthereumEventAnalyzer()
  analyzed_balance_map = eea.Analyze(export_folder, target_height)
  Logger.printInfo('Token holders extracted.')
  Logger.printInfo('')
  
  with open(balance_file_path + '.analyzed', 'w') as balance_file:
    json.dump(analyzed_balance_map, balance_file, indent=2)
 
  Logger.printInfo('Start querying the balance of each holder at block height %s, may take a while...'%(target_height))
  token_holder_addresses = analyzed_balance_map.keys()
  tbe = TokenBalanceExtractor(ethereum_rpc_url, smart_contract_address)
  queried_balance_map = tbe.Query(token_holder_addresses, target_height)
  Logger.printInfo('Token holders balance retrieved.')
  Logger.printInfo('')

  with open(balance_file_path + '.queried', 'w') as balance_file:
    json.dump(queried_balance_map, balance_file, indent=2)

  Logger.printInfo('Start sanity checks...')
  if not sanityChecks(analyzed_balance_map, queried_balance_map, expected_total_supply):
    Logger.printError('Sanity checks failed.')
    exit(1)
  Logger.printInfo('Sanity checks all passed.')
  Logger.printInfo('')

  with open(balance_file_path, 'w') as balance_file:
    json.dump(queried_balance_map, balance_file, indent=2)
  
  Logger.printInfo('Token balances calculated and exported to: %s'%(balance_file_path))
  Logger.printInfo('')

def sanityChecks(analyzed_balance_map, queried_balance_map, expected_total_supply):
  total_supply = 0
  for address in analyzed_balance_map.keys():
    analyzed_balance = analyzed_balance_map[address]
    queried_balance = queried_balance_map.get(address, -1)
    if (analyzed_balance != queried_balance) or (queried_balance == -1):
      Logger.printError("Balance mismatch for address: %s, analyzed_balance = %s, queried_balance = %s"%(
        address, analyzed_balance, queried_balance))
      return False
    total_supply += int(queried_balance)

  Logger.printInfo('Expected total supply  : %s'%(expected_total_supply))
  Logger.printInfo('Sum of queried balances: %s'%(total_supply))
  if total_supply != expected_total_supply:
    Logger.printError('Token total supply mismatch. expected = %s, calculated = %s'%(expected_total_supply, total_supply))
    return False

  return True

  
#
### Example: extract all the Theta ERC20 token holder addresses and balances at block height 6958428, and save to ./balance.json
#
#    python run.py config.json 6958428 balance.json
#
### The config.json file for this example:
#    {
#      "ethereum_rpc_url" : "http://localhost:8545",
#      "smart_contract_address" : "0x3883f5e181fccaf8410fa61e12b59bad963fb645",
#      "genesis_height" : 4728491
#      "expected_total_supply" : 1000000000000000000000000000
#    }
#

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print("\nUsage: python run.py <config_file_path> <target_height> <balance_file_path>\n")
    exit(1)
  #Logger.enableDebugLog()

  config_file_path = sys.argv[1]
  target_height = int(sys.argv[2])
  balance_file_path = sys.argv[3]
  
  cfgMgr = ConfigManager()
  if not cfgMgr.load(config_file_path):
    Logger.printError('Failed to load config: %s'%(config_file_path))
    exit(1)
  
  config = cfgMgr.config
  ethereum_rpc_url = config.ethereum_rpc_url
  smart_contract_address = config.smart_contract_address
  expected_total_supply = config.expected_total_supply
  genesis_height = config.genesis_height

  exportTokenBalance(ethereum_rpc_url, smart_contract_address, expected_total_supply,
    genesis_height, target_height, balance_file_path)


