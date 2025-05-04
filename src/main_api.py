from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Union, List, Optional
from typing_extensions import Annotated
import csv
import codecs
from csv_to_objects import create_person,create_project,create_internship,create_job,create_Phd,create_education,create_project,create_publication
from cv_objects import Person
from copy import deepcopy

app = FastAPI()


@app.post("/article_csv_to_json/")
async def create_art(publications: UploadFile, people: Optional[UploadFile]=None):
    """ Upload publications.csv and create Publication objects, return as JSON 
    
        - Optional: Upload person.csv to add to authors to publications
    """
    articles = []
    all_publications = csv.DictReader(codecs.iterdecode(publications.file, 'utf-8'))
    if people:
        persons = await create_per(people)
    else:
        persons = []
    for pub in all_publications:   
        articles.append(create_publication(pub,persons))
    return articles

@app.post("/edu_csv_to_json/")
async def create_edu(file: UploadFile):
    """ Upload educations.csv and create Education objects, return as JSON """
    educations = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    studies = []
    for edu in educations:   
        studies.append(create_education(edu))
    return studies

@app.post("/exp_csv_to_json/")
async def create_exp(experiences: UploadFile, publications: Optional[UploadFile]=None, people: Optional[UploadFile]=None, education:Optional[UploadFile]=None):
    """ Upload experiences.csv and create Experience objects (e.g. Job,PhD,Internship,Project), return as JSON 
    
        - Optional: Upload publications.csv to add to PhD
        - Optional: Upload person.csv to add to authors to publications
        - Optional: Upload education.csv to add associated study to be able to create internship
    
    """
    experiences = csv.DictReader(codecs.iterdecode(experiences.file, 'utf-8'))
    if publications:
        if not people:
            people = []
        publications = await create_art(publications,people)
        
    if education:
        edu = await create_edu(education)
    
    all_experiences = []
    for row in experiences:   
        if row['project_type'] == '0':
                all_experiences.append(create_job(row))
        elif row['project_type'] == '1':
                all_experiences.append(create_Phd(row,publications))
        elif row['project_type'] == '2':
            if row['associated_study'] and edu:              
                associated = [s if s.degree_level.lower() in row['associated_study'].lower() else None for s in edu]
                all_experiences.append(create_internship(row,associated[0]))
        elif row['project_type']=='3':
            all_experiences.append(create_project(row))
    return all_experiences                


@app.post("/person_csv_to_json/")
async def create_per(people_csv: UploadFile):
    """ Upload person.csv and create Person objects, return as JSON """
    people = []
    persons = csv.DictReader(codecs.iterdecode(people_csv.file, 'utf-8'))
    for person in persons:
        people.append(create_person(person))
    print(people)
    return people

@app.post("/create_cv/")
async def create_cv(experiences: UploadFile, education:UploadFile, people: UploadFile, publications: Optional[UploadFile]=None):
    """ Upload experiences.csv, education.csv, person.csv, publications.csv and create full CV, return as JSON """
    file_copy = deepcopy(education)
    studies = await create_edu(education)
    if publications:
        e = await create_exp(experiences, publications=publications, education=file_copy) 
    else:
        e = await create_exp(experiences, education=education) 
    person = await create_per(people)
    person[0].education = studies
    person[0].experience = e   
    return person


@app.get("/")
async def main():
    content = """
<body>
<form action="/create_cv/" enctype="multipart/form-data" method="post">
<h3>Upload a CSV file with your experiences</h3>
<p>The file must contain the following columns:</p> 
<p>project_type,start_date,end_date,title,company,skills,description,project_title,project_link,skill_type,associated_study</p>
<br>
<input name="experiences" type="file" required>
<br>
<h3>Upload a CSV file with your education</h3>
<p>The file must contain the following columns:</p>
<p>degree_level,university_name,study_name,start_date,end_date,gpa,thesis,courses</p>
<br>
<input name="education" type="file" required>
<br>
<h3>Upload a CSV file with your personal information (optional)</h3>
<p>The file must contain the following columns:</p>
<p>name,date_of_birth</p>
<br>
<input name="people" type="file" required>
<br>
<h3>Upload a CSV file with your publications</h3>
<p>The file must contain the following columns:</p>
<p>title,journal_name,doi,authors</p>
<br>
<input name="publications" type="file">
<br>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)