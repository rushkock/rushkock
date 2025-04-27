from typing import List
from abc import ABC, abstractmethod
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

class Skills:
    def __init__(self, skill: str, type: int) -> None:
        self.skill = skill
        self.type = type

    def __str__(self):
        type = 'Soft-skill' if self.type == 0 else 'Hard-skill'
        return f"{self.skill} ({type})"
    
    def to_html(self):
        type = 'Soft-skill' if self.type == 0 else 'Hard-skill'
        return f"<span>{self.skill} <em style='color: gray;'>({type})</em></span>"

class Experience(ABC):
    def __init__(self, start_date: date, end_date: date = None, title: str = None, company: str = None, skills: List[Skills] = None, description: str = None, print_order: int = None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.company = company
        self.skills = skills
        self.description = description
        self.print_order = print_order

    def reorder_skills(self):
        ordered_skills = self.skills
        if ordered_skills and len(ordered_skills) > 1:
            ordered_skills = sorted(ordered_skills, key=lambda s: s.type)
        return ordered_skills

    def print_experiences(self):
        date_range = f"{self.start_date.strftime('%b %Y')} – "
        date_range += self.end_date.strftime('%b %Y') if self.end_date else "Present"
        exp_str = ''
        if self.title:
            exp_str += f"{self.title}  "
        exp_str += f"({date_range})"
        if self.description:
            exp_str += f"\n{self.description}"
        if self.skills:
            exp_str += "\nRelated skills:"
            ordered_skills = self.reorder_skills()
            for skill in ordered_skills:
                exp_str += f"\n    - {skill}"
        return exp_str

    @abstractmethod
    def __str__(self):
        pass

    def to_html(self):
        date_range = f"{self.start_date.strftime('%b %Y')} – "
        date_range += self.end_date.strftime('%b %Y') if self.end_date else "Present"
        html = ""
        if self.title:
            html += f"<h3 style='margin-bottom:5px;'>{self.title}</h3>"
        if self.company:
            html += f"<p style='margin:2px 0;color:gray;'>{self.company}</p>"
        html += f"<p style='font-size:small;color:gray;'>{date_range}</p>"
        if self.description:
            html += f"<p>{self.description}</p>"
        if self.skills:
            html += "<p><strong>Related skills:</strong></p><ul>"
            for skill in self.reorder_skills():
                html += f"<li>{skill.to_html()}</li>"
            html += "</ul>"
        html += "</div>"
        return html

class Job(Experience):
    def __init__(self, title: str, start_date: date, end_date: date = None, company: str = None, skills: List[Skills] = None, description: str = None) -> None:
        super().__init__(start_date, end_date, title, company, skills, description, print_order=0)

    def __str__(self):
        return '💼' + Experience.print_experiences(self)

    def to_html(self):
        return f"<div>{super().to_html()}</div>"

class Project(Experience):
    def __init__(self, start_date: date, title: str = None, end_date: date = None, company: str = None, skills: List[Skills] = None, description: str = None, project_title: str = None, project_link: str = None) -> None:
        super().__init__(start_date, end_date, title, company, skills, description, print_order=3)
        self.project_title = project_title
        self.project_link = project_link

    def __str__(self):
        str_top_level = '💻'
        if self.project_title:
            str_top_level += f"Title:{self.project_title}  "
        str_top_level += Experience.print_experiences(self)
        return str_top_level

    def to_html(self):
        old_title = self.title
        self.title = None
        proj_html = "<div>"
        if self.project_title:
            proj_html += f"<h3>Project: {self.project_title}</h3>"
            proj_html += super().to_html()
            if self.project_link:
                proj_html += f"<p>View Project <a href='{self.project_link}' target='_blank'>here</a></p>"        
        proj_html += "</div>"
        self.title = old_title
        return proj_html

class Course:
    def __init__(self, course_name: str, description: str = None) -> None:
        self.course_name = course_name
        self.description = description

    def __str__(self):
        course_str = f"{self.course_name}"
        if self.description:
            course_str += f":\n {self.description}"
        return course_str

    def to_html(self):
        if self.description:
            return f"<li>{self.course_name}: {self.description}</li>"
        return f"<li>{self.course_name}</li>"

class Education:
    def __init__(self, degree_level: str, start_date: date, university_name: str = None, study_name: str = None, end_date: date = None, gpa: float = None, thesis: Project = None, courses: List[Course] = None) -> None:
        self.degree_level = degree_level
        self.university_name = university_name
        self.study_name = study_name
        self.start_date = start_date
        self.end_date = end_date
        self.gpa = gpa
        self.courses = courses
        self.thesis = thesis

    def __str__(self):
        edu_str = f"{self.degree_level}"
        if self.start_date and self.end_date:
            edu_str += f" ({self.start_date.strftime('%Y')} - {self.end_date.strftime('%Y')})"
        if self.study_name:
            edu_str += f"\n{self.study_name}"
        if self.university_name:
            edu_str += f"\n{self.university_name}"
        if self.gpa:
            edu_str += f"\nGPA: {self.gpa}"
        if self.courses:
            edu_str += "\nSpecializations/Electives:"
            for course in self.courses:
                edu_str += f"\n    {course}"
        if self.thesis:
            edu_str += f"\nThesis:\n{self.thesis}"
        return edu_str

    def to_html(self):
        edu_html = f"<h2 style='margin-bottom:5px;'>🎓{self.degree_level}</h2>"
        if self.start_date and self.end_date:
            edu_html += f"<p style='font-size:small;color:gray;'>{self.start_date.strftime('%Y')} - {self.end_date.strftime('%Y')}</p>"
        if self.study_name:
            edu_html += f"<p><strong>{self.study_name}</strong></p>"
        if self.university_name:
            edu_html += f"<p>{self.university_name}</p>"
        if self.gpa:
            edu_html += f"<p>GPA: {self.gpa}</p>"
        if self.courses:
            edu_html += "<p><strong>Specializations/Electives:</strong></p><ul>"
            for course in self.courses:
                edu_html += course.to_html()
            edu_html += "</ul>"
        if self.thesis:
            edu_html += f"<div><strong>Thesis:</strong>{self.thesis.to_html()}</div>"
        edu_html += "</div>"
        return edu_html

class Internship(Experience):
    def __init__(self, title: str, start_date: date, associated_study: Education, end_date: date = None, company: str = None, skills: List[Skills] = None, description: str = None) -> None:
        super().__init__(start_date, end_date, title, company, skills, description, print_order=2)
        self.associated_study = associated_study

    def __str__(self):
        str_top_level = '💼' + Experience.print_experiences(self)
        str_top_level += f"\nAssociated study : {self.associated_study.study_name}"
        return str_top_level

    def to_html(self):
        return f"<div>{super().to_html()}<p>Associated study: {self.associated_study.study_name}</p></div>"

class Publications:
    def __init__(self, journal_name: str, title: str, doi: str, authors: List['Person']) -> None:
        self.journal_name = journal_name
        self.title = title
        self.doi = doi
        self.authors = authors

    def __str__(self):
        authors_list = ", ".join([author.name for author in self.authors])
        return f"  {self.title}.\n    {authors_list}\n    Published in {self.journal_name}\n    DOI: {self.doi}"

    def to_html(self):
        authors_list = ", ".join([author.name for author in self.authors])
        return f"<p><strong>{self.title}</strong><br><em>{authors_list}</em><br>Published in {self.journal_name}<br>DOI: <a href='https://doi.org/{self.doi}' target='_blank'>{self.doi}</a></p>"

class PhD(Experience):
    def __init__(self, title: str, start_date: date, end_date: date = None, company: str = None, skills: List[Skills] = None, description: str = None, publications: List[Publications] = None) -> None:
        super().__init__(start_date, end_date, title, company, skills, description, print_order=1)
        self.publications = publications

    def __str__(self):
        str_top_level = '💼' + Experience.print_experiences(self)
        if self.publications:
            str_top_level += "\n\n  📃Relevant Publications\n"
            for pub in self.publications:
                str_top_level += f"{pub}\n"
        return str_top_level

    def to_html(self):
        phd_html = f"<div>{super().to_html()}"
        if self.publications:
            phd_html += "<h4>📃 Relevant Publications</h4>"
            for pub in self.publications:
                phd_html += pub.to_html()
        phd_html += "</div>"
        return phd_html

class Person:
    def __init__(self, name: str, education: List[Education] = None, experience: List[Experience] = None, date_of_birth: date = None) -> None:
        self.name = name
        self.education = education
        self.experience = experience
        self.age = self.calculate_age(date_of_birth)

    def calculate_age(self, date_of_birth):
        if not date_of_birth:
            return None
        time_since_birth = relativedelta(datetime.now(), date_of_birth)
        return time_since_birth

    def __str__(self):
        output = f"👤 {self.name}"
        if self.age:
            output += f" ({self.age.years} Years Old)\n\n"
        else:
            output += f"\n\n"
        if self.education:
            output += "=== Education ===\n"
            for edu in self.education:
                output += f"{edu}\n\n"
        if self.experience:
            output += "=== Experience(s) ===\n"
            for exp in self.experience:
                output += f"{exp}\n\n"
        return output

    def to_html(self):
        html = f"<div><h1>👤 {self.name}</h1>"
        if self.age:
            html += f"<p>{self.age.years} Years Old</p>"
        if self.education:
            html += "<h1>🎓 Education</h1>"
            for edu in self.education:
                html += edu.to_html()
        if self.experience:
            html += "<h1>💼 Experience(s) </h1>"
            for exp in self.experience:
                html += exp.to_html()
        html += "</div>"
        return html

class CompareHelper:
    def __init__(self, type, date):
        self.type = type
        self.date = date

    def __lt__(self, other):
        if (self.type < other.type):
            return True
        elif (self.type == other.type and self.date < other.date):
            return True
        else:
            return False

    def __eq__(self, other):
        return self.type == other.type and self.date == other.date

def sort_objects(ordered_skills, sort_type, order):
    if sort_type:
        return sorted(ordered_skills, key=lambda s: CompareHelper(s.print_order, s.start_date), reverse=order)
    else:
        return sorted(ordered_skills, key=lambda s: s.start_date, reverse=order)