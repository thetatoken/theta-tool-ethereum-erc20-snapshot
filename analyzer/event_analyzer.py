import re
import json
from os import listdir
from os.path import isfile
from common.constants import ApiKey
from common.utils import Logger
from extractor.event_extractor import EthereumEventExtractor


class EthereumEventAnalyzer:
  
  ZERO_ADDR = '0x0000000000000000000000000000000000000000' 
  TRANSFER_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
  APPROVAL_TOPIC = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'
  
  def __init__(self):
    pass

  def Analyze(self, event_file_folder, target_height):
    balance_map = {}
    event_file_regex = re.compile(EthereumEventExtractor.FILENAME_REGEX)
    filenames = sorted([f for f in listdir(event_file_folder) if event_file_regex.search(f)])
    for filename in filenames:
      match_res = event_file_regex.match(filename)
      if match_res:
        file_path = event_file_folder + '/' + filename
        self.analyzeFile(file_path, target_height, balance_map)
    balance_map = self.filterOutAddressesWithZeroBalance(balance_map)
    balance_map = self.convertBalanceToString(balance_map)
    return balance_map

  def analyzeFile(self, file_path, target_height, balance_map):
    with open(file_path) as f:
      data = json.load(f)
    for event_json in data:
      block_height = int(self.getBlockHeight(event_json), 16)
      if block_height > target_height:
        break

      from_addr, to_addr, amount = '', '', 0
      event_topic = self.getEventTopic(event_json)
      if event_topic == EthereumEventAnalyzer.TRANSFER_TOPIC:
        from_addr, to_addr, amount = self.analyzeTransferEvent(event_json)
      elif event_topic == EthereumEventAnalyzer.APPROVAL_TOPIC:
        from_addr, to_addr = self.analyzeApprovalEvent(event_json) # approve() transfers ZERO token
      
      if (len(from_addr) == 0) or (len(to_addr) == 0):
        Logger.printWarning('failed to process event: %s'%(event_json))
        continue

      from_balance = balance_map.get(from_addr, 0)
      if (from_balance < amount) and (not(from_addr == EthereumEventAnalyzer.ZERO_ADDR)):
        Logger.printError('from_balance < amount. from_addr: %s, to_addr: %s, amount: %s, event: %s'%(\
          from_addr, to_addr, amount, event_json))
        exit(1)
      
      if from_addr == EthereumEventAnalyzer.ZERO_ADDR:
        updated_from_balance = from_balance # minting token
      else:
        updated_from_balance = from_balance - amount
      balance_map[from_addr] = updated_from_balance

      to_balance = balance_map.get(to_addr, 0)
      updated_to_balance = to_balance + amount
      balance_map[to_addr] = updated_to_balance

  def getBlockHeight(self, event_json):
    block_height = event_json.get(ApiKey.BLOCK_NUMBER, -1)
    if block_height < 0:
      Logger.printError('Cannot extract block number: %s'%(event_json))
      exit(1)
    return block_height

  def getEventTopic(self, event_json):
    topics = event_json.get(ApiKey.TOPICS, None)
    if (topics is None) or (len(topics) == 0):
      return None
    event_topic = topics[0]
    return event_topic

  def analyzeTransferEvent(self, transfer_event_json):
    from_addr, to_addr, amount = '', '', 0
    topics = transfer_event_json.get(ApiKey.TOPICS, None)
    data = transfer_event_json.get(ApiKey.DATA, None)
    if (topics is None) or (len(topics) != 3) or (data is None):
      return from_addr, to_addr, amount
    from_addr = self.extractAddressFromTopic(topics[1])
    to_addr = self.extractAddressFromTopic(topics[2])
    amount = self.extractTransferAmountFromData(data)
    return from_addr, to_addr, amount

  def analyzeApprovalEvent(self, approval_event_json):
    from_addr, to_addr = '', ''
    topics = approval_event_json.get(ApiKey.TOPICS, None)
    if (topics is None) or (len(topics) != 3):
      return from_addr, to_addr
    from_addr = self.extractAddressFromTopic(topics[1])
    to_addr = self.extractAddressFromTopic(topics[2])
    return from_addr, to_addr
 
  def extractAddressFromTopic(self, topic):
    addr = '0x' + topic[26:]
    return addr

  def extractTransferAmountFromData(self, data):
    amount = int(data, 16)
    return amount

  def filterOutAddressesWithZeroBalance(self, balance_map):
    filtered_balance_map = {}
    for (addr, bal) in balance_map.iteritems():
      if bal != 0:
        filtered_balance_map[addr] = bal
    return filtered_balance_map

  def convertBalanceToString(self, balance_map):
    converted_balance_map = {}
    for (addr, bal) in balance_map.iteritems():
      converted_balance_map[addr] = str(bal)
    return converted_balance_map

