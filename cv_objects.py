from typing import List
from abc import ABC, abstractmethod
from dateutil.relativedelta import relativedelta
from datetime import date,datetime

class Skills:
    def __init__(self, skill:str,type:int) -> None:
        self.skill = skill 
        self.type = type 
    def __str__(self):
        type= 'Soft-skill' if self.type == 0 else 'Hard-skill' 
        return f"{self.skill} ({type})"

class Experience(ABC):
    """ Collect any professional experiences including internships, employment or projects
        start_date = Start date 
        end_date = End date, if None then still ongoing
        title = Function e.g. Developer
        company = Associated company  
        skills = Most relevant skills acquired with the experience
        description = Description of the main tasks performed
    """
    def __init__(self, start_date:date, end_date:date=None,title:str=None, company:str=None, skills:List[Skills]=None, description:str=None,print_order:int=None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.title = title
        self.company = company
        self.skills = skills   
        self.description = description
        self.print_order = print_order
        
    def reorder_skills(self):
        ordered_skills = self.skills
        if len(ordered_skills)>1:
            ordered_skills = sorted(ordered_skills,key=lambda s: s.type)
        return ordered_skills
        
    def print_experiences(self):
        date_range = f"{self.start_date.strftime('%b %Y')} – "
        date_range += self.end_date.strftime('%b %Y') if self.end_date else "Present"
        exp_str = ''
        if self.description:
            exp_str = f"{self.title}  "
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

class Job(Experience):    
    def __init__(self, title:str, start_date:date, end_date:date=None, company:str=None, skills:List[Skills]=None, description:str=None) -> None:
        super().__init__(start_date,end_date,title, company, skills, description,print_order=0)
    def __str__(self):  
        str_top_level = '💼' + Experience.print_experiences(self)        
        return str_top_level

class Project(Experience):
    def __init__(self, start_date:date, title:str=None, end_date:date=None, company:str=None, skills:List[Skills]=None, description:str=None, project_title:str=None,project_link:str=None) -> None:
        super().__init__(start_date,end_date,title, company, skills, description,print_order=3)
        # specific title of the project
        self.project_title = project_title
        self.project_link = project_link
        
    def __str__(self): 
        str_top_level = '💻' 
        if self.project_title:
            str_top_level += f"Title:{self.project_title}  "
        str_top_level += Experience.print_experiences(self)        
        return str_top_level

class Course:
    def __init__(self,course_name:str,description:str=None) -> None:
        self.course_name = course_name
        self.description = description
    def __str__(self):
        course_str = f"{self.course_name}"
        if self.description:
            course_str += f":\n {self.description}"
        return course_str

class Education:
    def __init__(self, degree_level:str, start_date:date, university_name:str=None, study_name:str=None, end_date:date=None, gpa:float=None,thesis:Project=None, courses:List[Course]=None) -> None: 
        self.degree_level = degree_level
        self.university_name = university_name
        self.study_name = study_name
        self.start_date = start_date
        self.end_date = end_date
        self.gpa = gpa
        self.courses = courses
        self.thesis = thesis
    def __str__(self):
        edu_str = f"🎓{self.degree_level}"
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

class Internship(Experience):
    def __init__(self, title:str, start_date:date, associated_study:Education, end_date:date=None, company:str=None, skills:List[Skills]=None, description:str=None) -> None:
        super().__init__(start_date,end_date,title, company, skills, description,print_order=2)
        # study associated with the internship
        self.associated_study = associated_study
        
    def __str__(self):
        str_top_level = '💼' + Experience.print_experiences(self)
        str_top_level += f"\nAssociated study : {self.associated_study.study_name}"
        return str_top_level
        
class Person:
    def __init__(self, name:str, education:List[Education]=None, experience:List[Experience]=None, date_of_birth:date=None) -> None:
        self.name = name
        self.education = education
        self.experience = experience
        self.age = self.calculate_age(date_of_birth)

    def calculate_age(self,date_of_birth):  
        time_since_birth = relativedelta(datetime.now(),date_of_birth)
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
            output += "=== Experience ===\n"
            for exp in self.experience:
                output += f"{exp}\n\n"
        return output

class Publications:
    def __init__(self, journal_name:str, title:str, doi:str,authors:List[Person] ) -> None:
        self.journal_name = journal_name
        self.title = title
        self.doi = doi 
        self.authors = authors
    def __str__(self):
        authors_list = ", ".join([author.name for author in self.authors])
        return f"  {self.title}.\n    {authors_list}\n    Published in {self.journal_name}\n    DOI: {self.doi}"

class PhD(Experience):
    def __init__(self, title:str, start_date:date, end_date:date=None, company:str=None, skills:List[Skills]=None, description:str=None, publications:List[Publications]=None) -> None:
        super().__init__(start_date,end_date,title, company, skills, description,print_order=1)
        self.publications = publications
        
    def __str__(self):  
        str_top_level = '💼' + Experience.print_experiences(self)
        if self.publications:
            str_top_level += "\n\n  📃Relevant Publications\n"
            for pub in self.publications:
                str_top_level += f"{pub}\n"               
        return str_top_level

class CompareHelper:
    def __init__(self, type, date):
        self.type = type
        self.date = date
    
    def __lt__(self, other):
        if (self.type < other.type):
            return True
        elif(self.type == other.type and self.date < other.date):
            return True
        else:
            return False
            
    def __eq__(self, other):
        return self.type == other.type and self.date == self.date

def sort_objects(ordered_skills,sort_type,order):
    if sort_type:
        return sorted(ordered_skills,key=lambda s: CompareHelper(s.print_order,s.start_date),reverse=order)
    else:
        return sorted(ordered_skills,key=lambda s:s.start_date,reverse=order)
    