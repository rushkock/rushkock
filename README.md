![ruchella_banner](https://github.com/user-attachments/assets/fadf09d7-ecf5-47cc-9acf-fbf489608e38)
# Structured CV: My Career in Code

This Python package was developed as a way to showcase my professional and technical skills through a structured, object-oriented framework. 
The idea behind this project is to "show, not tell" — rather than simply describing my experience, I have built a tool that models my CV as a collection of Python objects, demonstrating my ability to design and implement such solutions.

Although initially created to represent my own background, the package has been designed with flexibility in mind. 
The classes are generic enough that they can be easily adapted by others to model their own professional profiles. 

The package provides an efficient way to structure and organize key aspects of a CV, including education, work experience, projects, and publications, and allows for conversion between multiple formats such as CSV, HTML/Markdown, and JSON. 

Additionally, the CV can be visualized through data visualizations. 

## Getting Started
### Installation
1. Create a new environment 
2. Clone this repository and cd into the repository
3. run: ```bash pip install -r requirements.txt```

[//]: <> or you can install the package directly using: ```bash pip install git+https://github.com/rushkock/rushkock``` 

### See my CV
To see my full CV in your command line you can run: 
```bash 
python3 ruchellas_cv.py
```

### Example Usage
### Python 
```python
from cv_objects import Course,Project,Skills
courses = [Course('Applied Cognitive Psychology'), Course('Cognitive Neuroscience'), Course('Clinical Neuropsychology'), Course('Artificial Intelligence'),Course('Minor in Programming')]

thesis_bsc = Project(start_date=date(2019, 3, 1),
                 end_date=date(2019, 7, 1),
                 company="Leiden University",
                 skills=[Skills("Statistics", 1), Skills("Permutation Testing",1), Skills('Simulations',1)],
                 project_title="Violation of homogeneity of variances: A comparison between Welch’s t-test and the permutation test",
                 project_link="http://rushkock-env.eba-yi6rkpue.us-east-1.elasticbeanstalk.com/thesis")
```


## Key Features
What you can do with the package:
- Import CSV and create objects
- Create data visualizations of your CV (through the CSV file) 
- Create your CV through objects and export as HTML/markdown or JSON

# Available classes
| Class             | Attributes                                                                 | Methods                                          |
|-------------------|----------------------------------------------------------------------------|--------------------------------------------------|
| Person            | name, education, experience, date\_of\_birth, summary, contact, interests, certificates | \_\_str\_\_, to\_html, calculate\_age           |
| Education         | degree\_level, university\_name, study\_name, start\_date, end\_date, gpa, thesis, courses | \_\_str\_\_, to\_html                          |
| Experience        | start\_date, end\_date, title, company, skills, description, print\_order | print\_experiences, reorder\_skills, to\_html, \_\_str\_\_ |
| Job               | title, start\_date, end\_date, company, skills, description                | to\_html, \_\_str\_\_                          |
| Project           | start\_date, title, end\_date, company, skills, description, project\_title, project\_link | to\_html, \_\_str\_\_                          |
| Internship        | title, start\_date, end\_date, company, skills, description, associated\_study | to\_html, \_\_str\_\_                          |
| Skills            | skill, type                                                                | \_\_str\_\_, to\_html                          |
| Course            | course\_name, description                                                  | \_\_str\_\_, to\_html                          |
| Thesis            | title, start\_date, description, link                                      | \_\_str\_\_, to\_html                          |
| Address           | address, postal\_code, city, country, region                               | \_\_str\_\_                                     |
| Socials           | type, link                                                                 | \_\_str\_\_                                     |
| Contact\_info     | email, phone\_number, website, address, socials                           | \_\_str\_\_                                     |
| Interests         | name, description                                                          | \_\_str\_\_, to\_html                          |
| Certificates      | title, description, date, url, issuer                                      | \_\_str\_\_                                     |
| Publications      | journal\_name, title, doi, authors                                         | \_\_str\_\_, to\_html                          |


# Available visualizations:
| Feature Name               | Description                                                                |
| -------------------------- | -------------------------------------------------------------------------- |
| `timeline full`            | A chronological timeline of the full career with start and end dates (from `experiences.csv` and `education.csv`).          |
| `circle_experiences`       | A circular (radial) chart visualizing experiences by type, title, or role (from `experiences.csv`). |
| `wordcloud_skills`         | A word cloud showing the most frequently used skills across experiences (from `experiences.csv`).   |
| `tree_skills`              | A treemap showing experiences as top-level categories with nested skills (from `experiences.csv`).  |
| `timeline`                 | A chronological timeline of experiences with start and end dates (from `experiences.csv`).          |
| `pie_experience_type`      | A pie chart breaking down experiences by type (e.g., Job, Internship) (from `experiences.csv`).     |
| `stacked_bar_studies`      | A stacked bar chart showing duration (years) spent per study or degree (from `education.csv`).    |
| `circle_education_courses` | A circle chart associating each education entry with its listed courses (from `education.csv`).   |
| `gauge_age`                | A gauge chart representing the person’s current age (from `person.csv`).                       |
| `map_location`             | A geographical map marking the address (from `person.csv`).                |


# CSV files formats
### 🧑 Person
Filename: person.csv
| Column Name     | Description                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| name            | Full name of the individual                                                                                                           |
| date\_of\_birth | Date of birth in `YYYY-MM-DD` format                                                                                                  |
| email           | Email address                                                                                                                         |
| phone\_number   | Phone number (optional)                                                                                                               |
| website         | URL to personal or professional website                                                                                               |
| address         | Street name and number                                                                                                                        |
| postal\_code    | Postal or ZIP code                                                                                                                    |
| city            | City name                                                                                                                             |
| country         | Country name                                                                                                                          |
| region          | Region or province/state                                                                                                              |
| socials         | Semicolon-separated list of social links with name:url (e.g., `GitHub:https://...;LinkedIn:https://...`)                                            |
| interests       | Semicolon-separated list of interests, with optional descriptions as follows interest:description or interest1,interest2:description,  (e.g., `Reading:sci-fi and philosophy;Triathlons`) |
| summary         | Professional summary or personal statement                                                                                            |

### 🎓Education
Filename: education.csv
| Column Name      | Description                                    |
| ---------------- | ---------------------------------------------- |
| degree\_level    | Level of education (e.g., BSc, MSc, PhD)       |
| university\_name | Name of the university                         |
| study\_name      | Name of the degree program or major            |
| start\_date      | Start date in `YYYY-MM-DD` format |
| end\_date        | End date in `YYYY-MM-DD` format   |
| gpa              | Grade Point Average                  |
| thesis           | Thesis title or topic                |
| courses          | Semicolon-separated list of key courses        |

### 💼Experience
Filename: experiences.csv
| Column Name       | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| project\_type     | Type of experience where mapping = {0:'job',1:'PhD', 2:'Internship',3:'Project', 4:'Thesis'}) |
| start\_date       | Start date in `YYYY-MM-DD` format             |
| end\_date         | End date in `YYYY-MM-DD`format               |
| title             | Role or position title                                     |
| company           | Company or organization name                               |
| skills            | Semicolon-separated list of relevant skills                |
| description       | Summary of responsibilities or achievements                |
| project\_title    | Specific project name (if applicable)                      |
| project\_link     | URL to the project (optional)                              |
| skill\_type       | Type of skills (1:`Hard`, 0:`Soft`)                 |
| associated\_study | Related degree or study program (if applicable)            |

### 📃Publications
Filename: publications.csv
| Column Name   | Description                                                                     |
| ------------- | ------------------------------------------------------------------------------- |
| title         | Full title of the publication                                                   |
| journal\_name | Name of the journal or conference                                               |
| doi           | Digital Object Identifier (e.g., `10.1038/s41586-020-03148-w`)                  |
| authors       | Semicolon-separated list of authors (e.g., `Ruchella Kock;Jane Doe;John Smith`) |

# Author(s):
:octocat: Ruchella Kock
