
import imp
import sys

"""
#TODO: PROTOTYPE ONLY
Example with TaskResource abstraction:

tr = TaskResource('MemcacheTaskResource')

my_key_values = [1,323,34,45,455]
tr.store('my_key', my_key_values, 3600)

data = tr.restore('my_key')

"""
class TaskResource():
   driver_resource   = None
   driver_full_name  = 'MemcacheTaskResource'
   driver_parameters = ['127.0.0.1:11211']
   debug             = False

   # initialize driver driver_full_name
   def __init__(self, driver_full_name = 'MemcacheTaskResource',\
                driver_parameters = ['127.0.0.1:11211']):

      self.driver_full_name = driver_full_name
      self.driver_parameters = driver_parameters
      self.driver_resource = TaskResource.create(self.driver_full_name)

   def import_module(self, path, name, unique_name,\
                globals=None, locals=None, fromlist=None):
      # Fast path: see if unique_name has already been imported.
      try:
          return sys.modules[unique_name]
      except KeyError:
          pass

      sys.path.append(path)
      fp, pathname, description = imp.find_module(name)
      sys.path.pop(-1)

      try:
          return imp.load_module(unique_name,fp, pathname, description)
      finally:
          # Since we may exit via an exception, close fp explicitly.
          if fp:
              fp.close()

   # init driver
   def init(self, data = None):
      return True

   # create factory method
   @staticmethod
   def create(self, data = None):
      self.driver_loaded_module = import_module('', '', self.driver_full_name)
      self.driver_resource = self.driver_loaded_module()

      return self.driver_resource

   # deinit driver
   def deinit(self):
      self.clear()
      self.driver_resource = None
      return True

   # storing data in resource
   def store(self, data_key, values, lifetime = None):
      self.lifetime = lifetime
      return True

   def restore(self):
      #TODO: resting data from resource

   def clear(self):
      #TODO: clear all data storing in resource

      return True

   def set_lifetime(self, lifetime):
      #TODO: set data lifetime
      return True

   def get_info(self):
      return 'INFO....'

   def set_debug(self, debug):
      self.debug = debug
      return True

tr = TaskResource('MemcacheTaskResource')

my_key_values = [1,323,34,45,455]
tr.store('my_key', my_key_values, 3600)

data = tr.restore('my_key')
