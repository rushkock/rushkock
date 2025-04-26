![ruchella_banner](https://github.com/user-attachments/assets/fadf09d7-ecf5-47cc-9acf-fbf489608e38)
# Structured CV: My Career in Code

This Python package was developed as a way to showcase my professional and technical skills through a structured, object-oriented framework. 
The idea behind this project is to "show, not tell" — rather than simply describing my experience, I have built a tool that models my CV as a collection of Python objects, demonstrating my ability to design and implement such solutions.

Although initially created to represent my own background, the package has been designed with flexibility in mind. 
The classes are generic enough that they can be easily adapted by others to model their own professional profiles. 

The package provides an efficient way to structure and organize key aspects of a CV, including education, work experience, projects, and publications, and allows for conversion between multiple formats such as CSV, Markdown, and JSON.

## Getting Started
### Installation
You can clone this repository or  you can install the package directly using:

```bash
pip install git+https://github.com/rushkock/rushkock
``` 

## Key Features
You can create objects containing information about:
- Education: Degree programs, universities, GPA, selected coursework, and thesis projects.
- Professional Experience: Overview of industry positions, internships, and academic roles.
- Skills: Categorized into hard and soft skills for easy reference.
- Projects: Independent and collaborative projects.
- Publications: List of peer-reviewed articles and preprints.
- Formatted Output: Includes terminal-friendly display and export to JSON or Markdown formats.

## Example Usage
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
### Through the command line
To see my full CV in your command line you can run: 
```bash 
python3 csv_to_objects.py
```

# Author(s):
:octocat: Ruchella Kock