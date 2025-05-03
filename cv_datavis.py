

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import re
    from datetime import datetime as dt
    from dateutil.relativedelta import relativedelta
    import pandas as pd
    from cv_plots import circle_experiences,wordcloud_skills,tree_skills,plot_timeline,pie_experience_type,stacked_bar_studies,circle_education_courses,gauge_age,map_location
    return (
        circle_education_courses,
        circle_experiences,
        dt,
        gauge_age,
        map_location,
        mo,
        pd,
        pie_experience_type,
        plot_timeline,
        relativedelta,
        stacked_bar_studies,
        tree_skills,
        wordcloud_skills,
    )


@app.cell
def _(pd):
    # Load personal data
    df_person = pd.read_csv("data/person.csv",delimiter=',',index_col=False)
    return (df_person,)


@app.cell
def _(mo):
    mo.md("""# About the candidate""")
    return


@app.cell
def _(mo):
    mo.md("""## Candidate location""")
    return


@app.cell
def _(df_person, map_location):
    map_location(df_person)
    return


@app.cell
def _(mo):
    mo.md("""## Candidate age""")
    return


@app.cell
def _(df_person, dt, gauge_age, relativedelta):
    def calculate_date_of_birth(date_of_birth):  
        time_since_birth = relativedelta(dt.now(),date_of_birth)
        return time_since_birth
    age = calculate_date_of_birth(dt.strptime(df_person.iloc[0]['date_of_birth'],'%Y-%m-%d'))
    gauge_age(age)
    return


@app.cell
def _(mo):
    mo.md("""# Education""")
    return


@app.cell
def _(pd):
    # Load data
    df_edu = pd.read_csv("data/education.csv",delimiter=',',index_col=False)
    return (df_edu,)


@app.cell
def _(df_edu, dt, pd, stacked_bar_studies):
    df_edu['start_date'] = df_edu['start_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d'))
    df_edu['end_date'] = df_edu['end_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d') if not pd.isnull(x) else dt.now())
    df_edu['diff'] = df_edu['end_date'] - df_edu['start_date']
    stacked_bar_studies(df_edu,(10,3),'Education across time')
    return


@app.cell
def _(circle_education_courses, df_edu):
    def f(study_name,courses):
        return {'id': study_name,
        'datum':200,
        'children': [{'id':course, 
                      'datum':100} for course in courses.split(';')]}

    edu_circ = df_edu.apply(lambda x: f(x.study_name,x.courses),axis=1).to_list()
    ctmp = [{'id': 'education', 'datum': 300, 'children': edu_circ}]
    circle_education_courses(ctmp,(15, 14),'Education and corresponding courses')
    return


@app.cell
def _(mo):
    mo.md("""# Experiences such as jobs, internships, projects""")
    return


@app.cell
def _(pd):
    # Load data
    df_exp = pd.read_csv("data/experiences.csv",delimiter=',',index_col=False)
    return (df_exp,)


@app.cell
def _(mo):
    mo.md("""## Different types of experiences""")
    return


@app.cell
def _(df_exp, pie_experience_type):
    data = df_exp['project_type'].value_counts()
    mapping = {0:'job',1:'PhD', 2:'Internship',3:'Project', 4:'Thesis'}
    pie_experience_type(data,mapping,(6, 3),'Types of experiences')
    return


@app.cell
def _(mo):
    mo.md("""## Experiences across time""")
    return


@app.cell
def _(df_exp, dt, pd, plot_timeline):
    df_exp['start_date'] = df_exp['start_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d'))
    df_exp['end_date'] = df_exp['end_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d') if not pd.isnull(x) else dt.now())
    df_exp['diff'] = df_exp['end_date'] - df_exp['start_date']
    sorted_df_exp = df_exp.sort_values(by='start_date').reset_index()
    plot_timeline(sorted_df_exp,(8,6),"Candidate's experiences across time")
    return


@app.cell
def _(mo):
    mo.md("""## Amount of time spent per experience""")
    return


@app.cell
def _(circle_experiences, df_exp):
    days_on_project = df_exp['diff'].apply(lambda x: round(x.days))
    circle_experiences(df_exp,days_on_project,(8, 8),'Days spent per experience')
    return


@app.cell
def _(mo):
    mo.md("""## Skills acquired during experiences""")
    return


@app.cell
def _(df_exp, pd, tree_skills):
    df_exp['skills'] = df_exp['skills'].apply(lambda x: x.split(';')) 
    tmp = pd.DataFrame()
    tmp['level_1'] = [title for skills, title in zip(df_exp['skills'],df_exp['title']) for _ in skills]
    tmp['level_2'] = [_ for skill in df_exp['skills'] for _ in skill]
    tmp['level_3'] = [d.days for d,skills in zip(df_exp['diff'],df_exp['skills']) for _ in skills]
    tree_skills(tmp)
    return


@app.cell
def _(mo):
    mo.md("""## Relevant Skills""")
    return


@app.cell
def _(df_exp, wordcloud_skills):
    type = 'skills'
    text = ' '.join(df_exp[type].astype(str).tolist())
    wordcloud_skills(text,'Relevant Skills')
    return


@app.cell
def _(mo):
    mo.md("""# Full career timeline""")
    return


@app.cell
def _(df_edu, df_exp, pd):
    df_edu['title'] = df_edu['study_name']
    df_merged = pd.concat([df_exp[['diff','start_date', 'end_date','title']], df_edu[['diff','start_date', 'end_date','title']]], axis=0)
    df_merged_sorted = df_merged.sort_values(by='start_date').reset_index()
    return (df_merged_sorted,)


@app.cell
def _(df_merged_sorted, plot_timeline):
    plot_timeline(df_merged_sorted,(15,6),'Full career timeline')
    return


if __name__ == "__main__":
    app.run()
