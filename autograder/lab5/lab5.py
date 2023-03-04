from bs4 import BeautifulSoup
import os
import json
import traceback
import subprocess

class Lab5:
    def __init__(self, submissions_folder, submissions, debug=False) -> None:
        self.submissions_folder = submissions_folder
        self.submissions = submissions
        self.debug = debug
        self.file_obj = None

    def log_info(self, msg):
        print(msg)
    
    def log_debug(self, msg):
        if self.debug:
            print(msg)

    def start(self):
        with open('grades.csv', 'a') as g:
            g.write(",".join(["Name","dirStructurePoints","html","initializeContent","createUpdateEvents","updateDom","openEventModal","updateEventFromModal","updateTooltips","Comments\n"]))
        for submission in self.submissions:
            if os.path.isdir(os.path.join(self.submissions_folder, submission)):
                try:
                    self.log_info(f"Grading submission: {submission}")
                    proc = subprocess.Popen(f'node ./autograder/lab5/js-test/runner.js "{os.path.join(self.submissions_folder, submission)}" {submission}')
                    proc.wait()
                except Exception:
                    self.log_info(f"Exception occurred while grading {submission}")