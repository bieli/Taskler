# -*- coding: utf-8 -*-

from TasksProvider import TasksProvider

if __name__ == "__main__":
#    tasks_to_run  = ['ExamplePrintsMessagesTask', 'CsvReaderFileStoregeTask']
    tasks_to_run  = ['ExamplePrintsMessagesTask']
    inputed_data  = [1, 2]
    outputed_data = None

    # run tasks example
    tasks_provider = TasksProvider()
#    tasks_provider.plugin_set_verbose(True)
#    tasks_provider.plugin_set_verbose(False)
#    tasks_provider.task_set_verbose(False)
    outputed_data = tasks_provider.run_tasks(tasks_to_run, inputed_data)

    print outputed_data
