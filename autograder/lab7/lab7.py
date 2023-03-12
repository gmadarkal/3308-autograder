from bs4 import BeautifulSoup
import os
import json
import traceback
import subprocess
import requests

class Lab7:
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
        # with open(os.path.join(self.submissions_folder,'grades.csv'), 'a') as g:
        #     g.write(",".join(["Name","dirStructurePoints: 5pts","html: 5pts","initializeContent: 10pts","createUpdateEvents: 10pts","updateDom: 10pts","openEventModal: 10pts","updateEventFromModal: 10pts","updateTooltips: 20pts","Attendance","Total","Comments", "Errors\n"]))
        for submission in self.submissions:
            if os.path.isdir(os.path.join(self.submissions_folder, submission)):
                try:
                    self.log_info(f"Grading submission: {submission}")
                    print(f'changin path to cd "{os.path.join(self.submissions_folder, submission)}"')
                    os.chdir(os.path.join(self.submissions_folder, submission))
                    # cd_proc = subprocess.Popen(f'cd "{os.path.join(self.submissions_folder, submission)}"')
                    # cd_proc.wait()
                    proc = subprocess.Popen(f'npm install', shell=True)
                    proc.wait()
                    with open(os.path.join(self.submissions_folder, submission, ".env"), 'w') as env_file:
                        env_file.write("POSTGRES_USER='postgres'\nPOSTGRES_PASSWORD='pwd'\nPOSTGRES_DB='hiking_db'")
                    server_proc = subprocess.Popen(f'docker-compose -f "{os.path.join(self.submissions_folder, submission, "docker-compose.yaml")}" up', stdout=subprocess.PIPE, universal_newlines=True)
                    for stdout_line in iter(server_proc.stdout.readline, ""):
                        # print("This is from stdout:", stdout_line)
                        if stdout_line and "listening on port 3000" in str(stdout_line):
                            print("server has started")
                            res =  requests.get("http://localhost:3000")
                            print(res)
                            server_proc.kill()
                            break
                except Exception:
                    self.log_info(f"Exception occurred while grading {submission}" + traceback.format_exc())