= Taskler overview =

*Taskler* is a simple _task manager_ for any frequently *tasks* written in Python.
It supports the creation of _complex tasks_ with the use of _specific and simple_ *plug-ins*.
Each plug-in has a certain interface and performs one small operations.
Each forward to the next queue plug-in plug-ins results for its action, so that it is possible to processing many information with many data transactions.
In future versions I would like to add some maybe parrallel, multiprocess and multithreading schedules. At the moment flow in solution is very simple to implementation and populating.

== Tasks ==

There are simple group for declaring required (used) plug-ins for proccess work.

![Taskler flow diagram](https://raw.githubusercontent.com/bieli/Taskler/master/docs/taskler_flow_diagram.png)


== Plug-ins ==

It is a small class plug-ins code for doing simple unique proccess in _run_ method.
It is waiting for input data from other plugins and serving outputs results for other plugins. Each plug-ins have dedicated inteface. In future mayby it will be _json_ but now it is a array, list data structure format.

=== Standard plug-ins description ===
 * fetch data from _url_
 * login in owa M$ e-mail web client
 * fetch all unreaded messages from owa M$ e-mail web client _recived emails_ page
 * get all links (url) with specyfic regular expression from inputed content
 * save data array in CSV file
 * load data array from CSV file
 * tray notification icon in GTK (gnome)
 * send emails with data with using simple templates system
 * get all links (url) for images with specyfic regular expression from inputed content


== Solutions ==

It is a group of tasks. We can create onededicated file in YAML format for our solution.
For example we need run My1Task (witch runs plugins Ex1Plugin and Ex2Plugin) and next 
run other task My2Task (witch runs plugins Ex3Plugin). All configured in simple text format:

{{{
takler_solution:
  task_set_verbose:   True
  plugin_set_verbose: True
  tasks:              
    - ExampleGetRandomDataTask
    - ExamplePrintsMessagesTask

  input_data:         [10, 20, 3, 11]
}}}

=== ExampleSolution run and output ===

$ python RunSolution.py ExampleSolution

RunSolution start with argument: "ExampleSolution"
{'takler_solution': {'input_data': [10, 20, 3, 11], 'plugin_set_verbose': True, 'tasks': ['ExampleGetRandomDataTask', 'ExamplePrintsMessagesTask'], 'task_set_verbose': True}}
--- Input data for task "ExampleGetRandomDataTask": "[10, 20, 3, 11]"
Searched tasks '['ExampleGetRandomDataTask']'
Found tasks '[]'
{<class 'ExampleGetRandomDataTask.ExampleGetRandomDataTask'>: <ExampleGetRandomDataTask ['task_run', 'task_set_verbose']>}
plugin verbose mode >> init from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> set_data from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> proccess from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> get_data_count from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> proccesed_data_length = "4"!
plugin verbose mode >> get_data from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> deinit from "ExampleGetRandomRangedDataTaskPlugin"!
--- Task "ExampleGetRandomDataTask" return output data: "[1, 13, 0, 4]"
--- Input data for task "ExamplePrintsMessagesTask": "[1, 13, 0, 4]"
Searched tasks '['ExamplePrintsMessagesTask']'
Found tasks '[]'
{<class 'ExamplePrintsMessagesTask.ExamplePrintsMessagesTask'>: <ExamplePrintsMessagesTask ['task_run', 'task_set_verbose']>, <class 'ExampleGetRandomDataTask.ExampleGetRandomDataTask'>: <ExampleGetRandomDataTask ['task_run', 'task_set_verbose']>}
plugin verbose mode >> init from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> init from "GetConfigProfilePlugin"!
plugin verbose mode >> init from "PrintHelloFromMethodsPlugin"!
plugin verbose mode >> set_data from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> proccess from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> get_data_count from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> proccesed_data_length = "4"!
plugin verbose mode >> get_data from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> set_data from "GetConfigProfilePlugin"!
plugin verbose mode >> proccess from "GetConfigProfilePlugin"!
plugin verbose mode >> get_data_count from "GetConfigProfilePlugin"!
plugin verbose mode >> proccesed_data_length = "4"!
plugin verbose mode >> get_data from "GetConfigProfilePlugin"!
plugin verbose mode >> set_data from "PrintHelloFromMethodsPlugin"!
plugin verbose mode >> proccess from "PrintHelloFromMethodsPlugin"!
plugin verbose mode >> get_data_count from "PrintHelloFromMethodsPlugin"!
plugin verbose mode >> proccesed_data_length = "4"!
plugin verbose mode >> get_data from "PrintHelloFromMethodsPlugin"!
plugin verbose mode >> deinit from "ExampleGetRandomRangedDataTaskPlugin"!
plugin verbose mode >> deinit from "GetConfigProfilePlugin"!
plugin verbose mode >> deinit from "PrintHelloFromMethodsPlugin"!
--- Task "ExamplePrintsMessagesTask" return output data: "[10, 50, 0, 20]"
[10, 50, 0, 20]

