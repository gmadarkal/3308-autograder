import os
import mysql.connector
import sqlparse

class Lab6:
    def __init__(self, submissions_folder, submissions, debug=False) -> None:
        self.submissions_folder = submissions_folder
        self.submissions = submissions
        self.debug = debug
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
    
    def get_conn(self):
        if self.db.is_connected():
            return self.db
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="grading_db"
        )
        return self.db

    def log_info(self, msg):
        print(msg)
    
    def log_debug(self, msg):
        if self.debug:
            print(msg)

    def grade_create(self, path):
        total_points = 0
        comments = []
        errors = []
        try:
            with open(path) as sql_file:
                contents = sql_file.read()
            if contents and len(contents) > 5: 
                parsed_file = sqlparse.parse(contents)
                count = 0
                for query in parsed_file:
                    l_query = query.value.lower()
                    if "create table" in l_query:
                        query_validity = [
                            "movies_to_actors" in l_query,
                            "movies_to_genres" in l_query,
                            "movies" in l_query,
                            "actors" in l_query,
                            "genres" in l_query,
                            "platforms" in l_query,
                        ]
                        if any(query_validity):
                            total_points += 1.5
                        else:
                            count += 1
                if count > 0:
                    comments.append(f"-{(1.5 * count) + 1}: incorrect create query found")
                else:
                    total_points += 1
            else:
                comments.append("-10: incomplete create tables command")
        except Exception as e:
            comments.append("-10: incorrect create tables command")
            errors.append("Create commands: " + str(e))
        return total_points, comments, errors

    def grade_alter(self, path):
        total_points = 0
        comments = []
        errors = []
        try:
            with open(path) as sql_file:
                contents = sql_file.read()
            if contents and len(contents) > 5:
                parsed_file = sqlparse.parse(contents)
                alter_stmt = parsed_file[0]
                alter_stmt = alter_stmt.value.lower()
                query_validity = [
                    "alter" in alter_stmt,
                    "movies" in alter_stmt,
                    "foreign" in alter_stmt,
                    "platform_id" in alter_stmt,
                ]
                if all(query_validity):
                    total_points += 5
                else:
                    comments.append("-5: incorrect alter query")
            else:
                comments.append("-5: alter table command is not submitted or incorrect")
        except Exception as e:
            comments.append("-5: incorrect alter table command")
            errors.append("Alter commands: " + str(e))
        return total_points, comments, errors
    
    def grade_insert(self, path):
        total_points = 0
        comments = []
        errors = []
        with open(path, encoding="utf-8") as sql_file:
            contents = sql_file.read()
        statements = sqlparse.split(contents)
        if statements and len(statements) > 2:
            count = 0
            for statement in statements:
                if statement.startswith("insert"):
                    l_query = statement.lower()
                    query_validity = [
                        "insert into movies_to_actors" in l_query,
                        "insert into movies_to_genres" in l_query,
                        "insert into movies" in l_query,
                        "insert into actors" in l_query,
                        "insert into genres" in l_query,
                        "insert into platforms" in l_query,
                    ]
                    if not any(query_validity):
                        count += 1
            if count > 0:
                comments.append(f"-6: insert commands are incorrect")
            else:
                total_points += 6
        return total_points, comments, errors
    
    def grade(self, s_path):
        total_points = 0
        er_diagram_points = 0
        comments = []
        errors = []
        files_path = None
        try:
            img_files = os.listdir(os.path.join(s_path, "part_a", "img"))
            sql_files = os.listdir(os.path.join(s_path, "part_a", "sql"))
            files_path = os.path.join(s_path, "part_a", "sql")
        except:
            errors.append("dir structure is not followed, please verify the points once")
            img_files = os.listdir(s_path)
            sql_files = os.listdir(s_path)
            files_path = s_path
        l_img_files = []
        l_sql_files = []
        for file in img_files:
            l_img_files.append(file.lower())
        for file in sql_files:
            l_sql_files.append(file.lower())
        
        if 'er_diagram.png' in l_img_files:
            er_diagram_points += 5
        else:
            comments.append("-15: er diagram is missing in the submission")

        if 'insert.png' in l_img_files:
            total_points += 1.5
        else:
            comments.append("-1.5: insert.png is missing in the submission")

        png_files_to_check = ['create.png', 'alter.png']

        for f in png_files_to_check:
            if f in l_img_files:
                total_points += 2.5
            else:
                comments.append(f"-2.5: file {f} is missing in the submission")
        
        sql_files = ['create', 'alter', 'insert']
        for s_file in sql_files:
            p_points = 0
            p_comments = [] 
            p_errors = []
            if f'{s_file}.sql' in l_sql_files:
                total_points += 2.5
                f_path = os.path.join(files_path, f"{s_file}.sql")
                f_path = f_path.replace("\\", "\\\\")
                p_points, p_comments, p_errors = eval(f'self.grade_{s_file}("{f_path}")')
            else:
                comments.append(f"-2.5: file {s_file}.sql is missing in the submission")
            total_points += p_points
            comments.extend(p_comments)
            errors.extend(p_errors)
        
        return total_points, er_diagram_points, comments, errors

    def start(self):
        grades = []
        for submission in self.submissions:
            if os.path.isdir(os.path.join(self.submissions_folder, submission)):
                try:
                    self.log_info(f"grading submission: {submission}")
                    points, er_diagram_points, comments, errors = self.grade(os.path.join(self.submissions_folder, submission))
                    grades.append({
                        "Name": submission,
                        "Part_A": points,
                        "ER_Diagram_1": er_diagram_points,
                        "ER_Diagram_2": "",
                        "Part_B": "",
                        "Total": "",
                        "Comments": "; ".join(comments),
                        "Errors": "; ".join(errors).replace(",", "; ").replace("\n", "; ")
                    })
                except Exception as e:
                    self.log_info(f"Exception occurred while grading {submission}" + str(e))
                    grades.append({
                        "Name": submission,
                        "Part_A": 0,
                        "ER_Diagram_1": 0,
                        "ER_Diagram_2": "",
                        "Part_B": "",
                        "Total": "",
                        "Comments": "",
                        "Errors": str(e).replace(",", "; ").replace("\n", "; ")
                    })
        return grades
                    