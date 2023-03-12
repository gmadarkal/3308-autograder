import os
from autograder.lab4.lab4 import Lab4
from autograder.lab5.lab5 import Lab5
from autograder.lab7.lab7 import Lab7
from autograder.lab6.lab6 import Lab6
from autograder.reporter.csv_reporter import CSVReporter
from autograder.helpers.constants import lab6_columns

lab_number = int(input("Please enter lab number\n"))
sections_to_grade = []
submissions_folder = input(f"Please paste the folder containing all sections \n")
sections_to_grade = str(input("Please enter the sections you want to grade eg: 11,12,13 or enter 'a' to grade all sections \n"))
if sections_to_grade == 'a':
    sections = os.listdir(submissions_folder)
else:
    sections = sections_to_grade.split(",")

if lab_number == 4:
    for section in sections:
        if section != "grades":
            submissions = os.listdir(os.path.join(submissions_folder, section))
            print(f"Found {len(submissions)} in this section")
            lab4_obj = Lab4(os.path.join(submissions_folder, section), submissions)
            grades = lab4_obj.start()
            reporter = CSVReporter(submissions_folder, section)
            reporter.report(grades)
            print(f"Completed grading {len(submissions)} submissions in section {section}")
elif lab_number == 5:
    for section in sections:
        if section != "grades":
            submissions = os.listdir(os.path.join(submissions_folder, section))
            lab5_obj = Lab5(os.path.join(submissions_folder, section), submissions)
            grades = lab5_obj.start()
            print(f"Completed grading {len(submissions)} submissions in section {section}")
elif lab_number == 6:
    for section in sections:
        if section != "grades":
            submissions = os.listdir(os.path.join(submissions_folder, section))
            lab6_obj = Lab6(os.path.join(submissions_folder, section), submissions)
            grades = lab6_obj.start()
            reporter = CSVReporter(submissions_folder, section, lab6_columns)
            reporter.report(grades)
            print(f"Completed grading {len(submissions)} submissions in section {section}")
elif lab_number == 7:
    for section in sections:
        if section != "grades":
            submissions = os.listdir(os.path.join(submissions_folder, section))
            lab7_obj = Lab7(os.path.join(submissions_folder, section), [submissions[0]])
            grades = lab7_obj.start()
            reporter = CSVReporter(submissions_folder, section)
            reporter.report(grades)
            print(f"Completed grading {len(submissions)} submissions in section {section}")
else:
    print(f"Only lab 4,5,6,7 supported in the current version of autograde")