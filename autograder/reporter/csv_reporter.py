class CSVReporter():
    def __init__(self, submission_folder) -> None:
        self.submission_folder = submission_folder

    def report(self, grades):
        with open(f'{self.submission_folder}/grades.csv', 'a') as writer:
            writer.write('Name,Points,Comments\n')
            for grade in grades:
                writer.write(f"{grade['name']},{grade['[points']},{' '.join(grade['remarks'])}\n")