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
education_html = ''
with open('../data/education.csv', newline='') as edu_csv:
    educations = csv.DictReader(edu_csv)    
    for edu in educations:
        education =create_education(edu)
        studies.append(education)
        education_html += education.to_html()

articles = []
with open('../data/publications.csv', newline='') as publications_csv:
    publication_reader = csv.DictReader(publications_csv)
    for pub in publication_reader:
        articles.append(create_publication(pub, people))

with open('../data/experiences.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    all_experiences = []
    theses = []
    html_experiences = []
    for row in reader:     
        if row['project_type'] == '0':
            job = create_job(row)
            all_experiences.append(job)
            html_experiences.append(job.to_html())
        elif row['project_type'] == '1':
            phd = create_Phd(row,articles)
            all_experiences.append(phd)
            html_experiences.append(phd.to_html())
        elif row['project_type'] == '2':
            if row['associated_study']:
                associated = [s for s in studies if s.degree_level.lower() in row['associated_study'].lower()]
                internship = create_internship(row,associated[0])
                all_experiences.append(internship)
                html_experiences.append(internship.to_html())
        elif row['project_type']=='3':
            project = create_project(row)
            all_experiences.append(project)
            html_experiences.append(project.to_html())
        elif row['project_type']=='4':
            thesis = create_project(row)
            all_experiences.append(create_project(row))  
            html_experiences.append(thesis.to_html())

experience = sort_objects(all_experiences,1,False)
sorted_indexes = [i for i,j in experience]
sorted_html = [exp_html for _, exp_html in sorted(zip(sorted_indexes,html_experiences))]
all_experiences_html = ''.join(sorted_html)


html =  '<img src="../images/ruchella_banner.svg" alt="ruchella_banner">'
html += people[0].to_html()
html += "<h2>👤📊 Personal profile Visualized </h2>"
html += '<img src="../images/gauge_age.svg" alt="gauge chart for age">'
html += '<img src="../images/map_location.svg" alt="map location">'
html += "<h1>🎓 Education</h1>"
html += education_html
html += "<h2>🎓📊 Education Visualized </h2>"
html += '<img src="../images/stacked_bar_studies.svg" alt="stacked_bar_studies">'
html += '<img src="../images/circle_education_courses.svg" alt="circle_education_courses">'
html += "<h1>💼 Experience(s) </h1>"
html += all_experiences_html
html += "<h2>💼📊 Experience(s) Visualized </h2>"
html += '<img src="../images/timeline_full.svg" alt="timeline_full">'
html += '<img src="../images/pie_experience_type.svg" alt="pie_experience_type">'
html += '<img src="../images/tree_skills.svg" alt="tree_skills">'
html += '<img src="../images/wordcloud_skills.svg" alt="wordcloud_skills">'
save_file('../generated_cvs/my_cv_with_visualizations.md',html)