

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import re
    from wordcloud import STOPWORDS,WordCloud 
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib as mpl
    from matplotlib.collections import PolyCollection
    from datetime import datetime as dt
    from dateutil.relativedelta import relativedelta
    import numpy as np
    import circlify
    import pandas as pd
    from getconti import getConti
    import pycountry
    import plotly.express as px
    import plotly.graph_objects as go
    return (
        WordCloud,
        circlify,
        dt,
        getConti,
        go,
        mdates,
        mo,
        np,
        pd,
        plt,
        px,
        pycountry,
        relativedelta,
    )


@app.cell
def _(pd):
    # Load personal data
    df_person = pd.read_csv("data/person.csv",delimiter=',',index_col=False)
    return (df_person,)


@app.cell
def _(mo):
    mo.md('# About the candidate')
    return


@app.cell
def _(mo):
    mo.md('## Candidate location')
    return


@app.cell
def _(df_person, getConti, pd, px, pycountry):
    continent = getConti().getContinents(df_person.iloc[0]['country'])
    countries = {}
    iso_nums = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
        iso_nums[country.name] = country.numeric
    code = countries.get(df_person.iloc[0]['country'], 'Unknown code')

    location_info = {'country': df_person.iloc[0]['country'],
    'continent':continent,
    'value': 50,
    'iso_alpha':code}

    df_pp = pd.DataFrame(location_info, index=[0])

    fig = px.scatter_geo(df_pp, locations="iso_alpha", color="country",hover_name="country",size="value",projection="natural earth",scope=continent.lower(),size_max=15, color_discrete_map={df_pp.iloc[0]['country']: "#ffffff"})
    fig.show()
    return


@app.cell
def _(mo):
    mo.md('## Candidate age')
    return


@app.cell
def _(df_person, dt, go, relativedelta):
    def calculate_date_of_birth(date_of_birth):  
        time_since_birth = relativedelta(dt.now(),date_of_birth)
        return time_since_birth
    age = calculate_date_of_birth(dt.strptime(df_person.iloc[0]['date_of_birth'],'%Y-%m-%d'))

    fig_age = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = age.years,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Age"},
        gauge = {'axis': {'range': [None, 100]},
                 'bar': {'color': "white"}
                }
        ))
    fig_age.show()
    return


@app.cell
def _(mo):
    mo.md('# Education')
    return


@app.cell
def _(pd):
    # Load data
    df_edu = pd.read_csv("data/education.csv",delimiter=',',index_col=False)
    return (df_edu,)


@app.cell
def _(df_edu):
    df_edu
    return


@app.cell
def _(df_edu, dt, pd):
    df_edu['start_date'] = df_edu['start_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d'))
    df_edu['end_date'] = df_edu['end_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d') if not pd.isnull(x) else dt.now())
    return


@app.cell
def _(df_edu, np, plt):
    df_edu['diff'] = df_edu['end_date'] - df_edu['start_date']
    education_dates = [round(d.days/365) for d in df_edu['diff'].to_list()]
    cumulative_sum =  [sum(education_dates[:i+1]) for i in range(len(education_dates))]
    widths = education_dates
    starts = [sum-wid for wid,sum in zip(widths,cumulative_sum)]


    fig_stacked_bar, ax_stacked_bar = plt.subplots(figsize=(10,3))
    colors = ['white', 'black']
    for bar_idx in range(len(df_edu)):
        rects = ax_stacked_bar.barh([0], widths[bar_idx], left=starts[bar_idx], height=0.5, label=df_edu.iloc[bar_idx]['study_name'], color=colors[bar_idx],edgecolor='black')

    colors.reverse()
    for idx_bar, bar, study in zip(np.arange(0,len(df_edu)),ax_stacked_bar.patches, df_edu['study_name']):
        ax_stacked_bar.text(bar.get_x()+bar.get_width()/8,0, study, color = colors[idx_bar], ha = 'left', va = 'center') 

    ax_stacked_bar.set_xlabel('Years studying')
    plt.show()
    return


@app.cell
def _(circlify, df_edu, plt):
    def f(study_name,courses):
        return {'id': study_name,
        'datum':200,
        'children': [{'id':course, 
                      'datum':100} for course in courses.split(';')]}

    edu_circ = df_edu.apply(lambda x: f(x.study_name,x.courses),axis=1).to_list()
    ctmp = [{'id': 'education', 'datum': 300, 'children': edu_circ}]

    fig_circ, ax_circ = plt.subplots(figsize=(14, 14))
    ax_circ.set_title('Repartition of the world population')
    ax_circ.axis('off')

    circ = circlify.circlify(
        ctmp,
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )
    lim_c = max(max(abs(c.x) + c.r,abs(c.y) + c.r,) for c in circ)
    plt.xlim(-lim_c, lim_c)
    plt.ylim(-lim_c, lim_c)

    # Outer circles
    for c in circ:
        if c.level != 2:
            continue
        xc, yc, rad = c
        ax_circ.add_patch(plt.Circle((xc, yc), rad, alpha=1,
                     linewidth=2, color="white"))

    # inner circles
    for c in circ:
        if c.level != 3:
            continue
        xc, yc, rad = c
        label_c = c.ex["id"]
        ax_circ.add_patch(plt.Circle((xc, yc), rad, alpha=1,
                     color="black"))
        plt.annotate(label_c, (xc, yc), ha='center', color="white")

    for c in circ:
        if c.level != 2:
            continue
        xc, yc, rad = c
        label_c = c.ex["id"]
        plt.annotate(label_c, (xc, yc+0.6), color='black',va='center', ha='center', bbox=dict(
            facecolor='white', edgecolor='black', boxstyle='round', pad=.5))
    
    ax_circ.set_title('Studies and corresponding courses', color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    plt.show()
    return


@app.cell
def _(mo):
    mo.md('# Experiences such as jobs, internships, projects')
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
def _(df_exp, np, plt):
    data = df_exp['project_type'].value_counts()
    mapping = {0:'job',1:'PhD', 2:'Internship',3:'Project', 4:'Thesis'}
    indexes = data.index
    fig_donut, ax_donut = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts = ax_donut.pie(data, wedgeprops=dict(width=0.5),colors=plt.cm.tab20c.colors[-len(data):-1], labels=[f'{round(d/sum(data)*100)}%' for d in data],labeldistance=0.6, textprops={'color':'black'})

    # setup the label properties
    bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        # add the text to labels 
        ax_donut.annotate(f'{mapping[indexes[i]].capitalize()} - Count:{data[i]}', xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),horizontalalignment=horizontalalignment,color='black', **kw)

    ax_donut.set_title('Types of experiences', color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    plt.show()
    return


@app.cell
def _(mo):
    mo.md("""## Experiences across time""")
    return


@app.cell
def _(df_exp, dt, pd):
    df_exp['start_date'] = df_exp['start_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d'))
    df_exp['end_date'] = df_exp['end_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d') if not pd.isnull(x) else dt.now())

    return


@app.cell
def _(df_exp):
    df_exp['diff'] = df_exp['end_date'] - df_exp['start_date']
    sorted_df_exp = df_exp.sort_values(by='start_date').reset_index()
    return (sorted_df_exp,)


@app.cell
def _(df_exp, dt, mdates, plt, sorted_df_exp):
    timeline_fig, ax_time = plt.subplots(figsize=(8,6))
    for index, row in sorted_df_exp.iterrows():
        start_year = mdates.date2num(row.start_date)
        duration = row['diff'].days
        ax_time.broken_barh([(start_year, duration)], 
                        (index-0.5,0.8), 
                        facecolors =('white'),
                       label=row.title)
    ax_time.set_xticks(ax_time.get_xticks())
    ax_time.set_title("Candidate's experiences across time", color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    ax_time.set_xlabel('Years')
    ax_time.set_ylabel('Experiences')
    xlabels = [dt.strftime(mdates.num2date(d),'%Y') for d in ax_time.get_xticks()]
    ax_time.set_xticklabels(xlabels)
    ax_time.set_yticks(range(len(df_exp)),labels=sorted_df_exp['title'])
    plt.show()
    return


@app.cell
def _(mo):
    mo.md("""## Amount of time spent per experience""")
    return


@app.cell
def _(circlify, df_exp, plt):
    days_on_project = df_exp['diff'].apply(lambda x: round(x.days))
    circles = circlify.circlify(
        days_on_project.to_list(),
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )
    # Create just a figure and only one subplot
    fig_circle, ax_circle = plt.subplots(figsize=(8, 8))
    ax_circle.set_title('Days spent per experience', color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    ax_circle.axis('off')
    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    # list of labels
    sorted_labels = [f'{df_exp['title'][i[0]]}\nYears: {i[1]}' for i in sorted(enumerate(days_on_project), key=lambda x:x[1])]
    for circle, label in zip(circles, sorted_labels):
        xx, yy, r = circle
        ax_circle.add_patch(plt.Circle((xx, yy), r*0.9, alpha=0.9, linewidth=2,
                     facecolor="white", edgecolor="black"))
        plt.annotate(label, (xx, yy), va='center', ha='center', bbox=dict(
            facecolor='black', edgecolor='black', boxstyle='round', pad=0))
    plt.show()
    return


@app.cell
def _(mo):
    mo.md("""## Skills acquired during experiences""")
    return


@app.cell
def _(df_exp):
    df_exp['skills'] = df_exp['skills'].apply(lambda x: x.split(';')) 
    return


@app.cell
def _(df_exp, pd, px):
    tmp = pd.DataFrame()
    tmp['level_1'] = [title for skills, title in zip(df_exp['skills'],df_exp['title']) for _ in skills]
    tmp['level_2'] = [_ for skill in df_exp['skills'] for _ in skill]
    tmp['level_3'] = [d.days for d,skills in zip(df_exp['diff'],df_exp['skills']) for _ in skills]

    fig_tree = px.treemap(tmp, path=['level_1', 'level_2'], color='level_3', values='level_3',color_continuous_scale='greys',labels={'level_3': 'Days on experience'},width=900, height=700)
    fig_tree.update_layout(
     title={'text':'Experience and relevant skills',
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_tree.show()
    return


@app.cell
def _(mo):
    mo.md("""## Relevant Skills""")
    return


@app.cell
def _(WordCloud, df_exp, plt):
    type = 'skills'
    text = ' '.join(df_exp[type].astype(str).tolist())
    processed_text = WordCloud().process_text(text)
    wordcloud = WordCloud(width=800, height=400, background_color='black',color_func=lambda *args, **kwargs: 'white').fit_words(processed_text)

    fig_wordcloud, ax_wordcloud = plt.subplots(figsize=(10, 5))
    ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
    ax_wordcloud.axis('off') 
    ax_wordcloud.set_title("Relevant Skills", color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    plt.show()
    return


if __name__ == "__main__":
    app.run()
