# -*- coding: utf-8 -*-

from TasksProvider import TasksProvider
import sys, os

class RunSolution():
    solutions_dir = 'solutions'
    solution_file_ext = '.yml'

    def __init__(self, solutions_dir = 'solutions'):
        if self.solutions_dir <> solutions_dir:
            self.solutions_dir = solutions_dir

    def get_solution_config_from_yaml(self, solution_name):

        # read yaml solution configuration
        from yaml import load, dump
        try:
            from yaml import CLoader as Loader
            from yaml import CDumper as Dumper
        except ImportError:
            from yaml import Loader, Dumper

        # read selected solution file
        stream = file(os.getcwd() + '/' + self.solutions_dir + '/'\
                      + solution_name + self.solution_file_ext, 'r')

        data = load(stream, Loader=Loader)

        return data

    def run(self, solution_name):
        if 0 == len(solution_name):
            raise ValueError, "'solution_name' must be not empty string"

        solution_data = self.get_solution_config_from_yaml(solution_name)

        print solution_data

        tasks_to_run  = solution_data['takler_solution']['tasks']

        inputed_data = solution_data['takler_solution']['input_data']

        for task_to_run in tasks_to_run:
#            print "[ DEBUG ] task_to_run: " + task_to_run

            print '--- Input data for task "%s": "%s"' % (str(task_to_run), str(inputed_data))

            outputed_data = None

            # run solution tasks
            tasks_provider = TasksProvider()

            tasks_provider.plugin_set_verbose(\
                    solution_data['takler_solution']['plugin_set_verbose'])

            tasks_provider.task_set_verbose(\
                    solution_data['takler_solution']['task_set_verbose'])

            outputed_data = tasks_provider.run_tasks([ str(task_to_run) ], inputed_data)

            print '--- Task "%s" return output data: "%s"' % (str(task_to_run), str(outputed_data))

            inputed_data = outputed_data

        print outputed_data

if __name__ == "__main__":
    #TODO: add run script with more inputed tasks
    if 1 < len(sys.argv):
        print 'RunSolution start with argument: "%s"' % sys.argv[1]
        rs = RunSolution()
        rs.run(sys.argv[1])
    else:
        print '*** RunSolution script for taskler ***'
        print '--------------------------'
        print 'Please run with existing solution name in argument, for example:'
        print '$ python RunSolution ExampleSolution' + "\n"

