
################################################
# EXAMPLE config.json for the Theta ERC20 token
################################################
'''
{
  "ethereum_rpc_url" : "https://mainnet.infura.io",
  "smart_contract_address" : "0x3883f5e181fccaf8410fa61e12b59bad963fb645",
  "genesis_height" : 4728491
}
'''
################################################


import json
from common.utils import Logger
import traceback 


class ConfigKey:
  ETHEREUM_RPC_URL       = 'ethereum_rpc_url'
  SMART_CONTRACT_ADDRESS = 'smart_contract_address'
  GENESIS_HEIGHT         = 'genesis_height'
  EXPECTED_TOTAL_SUPPLY  = 'expected_total_supply'


class Config:
  
  def __init__(self):
    self.ethereum_rpc_url = ''
    self.smart_contract_address = ''
    self.genesis_height = 0
    self.expected_total_supply = 0

  def load(self, config_json):
    self.ethereum_rpc_url = config_json[ConfigKey.ETHEREUM_RPC_URL]
    self.smart_contract_address = config_json[ConfigKey.SMART_CONTRACT_ADDRESS]
    self.genesis_height = config_json[ConfigKey.GENESIS_HEIGHT]
    self.expected_total_supply = config_json[ConfigKey.EXPECTED_TOTAL_SUPPLY]


class ConfigManager:

  config = Config()

  @staticmethod
  def load(path_to_config_json):
    with open(path_to_config_json) as config_json_file:    
      config_json = json.load(config_json_file)
   
    config = ConfigManager.config
    try:
      config.load(config_json)
    except:
      Logger.printError('Failed to load config file! file path: %s %s'%(path_to_config_json, traceback.print_exc()))
      return False

    return True


