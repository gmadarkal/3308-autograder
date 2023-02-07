import os
from autograder.lab4.lab4 import Lab4
from autograder.reporter.csv_reporter import CSVReporter

lab_number = int(input("Please enter lab number"))
section_number = input("Please enter section number")
submissions_folder = input(f"Please paste the folder containing submissions for section: {section_number}")

submissions = os.listdir(submissions_folder)

if lab_number == 4:
    lab4_obj = Lab4(submissions_folder, submissions)
    grades = lab4_obj.start()
    reporter = CSVReporter(submissions_folder)
    reporter.report(grades)
    print(f"Completed grading section {section_number}")

