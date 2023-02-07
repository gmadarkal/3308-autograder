from bs4 import BeautifulSoup
import os
import json

class Lab4:
    def __init__(self, submissions_folder, submissions, debug=False) -> None:
        self.submissions_folder = submissions_folder
        self.submissions = submissions
        self.files = ['index.html', 'projects.html', 'hobbies.html', 'resume.html']
        self.debug = debug
        self.file_obj = None
    
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
        navbar_icon = navbar_obj.find(id="navbar-icon")
        if navbar_icon:
            total_points += 1
        else:
            comments.append("-2: navbar icon missing")
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
            if count < 4:
                comments.append('navbar is missing links')

        return total_points, comments

    def grade_footer(self):
        total_points = 0
        comments = []

        footer_obj = self.file_obj.footer
        if not footer_obj:
            comments.append("-3: footer does not exist")
            return total_points, comments
        footer_links = footer_obj.find_all("a")
        if not footer_links:
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
        image = self.file_obj.find(id="hero_image")
        if image:
            total_points += 3
        else:
            comments.append("-3: Could not find image in home page")
        desc = self.file_obj.find(id="hero_desc")
        if desc:
            total_points += 3
        else:
            comments.append("-3: Could not find description in home page")

        return total_points, comments

    def grade_hobbies(self, quantity):
        total_points = 0
        comments = []
        # 1 point for including 
        # card image (0.5), 
        # card title (0.25), 
        # card desc (0.25)
        for i in range(quantity):
            hobby_card = self.file_obj.find(id=f"hobby_card{i}")
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
        
        return total_points

    def grade_projects(self, quantity):
        total_points = 0
        comments = []
        # 2 points per project 
            # card image (1), 
            # card title (0.5), 
            # card desc (0.5)
        # 4 points for indicators on carousel
        # 2 points for no. of projects
        if quantity >= 3:
            total_points += 2
        else:
            comments.append("-2: less than 3 projects added")
        projects_obj = self.file_obj.find(id="projects")
        bottom_indicators = projects_obj.find(id="carousel_bottom_indicators")
        buttons = bottom_indicators.findAll("button")
        if len(buttons) >= 3:
            total_points += 2
        else:
            comments.append('-2: carousel bottom indicators are not found')
        prev_control = projects_obj.find(id="carousel_control_prev")
        next_control = projects_obj.find(id="carousel_control_next")
        if prev_control:
            total_points += 1
        else:
            comments.append("-1: previous project indicator is not found")
        if next_control:
            total_points += 1
        else:
            comments.append("-1: next project indicator is not found")
        for i in range(quantity):
            carousel_item = projects_obj.find(id=f"carousel_item{i}")
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
                lib.get("href").index("materialize") > -1,
                lib.get("href").index("bulma") > -1,
                lib.get("href").index("uikit") > -1,
                lib.get("href").index("semantic") > -1
            ]
            if any(libs_found):
                total_points += 12
                css_lib_found = True
                break
        if not css_lib_found:
            comments.append("-12: did not use css libraries mentioned in the lab requirement")

        resume_obj = self.file_obj.find(id="resume")
        tables = resume_obj.findAll("table")
        if len(tables) > 0:
            total_points += 6
        else:
            comments.append("-6: did not use table for resume")

        return total_points, comments

    def grade(self, submission):
        with open('./rubric/lab4.json') as reader:
            rubric_contents = reader.read()
        graded_sections = []
        rubric = json.loads(rubric_contents)
        submission_remarks = []
        total_points = 0
        for section in rubric['lab4']:
            section_points, section_comments = 0, []
            self.log_debug(f'Grading section: {section}')
            self.log_debug(f'Grading common components section: {section}')
            for comp in section['common_components']:
                comp_points, comp_comments = eval(f"self.grade_{comp['component_id']}()")
                section_points += comp_points
                section_comments.extend(comp_comments)
            for sub_section in section['sub_sections']:
                graded_sections.append(f"{section['section_name']}_{sub_section['name']}")
                self.log_debug(f"grading subsection {sub_section['name']}, total points: {sub_section['points']}")
                sub_section_points, sub_section_comments = 0, []
                for item in sub_section['items']:
                    self.log_debug(f"grading item: {item['component_id']}, total points: {item['item_point']}")
                    item_points, item_comments = eval(f"self.grade_{item['component_id']}()")
                    sub_section_points += item_points
                    sub_section_comments.extend(item_comments)
            section_points += sub_section_points
            section_comments.extend(sub_section_comments)
        total_points += sub_section_points
        submission_remarks.extend(sub_section_comments)
    
        return total_points, submission_remarks, graded_sections

    def start(self):
        views_folder = 'Lab_Website/views/'
        grades = []
        for submission in self.submissions:
                total_points, submission_remarks, graded_sections = self.grade(submission)
                grades.append({
                    "name": submission,
                    "points": total_points,
                    "remarks": submission_remarks,
                    "graded_sections": graded_sections
                })
                
        return grades