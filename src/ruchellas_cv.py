import csv
from cv_objects import Person
from csv_to_objects import sort_objects,create_person,create_project,create_internship,create_job,create_Phd,create_education,create_project,create_publication
from conversion_functions import save_file

people = []
with open('../data/person.csv', newline='') as pp_csv:
    persons = csv.DictReader(pp_csv)
    for person in persons:
        people.append(create_person(person))
        
studies = []
with open('../data/education.csv', newline='') as edu_csv:
    educations = csv.DictReader(edu_csv)
    for edu in educations:
        studies.append(create_education(edu))

articles = []
with open('../data/publications.csv', newline='') as publications_csv:
    publication_reader = csv.DictReader(publications_csv)
    for pub in publication_reader:
        articles.append(create_publication(pub, people))

with open('../data/experiences.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    all_experiences = []
    theses = []
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
        elif row['project_type']=='4':
            theses.append(create_project(row))  
            
people[0].experience =  [j for i,j in sort_objects(all_experiences,1,False)]
people[0].education = studies
print(people[0])
html = people[0].to_html()
save_file('../generated_cvs/my_cv.md',html)