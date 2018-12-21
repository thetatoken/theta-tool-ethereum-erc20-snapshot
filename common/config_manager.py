
#######################################
# EXAMPLE config.json
#######################################
'''
{
  "beta" : {
    "print_trivia_only" : true,
    "backend_public_dispatcher_root_url" : "https://beta-api.sliver.tv/v1",
    "backend_private_dispatcher_root_url" : "http://54.187.196.9:7070/v1",
    "trivia_game_ids" : ["gamakfkg09evym3zijx"]
  },

  "prod" : {
    "print_trivia_only" : true,
    "backend_public_dispatcher_root_url" : "https://api.sliver.tv/v1",
    "backend_private_dispatcher_root_url" : "http://54.89.131.120:7070/v1",
    "trivia_game_ids" : ["gamakfkg09evym3zijx"]
  }
}

'''
#######################################


import json
from common.utils import Logger
import traceback 


class ConfigKey:
  BETA = 'beta'
  PROD = 'prod'

  PRINT_TRIVIA_ONLY = 'print_trivia_only'
  BACKEND_PUBLIC_DISPATCHER_ROOT_URL = 'backend_public_dispatcher_root_url'
  BACKEND_PRIVATE_DISPATCHER_ROOT_URL = 'backend_private_dispatcher_root_url'
  TRIVIA_GAME_IDS = 'trivia_game_ids'
  TRIVIA_CHANNEL_IDS = 'trivia_channel_ids'
  DTOS_MAP = 'DtoSmap'

class DtoSmap:
  def __init__(self):
    self.dList = []
    self.map = {}
  def load(self, config_json):
    self.dList = config_json['dList']
    config_json.pop('dList', None)
    self.map = config_json
  def getStake(self, diff):
    re = 0
    for d in self.dList:
      try:
        if d <= int(diff):
          re = self.map.get(str(d), 10)
          break
      except :
        Logger.printWarning('difficulty is not an integer : ' + str(diff))
    return re

class EnvConfig:
  
  def __init__(self):
    self.print_trivia_only = True
    self.backend_public_dispatcher_root_url = None
    self.backend_private_dispatcher_root_url = None
    self.trivia_game_ids = []
    self.trivia_channel_ids = []

  def load(self, config_json):
    self.print_trivia_only = config_json[ConfigKey.PRINT_TRIVIA_ONLY]
    self.backend_public_dispatcher_root_url = config_json[ConfigKey.BACKEND_PUBLIC_DISPATCHER_ROOT_URL]
    self.backend_private_dispatcher_root_url = config_json[ConfigKey.BACKEND_PRIVATE_DISPATCHER_ROOT_URL]
    self.trivia_game_ids = config_json[ConfigKey.TRIVIA_GAME_IDS]
    self.trivia_channel_ids = config_json[ConfigKey.TRIVIA_CHANNEL_IDS]
    print(self.trivia_game_ids);

class Config:

  def __init__(self):
    self.beta = EnvConfig()
    self.prod = EnvConfig()
    self.dsMap = DtoSmap()
  
  def load(self, config_json):
    self.beta.load(config_json[ConfigKey.BETA])
    self.prod.load(config_json[ConfigKey.PROD])
    self.dsMap.load(config_json[ConfigKey.DTOS_MAP])

class ConfigManager:

  config = Config()
  _use_prod_env = False

  @staticmethod
  def setProdEnv(use_prod_env = True):
    ConfigManager._use_prod_env = use_prod_env
   
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

  @staticmethod
  def getEnvConfig():
    if ConfigManager._use_prod_env:
      return ConfigManager.config.prod
    else:
      return ConfigManager.config.beta




