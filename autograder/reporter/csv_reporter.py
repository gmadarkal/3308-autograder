import os
class CSVReporter():
    def __init__(self, submission_folder, section, columns=None) -> None:
        self.submission_folder = submission_folder
        self.section = section
        self.columns = columns
    
    def clean(self, msg):
        if msg:
            return msg.replace(",", "; ").replace("\n", "; ")
        

    def report(self, grades):
        if not os.path.exists(os.path.join(self.submission_folder, "grades")):
            os.makedirs(os.path.join(self.submission_folder, "grades"), exist_ok=True)
        with open(os.path.join(self.submission_folder, "grades", f'grades_{self.section}.csv'), 'w') as writer:
            if self.columns:
                writer.write(f'{",".join(["; ".join([obj["title"], obj["desc"]]) for obj in self.columns])}\n')
            else:
                writer.write('Name,Points,Comments,error,error_msg\n')
        with open(os.path.join(self.submission_folder, "grades", f'grades_{self.section}.csv'), 'a') as writer:
            for grade in grades:
                if self.columns:
                    content = ""
                    for col in self.columns:
                        content += f"{grade[col['title']]}" + ","
                    content += "\n"
                    writer.write(content)
                else:
                    writer.write(f"{grade['name']},{grade['points']},{'; '.join(grade['remarks'])},{grade['error']},{self.clean(grade['error_msg'])}\n")