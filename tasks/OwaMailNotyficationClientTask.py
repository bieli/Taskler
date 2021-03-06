# -*- coding: utf-8 -*-

from tasks.TasksProvider import Task
from tasks import TasksProvider


class OwaMailNotyficationClientTask(Task):
    capabilities = ['task_run', 'task_set_verbose']
    TASK_PLUGINS = ['OwaLoginAndGetRecivedEmailsSubjectsPagePlugin',
                    'SystemTrayMessageNotyficationPlugin']
    TASK_VERBOSE = False
    tp = None

    def __init__(self, task_plugins=None):
        self.tp = TasksProvider()
        if None == task_plugins:
            self.tp.plugins_configure(self.TASK_PLUGINS)
        else:
            self.tp.plugins_configure(task_plugins)

    def set_verbose(self, verbose):
        self.TASK_VERBOSE = verbose

    def task_run(self, data):
        return self.tp.run(data)
