# Grading Automation Script

This script offers a command line interface. When initiated the scripts requires a lab section folder path (eg: "c://lab4/012/") as input.
For more information on the rubric and automation script please look at file html-testing-automation.py

## Running the script

python runner.py

``` Please enter lab number ```

4

``` Please enter section number, eg: 012 ```

011

``` Please paste the folder containing the submissions ```

c://lab4/012/

```
Found 45 submissions in the folder.

Grading submission 1: Name: Gaurav Madarkal

Total score: 70/100
.

.

.

.

.

.

.

Grading for section 011 completed
```

A grades.csv file is generated in the same section folder

grades.csv file structure

| Name | Points | Comments | error | error_msg |
| ------ | ------ | ------ | ------ | ------ |