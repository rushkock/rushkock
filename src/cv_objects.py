from typing import List
from abc import ABC, abstractmethod
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from typing import List,Union
from abc import ABC, abstractmethod
#from dateutil.relativedelta import relativedelta
#from datetime import date, datetime

class Skills:
    """ Define a skills
    
        - skill (str): Name of the skill.
        - type (int): Type of skill; 0 = soft skill, 1 = hard skill.
    """
    def __init__(self, skill: str, type: int) -> None:
        self.skill = skill
        self.type = type

    def __str__(self):
        """Return a string representation of the skill."""
        type = 'Soft-skill' if self.type == 0 else 'Hard-skill'
        return f"{self.skill} ({type})"

    def to_html(self):
        """Return an HTML-formatted representation of the skill."""
        type = 'Soft-skill' if self.type == 0 else 'Hard-skill'
        return f"<span>{self.skill} <em style='color: gray;'>({type})</em></span>"

class Experience(ABC):
    """ Abstract base class for different types of professional experiences.
    
        - start_date: The start date of the experience.
        - end_date: The end date of the experience.
        - title: Job or project title.
        - company: Name of the company or organization.
        - skills: Associated skills from Skills class.
        - description: Description of the experience.
        - print_order: Order used for sorting output.
    """
    def __init__(self, start_date: date, end_date: date = None, title: str = None, company: str = None, skills: List[Skills] = None, description: str = None, print_order: int = None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.company = company
        self.skills = skills
        self.description = description
        self.print_order = print_order

    def reorder_skills(self):
        """Group hard and soft skills together"""
        ordered_skills = self.skills
        if ordered_skills and len(ordered_skills) > 1:
            ordered_skills = sorted(ordered_skills, key=lambda s: s.type)
        return ordered_skills

    def print_experiences(self):
        """Return a string representation of the experience."""
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
                exp_str += f"\n    -{skill}"
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
    """ Represents a professional job experience.
    
        All arguments same as class Experience
    """
    def __init__(self, title: str, start_date: date, end_date: date = None, company: str = None, skills: List[Skills] = None, description: str = None) -> None:
        super().__init__(start_date, end_date, title, company, skills, description, print_order=0)

    def __str__(self):
        return '💼' + Experience.print_experiences(self)

    def to_html(self):
        return f"<div>{super().to_html()}</div>"

class Project(Experience):
    """ Represents a project experience.
    
        - project_title: Display name of the project.
        - project_link: URL to the project.
        - See Class experience for the rest of the arguments
    """
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
        return f"<p>🏠 {self.address}, {self.city}, {self.postal_code}, {self.region}, {self.country}</p>"


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
    """ Represents a single course,specialization or elective.
    
        - course_name: Name of the course.
        - description: Short description.
    """
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
    """Represents an educational degree or program.
    
        - degree_level: Level of the degree (e.g., Bachelor's).
        - start_date: Program start date.
        - university_name: Name of the institution.
        - study_name: Program name.
        - end_date: Program end date.
        - gpa: GPA achieved.
        - thesis: Project object, if applicable.
        - courses: Relevant courses as Course objects.
    """
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
                edu_str += f"\n    -{course}"
        if self.thesis:
            edu_str += f"\nThesis:\n{self.thesis}"
        return edu_str

    def to_html(self):
        edu_html = f"<h2 style='margin-bottom:5px;'>{self.degree_level}</h2>"
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
    """ Represents an internship experience
    
        - associated_study : Education Object representing the associated instituion where the internship whose curriculum the internship was a part of
        - See Class experience for the rest of the arguments
    """
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
    """Represents an academic publication.
    
        - journal_name: Name of the journal.
        - title: Title of the publication.
        - doi: DOI / URL.
        - authors: List of author names as Person.
    """
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
    """ Represents a PhD education experience.

        - publications: List of academic publications as Publications objects
        - See Class experience for the rest of the arguments
    """
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

class Address:
    """ Represents personal address
    
        - address: Street name and number
        - postal_code: Postal or ZIP code
        - city: City name
        - country: Country name
        - region: Region or state
    """
    def __init__(self, address:str, postal_code:str, city:str, country:str, region:str):
        self.address = address
        self.postal_code = postal_code
        self.city =city
        self.country = country
        self.region = region

    def __str__(self):
        output = f"🏠{self.address},{self.city},{self.postal_code},{self.region},{self.country}"
        return output
    def to_html(self):
        return f"<p>🏠 {self.address}, {self.city}, {self.postal_code}, {self.region}, {self.country}</p>"

class Socials:
    """ Social media or online profile.
    
        - type: Name of the platform (e.g., LinkedIn, GitHub)
        - link: URL to the profile
    """
    def __init__(self,type:str,link:str):
        self.type = type
        self.link = link
    def __str__(self):
        return f"{self.type} : {self.link}"
    def to_html(self):
        return f"<li><strong>{self.type}</strong>: <a href='{self.link}' target='_blank'>{self.link}</a></li>"


class Contact_info:
    """ Contact information including address, phone number and socials.
    
        - email: Email address
        - phone_number: phone number with area code (e.g. `+890555555`)
        - website: URL to personal or professional website
        - address: Address object
        - socials: List of Socials objects
    """
    def __init__(self,email:str,phone_number:int=None,website:str=None, address:Address=None, socials:List[Socials]=None):
        self.email = email
        self.phone_number = phone_number
        self.url = website
        self.address = address
        self.socials = socials
    def __str__(self):
        output = f"📧{self.email}"
        if self.phone_number:
            output += f"\n📱{self.phone_number}"
        if self.url:
            output += f"\n🔗{self.url}"
        if self.address:
            output += f"\n{self.address}"
        if self.socials:
            output += f'\n📶Follow me on:'
            for social in self.socials:
               output += f"\n   -{social}" 
        return output
    def to_html(self):
        html = f"<p>📧 {self.email}</p>"
        if self.phone_number:
            html += f"<p>📱 {self.phone_number}</p>"
        if self.url:
            html += f"<p>🔗 <a href='{self.url}' target='_blank'>{self.url}</a></p>"
        if self.address:
            html += self.address.to_html()
        if self.socials:
            html += "<p>📶 Follow me on:</p><ul>"
            for social in self.socials:
                html += social.to_html()
            html += "</ul>"
        return html

class Interests:
    """ Add personal interests such as hobbies or experience unrelated interests
    
        - name: Name of the interest
        - description: Short description of the interest
    """
    def __init__(self,name:str,description:str=None):
        self.name = name
        self.description = description
    def __str__(self):
        output = f"   -{self.name}"
        if self.description:
            output += f": {self.description}"
        return output
    def to_html(self):
        if self.description:
            return f"<li>{self.name}: {self.description}</li>"
        return f"<li>{self.name}</li>"


class Certificates:
    """ Initialize a Certificate.
    
        - title: Title of the certificate
        - description: Description of the certificate content
        - date: Issuance date of the certificate
        - url: URL to verify or view the certificate
        - issuer: Issuing organization
    """
    def __init__(self,title:str,description:str,date:date,url:str=None,issuer:str=None):
        self.title = title
        self.description = description
        self.date = date
        self.url = url 
        self.issuer = issuer
    def __str__(self):
        output = f"{self.title}({self.date.strftime('%m/%Y')})\n{self.description}"
        if self.url:
            output += f"\nLink: {self.url}"
        if self.issuer:
            output += f"\nIssuer: {self.issuer}"
        return output
    def to_html(self):
        html = f"<div><h3>{self.title} <span style='font-size:small;color:gray;'>({self.date.strftime('%b %Y')})</span></h3>"
        html += f"<p>{self.description}</p>"
        if self.url:
            html += f"<p>🔗 <a href='{self.url}' target='_blank'>Certificate Link</a></p>"
        if self.issuer:
            html += f"<p><strong>Issuer:</strong> {self.issuer}</p>"
        html += "</div>"
        return html

class Person:
    """ Initialize a Person object representing a person and their complete professional profile.
    
        - name: Full name of the person
        - education: List of Education entries
        - experience: List of Experience entries (Job, Internship, Project, etc.)
        - date_of_birth: Date of birth for age calculation
        - summary: Brief personal or professional summary
        - contact: Contact_info object
        - interests: List of Interests
        - certificates: List of Certificates
    """
    def __init__(self, name:str, education:List[Education]=None, experience:List[Experience]=None, date_of_birth:date=None, summary:str=None, contact:Contact_info=None, interests:List[Interests]=None, certificates:List[Certificates]=None) -> None:
        self.name = name
        self.education = education
        self.experience = experience
        self.summary = summary
        self.date_of_birth = date_of_birth
        self.age = self.calculate_age(self.date_of_birth)           
        self.contact = contact
        self.interests = interests
        self.certificates = certificates

    def calculate_age(self, date_of_birth:Union[date,None]):
        if not date_of_birth:
           return None 
        return relativedelta(datetime.now(), date_of_birth)       

    def __str__(self):
        output = f"👤 {self.name}"
        if self.age:
            output += f" ({self.age.years} Years Old)\n"
        else:
            output += f"\n"
        if self.summary:
            output += f"{self.summary}\n"
        if self.contact:
            output += f"\n=== Contact Me ===\n"
            output += f"{self.contact}\n"
        if self.interests:
            output += f"\n=== Interests ===\n"
            for inter in self.interests:
                output += f"{inter}\n"
        if self.education:
            output += "\n=== Education ===\n"
            for edu in self.education:
                output += f"{edu}\n\n"
        if self.experience:
            output += "\n=== Experience(s) ===\n"
            for exp in self.experience:
                output += f"{exp}\n\n"
        if self.certificates:
            output += "\n=== Certificates ===\n"
            for cert in self.certificates:
                output += f"{cert}\n"
        return output

    def to_html(self):
        html = f"<div><h1>👤 {self.name}</h1>"
        if self.summary:
            html += f"<p>{self.summary}</p>"
        if self.age:
            html += f"<p>{self.age.years} Years Old</p>"
        if self.contact:
            html += self.contact.to_html()
        if self.education:
            html += "<h1>🎓 Education</h1>"
            for edu in self.education:
                html += edu.to_html()
        if self.experience:
            html += "<h1>💼 Experience(s) </h1>"
            for exp in self.experience:
                html += exp.to_html()
        if self.certificates:
            html += "<h1>🏅 Certificate(s) </h1>"
            for cert in self.certificates:
                html += cert.to_html()
        if self.interests:
            html += "<h1>🎮 Interest(s) </h1>"
            for inter in self.interests:
                html += inter.to_html()
        html += "</div>"
        return html

class CompareHelper:
    """Helper function to sort by type then date"""
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
    """ Reorder Objects by date and type or date starting from current date"""
    if sort_type:
        return sorted(enumerate(ordered_skills), key=lambda s: CompareHelper(s[1].print_order, s[1].start_date), reverse=order)
    else:
        return sorted(enumerate(ordered_skills), key=lambda s: s[1].start_date, reverse=order)