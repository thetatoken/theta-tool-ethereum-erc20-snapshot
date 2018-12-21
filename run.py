import os
import sys
from common.utils import Logger
from exporter.event_exporter import EthereumEventExporter

if __name__ == '__main__':
  if len(sys.argv) != 5:
    print("\nUsage: python run.py <ethereum_rpc_url> <smart_contract_address> <start_height> <end_height>\n")
    exit(1)

  Logger.enableDebugLog()

  ethereum_rpc_url = sys.argv[1]
  smart_contract_address = sys.argv[2]
  start_height = int(sys.argv[3])
  end_height = int(sys.argv[4])
  export_folder = "./ethereum_events"
  if not os.path.exists(export_folder):
    os.mkdir(export_folder)

  eee = EthereumEventExporter(ethereum_rpc_url, smart_contract_address, export_folder)
  eee.Export(start_height, end_height)


