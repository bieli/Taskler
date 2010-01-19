
import memcache
from zlib import adler32

"""
#TODO: PROTOTYPE ONLY

Example with TaskResource abstraction:

tr = TaskResource('MemcacheTaskResource')

my_key_values = [1,323,34,45,455]
tr.store('my_key', my_key_values, 3600)

data = tr.restore('my_key')
"""
class MemcacheTaskResource(TaskResource):
   def init(self, data = None):
      self.driver_resource = memcache.Client(self.driver_parameters, self.debug)
      # alternative hasing algoritm (default is crc32)
      memcache.serverHashFunction = adler32

      self.driver_full_name = driver_full_name
      self.driver_parameters = driver_parameters
      return True

   def deinit(self):
      #TODO: deinit driver

   # storing data in resource
   def store(self, data_key, values, lifetime = None):
      if None == lifetime:
         lifetime = self.lifetime

      self.driver_resource.set(data_key, values, lifetime)
      return True

   # resting data from resource
   def restore(self, data_key):
      return self.driver_resource.get(data_key)

   #TODO: clear all data storing in resource
   def clear(self):

      return True

   def get_info(self):
      return 'MemcacheTaskResource v0.1'


