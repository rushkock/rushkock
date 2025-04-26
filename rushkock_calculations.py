

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
    return birthday, date, version


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
    from cv_objects import Course,Project,Skills,Education,PhD,Job,Internship,Person,Publications,sort_objects
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
