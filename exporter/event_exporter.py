import re
import json
from exporter.rpc import EthereumRpcService
from os import listdir
from os.path import isfile, join
from common.utils import Logger


class EthereumEventExporter:
  
  HEIGHT_STEP = 10000
  FILENAME_FORMAT = '%s_events_%s_to_%s.txt'
  FILENAME_REGEX = '(?P<smaddr>[a-fx0-9]+)_events_(?P<from>[0-9]+)_to_(?P<to>[0-9]+)\.txt'

  def __init__(self, ethereum_rpc_url, smart_contract_address, export_folder):
    self.ethereum_rpc_service = EthereumRpcService(ethereum_rpc_url, smart_contract_address)
    self.smart_contract_address = smart_contract_address
    self.export_folder = export_folder

  def Export(self, start_height, end_height):
    Logger.printInfo("Start to export events from height %s to %s..."%(start_height, end_height))
    current_height = self.getProcessedHeight()
    if current_height >= start_height:
      Logger.printInfo("Already exported up to height %s"%(current_height))
      if current_height < end_height:
        Logger.printInfo("Continue from height %s..."%(current_height+1))
    else:
      current_height = start_height - 1
    while current_height < end_height:
      from_height = current_height + 1
      to_height = min(from_height + EthereumEventExporter.HEIGHT_STEP - 1, end_height)
      self.export(from_height, to_height)
      current_height = to_height
      Logger.printInfo("Exported events from height %s to %s"%(from_height, to_height))

  # export the events from from_height to to_height (both inclusive)
  def export(self, from_height, to_height):
    query_results = self.ethereum_rpc_service.GetLogs(from_height, to_height)
    event_file_name = EthereumEventExporter.FILENAME_FORMAT%(self.smart_contract_address, from_height, to_height)
    event_file_path = self.export_folder + '/' + event_file_name
    with open(event_file_path, 'w') as event_file:
      json.dump(query_results.body, event_file)

  def getProcessedHeight(self):
    current_height = 0
    event_file_regex = re.compile(EthereumEventExporter.FILENAME_REGEX)
    filenames = [f for f in listdir(self.export_folder) if event_file_regex.search(f)]
    for filename in filenames:
      match_res = event_file_regex.match(filename)
      if match_res:
        current_height = max(current_height, int(match_res.groups()[2]))
    return current_height


