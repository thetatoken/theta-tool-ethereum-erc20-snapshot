

class DataObject(object):

  @staticmethod
  def getAttributeFromJson(key, json_obj, default_value):
    if json_obj.get(key, None) == None:
      return default_value
    else:
      return json_obj[key]
  

