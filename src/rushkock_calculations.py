

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from dateutil.relativedelta import relativedelta
    from datetime import date,datetime
    date_of_birth = date(1998, 7, 28)
    def calculate_date_of_birth(date_of_birth):  
        time_since_birth = relativedelta(datetime.now(),date_of_birth)
        return time_since_birth
    time_since_birth = calculate_date_of_birth(date_of_birth)
    version = f"{time_since_birth.years}.{time_since_birth.months}.{time_since_birth.days}-yellow"
    return date, date_of_birth, datetime, relativedelta, version


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
    #from cv_objects import Course,Project,Skills,Education,PhD,Job,Internship,Person,Publications,sort_objects
    return


@app.cell
def _(date, datetime, relativedelta):
    from typing import List
    from abc import ABC, abstractmethod
    #from dateutil.relativedelta import relativedelta
    #from datetime import date, datetime

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

    class Address:
        def __init__(self, address:str, postal_code:str, city:str, country:str, region:str):
            self.address = address
            self.postal_code = postal_code
            self.city =city
            self.country = country
            self.region = region

        def __str__(self):
            output = f"🏠{self.address},{self.city},{self.postal_code},{self.region},{self.country}"
            return output

    class Socials:
        def __init__(self,type:str,link:str):
            self.type = type
            self.link = link
        def __str__(self):
            return f"{self.type} : {self.link}"
        def to_html(self):
            return f"<li><strong>{self.type}</strong>: <a href='{self.link}' target='_blank'>{self.link}</a></li>"


    class Contact_info:
        def __init__(self,email:str,phone_number:int=None,website:str=None, address:Address=None, socials:List[Socials]=None):
            self.email = email
            self.phone_number = phone_number
            self.link = website
            self.address = address
            self.socials = socials
        def __str__(self):
            output = f"📧{self.email}"
            if self.phone_number:
                output += f"\n📱{self.phone_number}"
            if self.link:
                output += f"\n🔗{self.link}"
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
            if self.link:
                html += f"<p>🔗 <a href='{self.link}' target='_blank'>{self.link}</a></p>"
            if self.address:
                html += self.address.to_html()
            if self.socials:
                html += "<p>📶 Follow me on:</p><ul>"
                for social in self.socials:
                    html += social.to_html()
                html += "</ul>"
            return html

    class Interests:
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
        def __init__(self,title:str,description:str,date:date,link:str=None,issuer:str=None):
            self.title = title
            self.description = description
            self.date = date
            self.link = link 
            self.issuer = issuer
        def __str__(self):
            output = f"{self.title}({self.date.strftime("%m/%Y")})\n{self.description}"
            if self.link:
                output += f"\nLink: {self.link}"
            if self.issuer:
                output += f"\nIssuer: {self.issuer}"
            return output
        def to_html(self):
            html = f"<div><h3>{self.title} <span style='font-size:small;color:gray;'>({self.date.strftime('%b %Y')})</span></h3>"
            html += f"<p>{self.description}</p>"
            if self.link:
                html += f"<p>🔗 <a href='{self.link}' target='_blank'>Certificate Link</a></p>"
            if self.issuer:
                html += f"<p><strong>Issuer:</strong> {self.issuer}</p>"
            html += "</div>"
            return html

    class Person:
        def __init__(self, name: str, education: List[Education] = None, experience: List[Experience] = None, date_of_birth: date = None,summary:str=None,contact:List[Contact_info]=None, interests:List[Interests]=None, certificates:List[Certificates]=None) -> None:
            self.name = name
            self.education = education
            self.experience = experience
            self.summary = summary
            self.age = self.calculate_age(date_of_birth)
            self.contact = contact
            self.interests = interests
            self.certificates = certificates

        def calculate_age(self, date_of_birth):
            if not date_of_birth:
                return None
            time_since_birth = relativedelta(datetime.now(), date_of_birth)
            return time_since_birth

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
    return (
        Address,
        Contact_info,
        Course,
        Education,
        Interests,
        Internship,
        Job,
        Person,
        PhD,
        Project,
        Publications,
        Skills,
        Socials,
        sort_objects,
    )


@app.cell
def _(
    Address,
    Contact_info,
    Course,
    Education,
    Interests,
    Internship,
    Job,
    Person,
    PhD,
    Project,
    Publications,
    Skills,
    Socials,
    date,
    date_of_birth,
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

    # Add my personal info
    interests = [Interests(name='Triathlons'), Interests(name='Reading',description='I enjoy fantasy and sci-fi book as well as philosophy'), Interests(name='Weight Lifting')]

    socials = [Socials(type='Github', link='https://github.com/rushkock'),Socials(type='LinkedIn', link='https://www.linkedin.com/in/ruchella-kock/')]

    address = Address(address='Koningweg 198', postal_code='1928AK',city='Amsterdam', country='The Netherlands',region='South')
    contact = Contact_info(email='test@test.com', socials=socials, website='ruchella.com',address=address)

    summary = 'I am passionate about the intersection of neuroscience and machine learning. My work focuses on understanding how the brain processes real world behavior captured through (smart) devices. I primarily fulfill the role of a data scientist working with timeseries datasets.'

    # initialize authors for the publications
    ruchella = Person(name="Ruchella Kock",education=[bsc,msc],date_of_birth=date_of_birth, interests=interests, summary=summary, contact=contact)
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
    print(ruchella)
    return


@app.cell
def _(Person):
    import csv
    from csv_to_objects import create_project,create_internship,create_job,create_Phd,create_education,create_project,create_publication
    people = []
    with open('data/person.csv', newline='') as pp_csv:
        persons = csv.DictReader(pp_csv)
        for person in persons:
            obj = Person(name=person['name'])
            if person['date_of_birth']:
                obj.date_of_birth = person['date_of_birth']
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
    people[0].experience = all_experiences
    people[0].education = studies
    print(people[0])
    return (all_experiences,)


@app.cell
def _(all_experiences):
    all_experiences
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
