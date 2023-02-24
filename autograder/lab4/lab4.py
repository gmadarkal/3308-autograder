from bs4 import BeautifulSoup
import os
import json
import traceback
from .constants import COMPONENT_IDS

class Lab4:
    def __init__(self, submissions_folder, submissions, debug=False) -> None:
        self.submissions_folder = submissions_folder
        self.submissions = submissions
        self.files = ['index.html', 'projects.html', 'hobbies.html', 'resume.html']
        self.debug = debug
        self.file_obj = None
        self.views_folder = "Lab_Website\\views"
    
    def log_info(self, msg):
        print(msg)
    
    def log_debug(self, msg):
        if self.debug:
            print(msg)
        
    def grade_navbar(self):
        total_points = 0
        comments = []
        navbar_obj = self.file_obj.nav
        if not navbar_obj:
            comments.append("-5: navbar is missing")
            return total_points, comments
        total_points += 2
        navbar_icon = navbar_obj.find(id=COMPONENT_IDS.get("NAVBAR_ICON", ""))
        if navbar_icon:
            total_points += 1
        else:
            comments.append("-1: navbar icon missing")
        navbar_links = navbar_obj.find_all("li")
        pages = ['index.html', 'hobbies.html', 'projects.html', 'resume.html']
        relative_pages = ['./index.html', './hobbies.html', './projects.html', './resume.html']
        alternate_page_values = ['#']
        try:
            count = 0
            for link in navbar_links:
                if link.a.get('href').lower() not in pages and link.a.get('href').lower() not in relative_pages:
                    comments.append('navbar is missing links')
                else:
                    count += 1
                    total_points += 0.5
        except:
            self.log_debug("exception occured while grading navbar. Proabaly a tag is missing. Requires further inspection of file")
        
        if count < 4:
            comments.append(f'-{(4-count)*0.5}: navbar is missing links')

        return total_points, comments

    def grade_footer(self):
        total_points = 0
        comments = []

        footer_obj = self.file_obj.footer or self.file_obj.find(id=COMPONENT_IDS.get("FOOTER", ""))
        if not footer_obj:
            footer_res = self.file_obj.find_all('div', { "class": "footer" })
            if footer_res:
                footer_obj = footer_res[0]
            else:
                comments.append("-3: footer does not exist")
                return total_points, comments
        footer_links = footer_obj.find_all("a")
        if len(footer_links) == 0:
            comments.append("-3: footer has no links")
        
        total_points += 1
        link_found = False
        for link in footer_links:
            link_val = link.get('href')
            if link_val and link_val.lower() != '#':
                link_found = True
        if link_found:
            total_points += 2
            return total_points, comments
        
        comments.append("-2: no valid links found in footer")
        return total_points, comments

    def grade_homepage(self):
        total_points = 0
        comments = []
        image = self.file_obj.find(id=COMPONENT_IDS.get("SELF_IMAGE", ""))
        if image:
            total_points += 3
        else:
            comments.append("-3: Could not find image in home page")
        desc = self.file_obj.find(id=COMPONENT_IDS.get("SELF_DESC", ""))
        if desc:
            total_points += 3
        else:
            comments.append("-3: Could not find description in home page")

        return total_points, comments

    def grade_hobbies(self):
        total_points = 0
        comments = []
        # 1 point for including 
        # card image (0.5), 
        # card title (0.25), 
        # card desc (0.25)
        for i in range(3):
            hobby_card = self.file_obj.find(id=f'{COMPONENT_IDS.get("HOBBY_CARDS_PREFIX", "")}{i+1}')
            if not hobby_card:
                comments.append(f"-1: hobby card {i+1} is missing")
                continue
            card_img = hobby_card.find('img')
            if card_img:
                total_points += 0.5
            else:
                comments.append("-0.5: hobby card image not found")
            # TODO: validate img path is valid or not
            heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']
            card_title = hobby_card.find_all(heading_tags)
            if len(card_title) > 0:
                total_points += 0.25
            else:
                comments.append("-0.25: hobby title not found")
            card_desc = hobby_card.find("p")
            if not card_desc:
                card_desc = hobby_card.find("span")
            if card_desc:
                total_points += 0.25
            else:
                comments.append("-0.25: hobby desc not found")
        
        return total_points, comments

    def grade_projects(self):
        total_points = 0
        comments = []
        # 2 points per project 
            # card image (1), 
            # card title (0.5), 
            # card desc (0.5)
        # 4 points for indicators on carousel
        # 2 points for no. of projects
        projects_obj = self.file_obj.find(id=COMPONENT_IDS.get("PROJECTS_CONTAINER", ""))
        if not projects_obj:
            obj = self.file_obj.find_all("div", {"class": "projects"})
            if len(obj) > 0:
                projects_obj = obj[0]
            if not projects_obj:
                comments.append("-12: projects div not found")
                return total_points, comments
        project_items = projects_obj.find_all("div", {"class": "carousel-item"})
        quantity = len(project_items)
        if len(project_items) >= 3:
            total_points += 2
        else:
            comments.append("-2: less than 3 projects added")
        bottom_indicators = projects_obj.find(id=COMPONENT_IDS.get("CAROUSEL_BTM_INDS", ""))
        buttons = bottom_indicators.find_all("button")
        if len(buttons) >= 3:
            total_points += 2
        else:
            comments.append('-2: carousel bottom indicators are not found')
        prev_control = projects_obj.find(id=COMPONENT_IDS.get("CAROUSEL_CONTROL_PREV", ""))
        next_control = projects_obj.find(id=COMPONENT_IDS.get("CAROUSEL_CONTROL_NEXT", ""))
        if prev_control:
            total_points += 1
        else:
            comments.append("-1: previous project indicator is not found")
        if next_control:
            total_points += 1
        else:
            comments.append("-1: next project indicator is not found")
        for i in range(quantity):
            carousel_item = projects_obj.find(id=f'{COMPONENT_IDS.get("CAROUSEL_ITEM_PREFIX", "")}{i+1}')
            card_img = carousel_item.find('img')
            if card_img:
                total_points += 1
            else:
                comments.append("-1: project image is not found")

            # TODO: validate img path is valid or not
            heading_tags = ["h1", "h2", "h3", 'h4', 'h5', 'h6']
            card_title = carousel_item.find_all(heading_tags)
            if len(card_title) > 0:
                total_points += 0.5
            else:
                comments.append("-0.5: project title is not found")
            card_desc = carousel_item.find("p")
            if not card_desc:
                card_desc = carousel_item.find("span")
            if card_desc:
                total_points += 0.5
            else:
                comments.append("-0.5: project desc is not found")

        return total_points, comments
            
    def grade_resume(self):
        # check css libraries
        # look for these keywords
        # 1. materialize
        # 2. bulma
        # 3. uikit
        # 4. semantic
        total_points = 0
        comments = []
        css_libs = self.file_obj.find_all("link")
        css_lib_found = False
        for lib in css_libs:
            libs_found = [
                "materialize" in lib.get("href"),
                "bulma" in lib.get("href"),
                "uikit" in lib.get("href"),
                "semantic" in lib.get("href")
            ]
            if any(libs_found):
                total_points += 12
                css_lib_found = True
                break
        if not css_lib_found:
            comments.append("-12: did not use css libraries mentioned in the lab requirement")

        resume_obj = self.file_obj.find(id=COMPONENT_IDS.get("RESUME", ""))
        if not resume_obj:
            obj = self.file_obj.find_all("div", {"class": "resume"})
            if len(obj) == 0:
                comments.append("-6: resume div not found")
                return total_points, comments
            resume_obj = obj[0]
        tables = resume_obj.find_all("table")
        if len(tables) > 0:
            total_points += 6
        else:
            comments.append("-6: did not use table for resume")

        return total_points, comments

    def get_submission_file_obj(self, submission, sub_section_name):
        file_path = os.path.join(self.submissions_folder, submission, self.views_folder, sub_section_name)
        with open(file_path, encoding='utf8') as html_file:
            file_contents = html_file.read()
        file_obj = BeautifulSoup(file_contents, 'html.parser')
        return file_obj

    def grade(self, submission):
        rubric_path = './autograder/lab4/rubric/lab4.json'
        with open(os.path.abspath(rubric_path)) as reader:
            rubric_contents = reader.read()
        graded_sections = []
        rubric = json.loads(rubric_contents)
        submission_remarks = []
        total_points = 0
        for section in rubric['lab4']:
            section_points = 0
            section_comments = []
            self.log_debug(f'Grading section: {section}')
            self.log_debug(f'Grading common components section: {section}')
            for sub_section in section['sub_sections']:
                graded_sections.append(f"{section['section_name']}_{sub_section['name']}")
                self.log_debug(f"grading subsection {sub_section['name']}, total points: {sub_section['points']}")
                sub_section_points = 0
                sub_section_comments = []
                self.file_obj = self.get_submission_file_obj(submission, sub_section['name'])
                for item in sub_section['items']:
                    self.log_debug(f"grading item: {item['component_id']}, total points: {item['item_point']}")
                    # if sub_section['name'] == 'hobbies.html':
                    #     print("soemthing")
                    item_points, item_comments = eval(f"self.grade_{item['component_id']}()")
                    sub_section_points += item_points
                    sub_section_comments.extend(item_comments)
                details = [f"[Section: {section['section_name']} Subsection: {sub_section['name']}]"]
                section_points += sub_section_points
                if len(sub_section_comments) > 0:
                    section_comments.extend(details)
                    section_comments.extend(sub_section_comments)
            total_points += section_points
            submission_remarks.extend(section_comments)
    
        return total_points, submission_remarks, graded_sections

    def start(self):
        grades = []
        for submission in self.submissions:
            if os.path.isdir(os.path.join(self.submissions_folder, submission)):
                try:
                    self.log_info(f"Grading submission: {submission}")
                    total_points, submission_remarks, graded_sections = self.grade(submission)
                    self.log_info(f"Total score for student: {submission} = {total_points}/100")
                    grades.append({
                        "name": submission,
                        "points": total_points,
                        "remarks": submission_remarks,
                        "graded_sections": graded_sections,
                        "error": False,
                        "error_msg": None
                    })
                except FileNotFoundError:
                    self.log_info(f"Submission file not found for: {submission}")
                    grades.append({
                        "name": submission,
                        "points": 0,
                        "remarks": [],
                        "graded_sections": {},
                        "error": True,
                        "error_msg": f"Submission file not found for: {submission}"
                    })
                except Exception:
                    self.log_info(f"Exception occurred while grading {submission}")
                    grades.append({
                        "name": submission,
                        "points": 0,
                        "remarks": [],
                        "graded_sections": {},
                        "error": True,
                        "error_msg": traceback.format_exc()
                    })
                
        return grades