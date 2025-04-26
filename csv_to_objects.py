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