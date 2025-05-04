from cv_objects import Course,Project,Skills,Education,PhD,Job,Internship,Person,Publications,sort_objects,Contact_info,Address,Socials,Certificates,Interests
from datetime import datetime

def check_empty(row,y):
    if row[y]:
        return row[y]
    else:
        return None
        
def create_project(row):
    """ Create object(s) Project from experiences.csv
    """
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
    """ Create object(s) Publications from publications.csv
    """
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
    """ Create object(s) Education from educations.csv
    """
    def cc(y):
        return check_empty(row,y)
    obj = Education(degree_level=row['degree_level'],start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date())
    obj.university_name=cc('university_name')
    obj.study_name=cc('study_name')
    if row['gpa']:
        obj.gpa=float(row['gpa'])
    if row['end_date']:
        obj.end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date()
    if row['courses']:
        obj.courses=[Course(course_name=s.strip(' ')) for s in row['courses'].split(';')]
    return obj

def create_job(row):
    """ Create object(s) Job from experiences.csv
    """   
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
    """ Create object(s) Internship from educations.csv
    """
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
    """ Create object(s) PhD from experiences.csv
    """
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

def create_person(row):
    """ Create object(s) Person from person.csv
    """
    def cc(y):
        return check_empty(row,y)
    if row['date_of_birth']:
        obj = Person(name=row['name'],date_of_birth=datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date())
    else:
        obj = Person(name=row['name'])
    obj.summary = cc('summary')
    if row['email']:
        contact_obj = Contact_info(email=row['email'])
        contact_obj.phone_number=cc('phone_number')
        contact_obj.website=cc('website')
        if row['address'] and row['postal_code'] and row['city'] and row['country'] and row['region']:
            contact_obj.address = Address(address=row['address'],postal_code=row['postal_code'],city=row['city'],country=row['country'],region=row['region'])
        if row['socials']:
            contact_obj.socials = [Socials(type=pp.split(':')[0], link=''.join(pp.split(':')[1:])) for pp in row['socials'].split(';')]
    obj.contact = contact_obj
    if row['interests']:
        obj.interests = [Interests(name=i.split(':')[0], description=i.split(':')[1]) if len(i.split(':')) > 1 else Interests(name=i.split(':')[0]) for i in row['interests'].split(';')]
    return obj
            