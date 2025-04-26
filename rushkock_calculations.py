

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from dateutil.relativedelta import relativedelta
    from datetime import date,datetime
    birthday = date(1998, 7, 28)
    def calculate_birthday(birthday):  
        time_since_birth = relativedelta(datetime.now(),birthday)
        return time_since_birth
    time_since_birth = calculate_birthday(birthday)
    version = f"{time_since_birth.years}.{time_since_birth.months}.{time_since_birth.days}-yellow"
    return birthday, date, datetime, relativedelta, version


@app.cell
def _(version):
    with open('README.md', 'r') as f:
        markdown_string = f.read()
        new_string = markdown_string.replace(markdown_string[markdown_string.find('Me-v')+4:614], version)

    with open('README.md', 'w') as f:
        f.write(new_string)
    return


@app.cell
def _():
    from typing import List
    from abc import ABC, abstractmethod
    return ABC, List, abstractmethod


@app.cell
def _(ABC, List, abstractmethod, date, datetime, relativedelta):
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
        def __init__(self, name:str, education:List[Education]=None, experience:List[Experience]=None, birthday:date=None) -> None:
            self.name = name
            self.education = education
            self.experience = experience
            self.age = self.calculate_age(birthday)

        def calculate_age(self,birthday):  
            time_since_birth = relativedelta(datetime.now(),birthday)
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

    return (
        Course,
        Education,
        Internship,
        Job,
        Person,
        PhD,
        Project,
        Publications,
        Skills,
        sort_objects,
    )


@app.cell
def _(
    Course,
    Education,
    Internship,
    Job,
    Person,
    PhD,
    Project,
    Publications,
    Skills,
    birthday,
    date,
    sort_objects,
):
    # My Bachelor
    courses = [Course('Applied Cognitive Psychology'), Course('Cognitive Neuroscience'), Course('Clinical Neuropsychology'), Course('Artificial Intelligence'),Course('Minor in Programming')]

    thesis_bsc = Project(start_date=date(2019, 3, 1),
                     end_date=date(2019, 7, 1),
                     company="Leiden University",
                     skills=[Skills("Statistics", 1), Skills("Permutation Testing",1), Skills('Simulations',1)],
                     project_title="Violation of homogeneity of variances: A comparison between Welch’s t-test and the permutation test",
                     project_link="http://rushkock-env.eba-yi6rkpue.us-east-1.elasticbeanstalk.com/thesis")

    bsc = Education(degree_level="Bachelor", 
                    university_name="Universiteit Leiden", 
                    study_name="International Bachelor in Psychology (IBP)",
                    start_date=date(2016,9,1),
                    end_date=date(2019,7,1),
                    gpa=8.0, 
                    courses=courses,
                    thesis=thesis_bsc)
    # My master
    courses_msc = [Course('Information Visualization'), Course('Information Organization')]
    thesis_msc = Project(start_date=date(2021, 4, 1),
                     end_date=date(2021,7,28),
                     company="Leiden University",
                     skills=[Skills("LSTM", 1)],
                     project_title="Analysis of Movements Identified by Artificial Neural Network During Smartphone Use.",
                     project_link="https://scripties.uba.uva.nl/search?id=726200")
    msc = Education(degree_level="Master", 
                    university_name="Universiteit van Amsterdam", 
                    study_name="Information Studies - Data Science Track",
                    start_date=date(2019,9,1),
                    end_date=date(2021,7,1), 
                    gpa=7.95, 
                    courses=courses_msc,
                    thesis=thesis_msc)

    # My professional experiences
    description_job1 = 'Full-stack development of agestudy.nl, a platform for a scientific study conducted by Leiden University to study healthy aging across a wide range of individuals. I created and managed a relational database for 3 years'

    # Job experiences
    skills_job1 = [Skills(skill='Python',type=1),Skills(skill='Database Management',type=0),Skills(skill='Javascript (D3)',type=1),Skills(skill='HTML (D3)',type=1), Skills(skill='CSS',type=1),Skills(skill='postgreSQL',type=1),Skills(skill='Azure',type=1)]

    job1 = Job(title='Full Stack Developer', 
                      company='Leiden University (Cognition in the Digital Environment Laboratory)',
                      start_date=date(2019,11,1),
                      end_date=date(2021,6,1), 
                      description=description_job1, 
                      skills=skills_job1)

    # Define descriptions
    description_job2 = ("In my Data Visualization Internship at QuantActions A.G., I designed and implemented data visualizations for a smartphone-based health and behavior application. My role focused on making complex behavioral data easily interpretable for end users." )

    skills_job2 = [Skills("Data Visualization design", 1), Skills("Agile Thinking", 0)]

    job2 = Internship(title='Data Visualization Internship', 
                      company='QuantActions A.G.',
                      start_date=date(2020, 11, 1),
                      end_date=date(2021, 2, 1), 
                      description=description_job2, 
                      skills=skills_job2,
                      associated_study=bsc)

    skills_job3 = [Skills("Deep Learning", 1), Skills("Data Alignment", 1)]

    description_job3 = ("During my Research Internship, I developed and trained a Long Short-Term Memory (LSTM) model for predicting sensor data. My work also involved the alignment and integration of datasets collected from four different sources to create a coherent dataset for analysis.")

    job3 = Internship(title="Research Internship",
                      company='Leiden University (Cognition in digital environment',
                      start_date=date(2020, 7, 1),
                      end_date=date(2021, 7, 1),
                      description=description_job2,
                      skills=skills_job3,
                      associated_study=bsc)

    # initialize authors for the publications
    ruchella = Person(name="Ruchella Kock",education=[bsc,msc],birthday=birthday)
    enea = Person(name="Enea Ceolini")
    guido = Person(name="Guido PH Band")
    gijsbert = Person(name="Gijsbert Stoet")
    arko = Person(name="Arko Ghosh")
    lysanne = Person(name="Lysanne Groenewegen")

    article1 = Publications(journal_name="iScience",
                                title="Temporal clusters of age-related behavioral alterations captured in smartphone touchscreen interactions",
                                doi="10.1016/j.isci.2022.104791",
                                authors=[enea, ruchella, guido, gijsbert, arko])

    article2 = Publications(journal_name="NeuroImage: Reports",
                                title="Neural processing of goal and non-goal-directed movements on the smartphone",
                                doi="10.1016/j.ynirp.2023.100164",
                                authors=[ruchella, enea, lysanne, arko])

    article3 = Publications(journal_name="bioRxiv",
                                title="Neural microstates in real-world behaviour captured on the smartphone",
                                doi="10.1101/2024.07.22.604605",
                                authors=[ruchella, arko])

    article4 = Publications(journal_name="bioRxiv",
                                title="Multiple forms of neural processing when repeating voluntary thumb flexions",
                                doi="10.1101/2023.02.19.529148",
                                authors=[ruchella, arko])

    publications = [article1,article2,article3,article4]

    skills_job4 = [Skills("Deep Learning", 1), Skills("Data Alignment", 1)]

    description_job4 = ("As an Education and Research Staff Member, I analyzed electroencephalography (EEG) datasets in combination with behavioral data collected from multiple sensors and smartphone usage. I trained machine learning algorithms, including Long Short-Term Memory (LSTM) networks and Support Vector Machines (SVMs), to identify neural correlates of movements associated with smartphone activity.")

    # Create Experience objects
    job4 = PhD(title="Phd Candidate",
               company='Leiden University (Cognition in digital environment)',
               start_date=date(2021, 10, 1),
               end_date=None,  # ongoing
               description=description_job4,
               skills=skills_job4,
               publications=publications)

    project1 = Project(title="Computer Vision Project",
                       start_date=date(2020, 6, 1),
                       end_date=date(2020, 6, 30),
                       skills=[Skills("Computer Vision", 1), Skills("VGG16", 1), Skills("Deep Learning", 1)],
                       project_title="Pizza or Donuts: Food Image Classification with VGG16",
                       project_link="http://rushkock-env.eba-yi6rkpue.us-east-1.elasticbeanstalk.com/computer_vision")

    ruchella.experience = sort_objects([job1,job2,job3,job4,project1],1,False)
    return


@app.cell
def _(
    Person,
    create_Phd,
    create_education,
    create_internship,
    create_job,
    create_project,
    create_publication,
):
    import csv

    people = []
    with open('data/person.csv', newline='') as pp_csv:
        persons = csv.DictReader(pp_csv)
        for person in persons:
            obj = Person(name=person['name'])
            if person['birthday']:
                obj.birthday = person['birthday']
            people.append(obj)
        
    studies = []
    with open('data/education.csv', newline='') as edu_csv:
        educations = csv.DictReader(edu_csv)
        for edu in educations:
            studies.append(create_education(edu))

    articles = []
    with open('data/publications.csv', newline='') as publications_csv:
        publication_reader = csv.DictReader(publications_csv)
        for pub in publication_reader:
            articles.append(create_publication(pub, people))

    with open('data/experiences.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        all_experiences = []
        for row in reader:     
            if row['project_type'] == '0':
                all_experiences.append(create_job(row))
            elif row['project_type'] == '1':
                all_experiences.append(create_Phd(row,articles))
            elif row['project_type'] == '2':
                if row['associated_study']:
                    associated = [s for s in studies if s.degree_level.lower() in row['associated_study'].lower()]
                    all_experiences.append(create_internship(row,associated[0]))
            elif row['project_type']=='3':
                all_experiences.append(create_project(row))  
    return


@app.cell
def _(
    Course,
    Education,
    Internship,
    Job,
    Person,
    PhD,
    Project,
    Publications,
    Skills,
    datetime,
):
    def check_empty(row,y):
        if row[y]:
            return row[y]
        else:
            return None
        
    def create_project(row):
        def cc(y):
            return check_empty(row,y)
        obj = Project(start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date())
        obj.project_title=cc('project_title')
        obj.project_link=cc('project_link')
        obj.title=cc('title')
        obj.company=cc('company')
        obj.description=cc('description')
        if row['end_date']:
            obj.end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date()
        if row['skill_type'] and row['skills']:
            s = [s.strip(' ') for s in row['skills'].split(';')]
            obj.skills=[Skills(i,j) for i,j in zip(s,row['skill_type'].split(';'))]
        return obj
    
    def create_publication(row,existing_people):
        authors_cleaned = [s.strip(' ').lower() for s in row['authors'].split(';')]
        names_existing = [e.name.lower() for e in existing_people]
        author_list = [Person(name=author) if author not in names_existing else existing_people[names_existing.index(author)] for author in authors_cleaned]
        obj = Publications(
            journal_name=row['journal_name'],
            title=row['title'],
            doi=row['doi'],
            authors=author_list)
        return obj
    
    def create_education(row):
        def cc(y):
            return check_empty(row,y)
        obj = Education(degree_level=row['degree_level'],start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date())
        obj.university_name=cc('university_name')
        obj.study_name=cc('study_name')
        if row['gpa']:
            obj.gpa=float(row['gpa'])
        if row['end_date']:
            obj.end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date()
        if row['courses'] and row['courses']:
            courses=[Course(course_name=s.strip(' ')) for s in row['courses'].split(';')]
        return obj

    def create_job(row):
        def cc(y):
            return check_empty(row,y)
        obj = Job(title=row['title'],start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date())
        obj.company=cc('company')
        obj.description=cc('description')
        if row['end_date']:
            obj.end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date()
        if row['skill_type'] and row['skills']:
            s = [s.strip(' ') for s in row['skills'].split(';')]
            obj.skills=[Skills(i,j) for i,j in zip(s,row['skill_type'].split(';'))]            
        return obj

    def create_internship(row,education):
        def cc(y):
            return check_empty(row,y)
        obj = Internship(title=row['title'],start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date(),associated_study=education)
        obj.company=cc('company')
        obj.description=cc('description')
        if row['end_date']:
            obj.end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date()   
        if row['skill_type'] and row['skills']:
            s = [s.strip(' ') for s in row['skills'].split(';')]
            obj.skills=[Skills(i,j) for i,j in zip(s,row['skill_type'].split(';'))]            
        return obj

    def create_Phd(row,publications):
        def cc(y):
            return check_empty(row,y)
        obj = PhD(title=row['title'],start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date())
        obj.company=cc('company')
        obj.description=cc('description')
        if row['end_date']:
            obj.end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date()   
        if row['skill_type'] and row['skills']:
            s = [s.strip(' ') for s in row['skills'].split(';')]
            obj.skills=[Skills(i,j) for i,j in zip(s,row['skill_type'].split(';'))] 
        if publications:
            obj.publications=publications
        return obj
    return (
        create_Phd,
        create_education,
        create_internship,
        create_job,
        create_project,
        create_publication,
    )


if __name__ == "__main__":
    app.run()
