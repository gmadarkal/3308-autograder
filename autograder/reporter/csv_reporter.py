import os
class CSVReporter():
    def __init__(self, submission_folder) -> None:
        self.submission_folder = submission_folder
    
    def clean(self, msg):
        if msg:
            return msg.replace(",", ";").replace("\n", ";")
        

    def report(self, grades):
        with open(os.path.join(self.submission_folder, 'grades.csv'), 'w') as writer:
            writer.write('Name,Points,Comments,error,error_msg\n')
        with open(os.path.join(self.submission_folder, 'grades.csv'), 'a') as writer:
            for grade in grades:
                writer.write(f"{grade['name']},{grade['points']},{' '.join(grade['remarks'])},{grade['error']},{self.clean(grade['error_msg'])}\n")