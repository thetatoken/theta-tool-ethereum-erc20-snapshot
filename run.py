import os
import sys
from common.utils import Logger
from exporter.event_exporter import EthereumEventExporter
from analyzer.event_analyzer import EthereumEventAnalyzer

# Example: python run.py https://mainnet.infura.io 0x3883f5e181fccaf8410fa61e12b59bad963fb645 4728491 6958428 balance.json
if __name__ == '__main__':
  if len(sys.argv) != 6:
    print("\nUsage: python run.py <ethereum_rpc_url> <smart_contract_address> <start_height> <end_height> <balance_file_path>\n")
    exit(1)

  Logger.enableDebugLog()

  ethereum_rpc_url = sys.argv[1]
  smart_contract_address = sys.argv[2]
  start_height = int(sys.argv[3])
  end_height = int(sys.argv[4])
  balance_file_path = sys.argv[5]

  export_folder = "./data/events"
  if not os.path.exists(export_folder):
    os.makedirs(export_folder)

  Logger.printInfo('')
  Logger.printInfo('Start exporting Ethereum events...')
  eee = EthereumEventExporter(ethereum_rpc_url, smart_contract_address, export_folder)
  eee.Export(start_height, end_height)
  Logger.printInfo('Ethereum events exported.')
  Logger.printInfo('')

  Logger.printInfo('Start calculating token balances...')
  eea = EthereumEventAnalyzer()
  eea.Analyze(export_folder, balance_file_path)
  Logger.printInfo('Token balances calculated and exported.')
  Logger.printInfo('')




