# -*- coding: utf-8 -*-

from TasksProvider import Task, TasksProvider

class ExamplePrintsMessagesTask(Task):
    capabilities = ['task_run', 'task_set_verbose']
    TASK_PLUGINS = ['GetConfigProfilePlugin', 'PrintHelloFromMethodsPlugin']
    TASK_VERBOSE = False
    tp = None

    def __init__(self, task_plugins = None):
        self.tp = TasksProvider()
        if None == task_plugins:
            self.tp.plugins_configure(self.TASK_PLUGINS)
        else:
            self.tp.plugins_configure(task_plugins)

    def task_set_verbose(self, verbose):
        self.TASK_VERBOSE = verbose

    def task_run(self, data):
        return self.tp.run(data)

    def get_test(self):
        return "1234"
