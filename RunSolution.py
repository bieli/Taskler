# -*- coding: utf-8 -*-
import sys
import os
from __builtin__ import file

from tasks import TasksProvider


class RunSolution:
    SOLUTIONS_DIR = 'solutions'
    SOLUTION_FILE_EXT = '.yml'

    def __init__(self, solutions_dir='solutions'):
        if self.SOLUTIONS_DIR != solutions_dir:
            self.SOLUTIONS_DIR = solutions_dir

    def get_solution_config_from_yaml(self, solution_name):

        # read yaml solution configuration
        from yaml import load

        try:
            from yaml import CLoader as Loader
            from yaml import CDumper as Dumper
        except ImportError:
            from yaml import Loader, Dumper

        # read selected solution file
        stream = file(os.getcwd() + '/' + self.SOLUTIONS_DIR + '/'
                      + solution_name + self.SOLUTION_FILE_EXT, 'r')

        data = load(stream, Loader=Loader)

        return data

    def run(self, solution_name):
        if 0 == len(solution_name):
            raise ValueError("'solution_name' must be not empty string")

        solution_data = self.get_solution_config_from_yaml(solution_name)

        print(solution_data)

        tasks_to_run = solution_data['taskler_solution']['tasks']
        inputed_data = solution_data['taskler_solution']['input_data']

        for task_to_run in tasks_to_run:
            # print "[ DEBUG ] task_to_run: " + task_to_run

            print('--- Input data for task "%s": "%s"' % (str(task_to_run), str(inputed_data)))

            outputed_data = None

            # run solution tasks
            tasks_provider = TasksProvider.TasksProvider()

            tasks_provider.set_verbose(solution_data['taskler_solution']['plugin_set_verbose'])

            tasks_provider.set_verbose(solution_data['taskler_solution']['task_set_verbose'])

            outputed_data = tasks_provider.run_tasks([str(task_to_run)], inputed_data)

            print('--- Task "%s" return output data: "%s"' % (str(task_to_run), str(outputed_data)))

            inputed_data = outputed_data

        print(outputed_data)


if __name__ == "__main__":
    # TODO: add run script with more inputed tasks
    if 1 < len(sys.argv):
        print('RunSolution start with argument: "%s"' % sys.argv[1])
        rs = RunSolution()
        rs.run(sys.argv[1])
    else:
        print('*** RunSolution script for taskler ***')
        print('--------------------------')
        print('Please run with existing solution name in argument, for example:')
        print('$ python RunSolution ExampleSolution' + "\n")
