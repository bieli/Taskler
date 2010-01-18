# -*- coding: utf-8 -*-

import sys
import os

from PluginProvider import PluginProvider

class Task(object):
    capabilities = []

    def __repr__(self):
        return '<%s %r>' % (
            self.__class__.__name__,
            self.capabilities
        )

_tasks_instances = {}

class TasksProvider(Task):
    PLUGINS_CFG     = {'plugin_path': 'plugins/',
                       'plugins':     []}
    TASKS_CFG       = {'tasks_path': 'tasks/',
                       'tasks':     []}
    CAPABILITIES    = 'proccess'
    INPUT_DATA      = []
    OUTPUT_DATA     = []
    PROCCESS_DATA   = []
    PLUGIN_PROVIDER = []
    PLUGIN_VERBOSE  = True
    TASK_VERBOSE    = True

    def plugin_set_verbose(self, verbose):
        self.PLUGIN_VERBOSE = verbose

    def task_set_verbose(self, verbose):
        self.TASK_VERBOSE = verbose

    def plugins_configure(self, plugin_provider, capabilities = None):
        if None <> capabilities:
            self.CAPABILITIES    = capabilities

        self.PLUGINS_CFG['plugins']  = plugin_provider

    def run(self, data):
        self.INPUT_DATA    = data
        self.PROCCESS_DATA = self.INPUT_DATA

        self.PLUGIN_PROVIDER = PluginProvider()
        self.PLUGIN_PROVIDER.init_plugin_system(self.PLUGINS_CFG)

        plugins = self.PLUGIN_PROVIDER.get_plugins_by_capability(\
                                            self.CAPABILITIES)

        # set verbose mode in plugins
        for plugin in plugins:
            plugin.plugin_set_verbose(self.PLUGIN_VERBOSE)

        # inilialize plugins
        for plugin in plugins:
            plugin.plugin_init()

        # proccess data in plugins
        for plugin in plugins:
            plugin.plugin_set_data(self.PROCCESS_DATA)
            plugin.plugin_proccess()
            plugin.plugin_get_data_count()
            self.PROCCESS_DATA = plugin.plugin_get_data()

        # deinilialize plugins
        for plugin in plugins:
            plugin.plugin_deinit()

        self.OUTPUT_DATA = self.PROCCESS_DATA

        return self.OUTPUT_DATA

    def run_tasks(self, tasks, data):
        self.TASKS_CFG['tasks'] = tasks
        self.INPUT_DATA         = data
        self.PROCCESS_DATA      = self.INPUT_DATA

        self.TASK_PROVIDER = TasksProvider()
        self.TASK_PROVIDER.init_tasks_system(self.TASKS_CFG)

        all_tasks = self.TASK_PROVIDER.get_tasks_by_capability('task_run')

        found_tasks = []
        for task in all_tasks:
#            print "[ DEBUG ] task: " + str(task)
#            print "[ DEBUG ] all_tasks: " + str(all_tasks)
            if task in tasks:
                found_tasks.append(task)

        if True == self.TASK_VERBOSE:
            print "Searched tasks '%s'" % tasks
            print "Found tasks '%s'" % found_tasks
            print _tasks_instances

        for found_tasks in tasks:
            task.task_set_verbose(self.TASK_VERBOSE)
            self.PROCCESS_DATA = task.task_run(self.PROCCESS_DATA)

        self.OUTPUT_DATA = self.PROCCESS_DATA

        return self.OUTPUT_DATA

    def init_tasks_system(self, cfg = None):
        if None == cfg:
            cfg = self.TASKS_CFG
        if not cfg['tasks_path'] in sys.path:
            sys.path.insert(0, cfg['tasks_path'])

#        print "tasks_path: '%s' " % cfg['tasks_path']
        loaded_tasks = self.load_tasks(cfg['tasks'])
#        print "loaded tasks: '%s' " % loaded_tasks

    def get_tasks_by_capability(self, capability):
        result = []
        for task in Task.__subclasses__():
#            print "task1: '%s' " % task
            if capability in task.capabilities:
#                print "capability: '%s' " % capability
                if not task in _tasks_instances:
                    _tasks_instances[task] = task()
                result.append(_tasks_instances[task])

        return result

    def load_tasks(self, tasks):
        for task in tasks:
            __import__(task, None, None, [''])

    def find_tasks(self):
        return Task.__subclasses__()

    def get_available_tasks(self):
        self.TASK_PROVIDER = TasksProvider()
        self.TASK_PROVIDER.init_tasks_system(self.TASKS_CFG)

        all_tasks = self.TASK_PROVIDER.get_tasks_by_capability('task_run')

        if len(all_tasks) > 0:
            return all_tasks
        else:
            return None

    def show_available_tasks(self):
        all_tasks = self.get_available_tasks()

        if len(all_tasks) > 0:
            for task in all_tasks:
                print "task: " + task
        else:
            print "No tasks available !"
