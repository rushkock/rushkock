from wordcloud import STOPWORDS,WordCloud 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection
from datetime import datetime as dt
from pandas import DataFrame as df
import numpy as np
import circlify
from getconti import getConti
import pycountry
import plotly.express as px
import plotly.graph_objects as go

def map_location(df_person,save_path=''):
    """ A geographical map marking the address (from person.csv).
    
        - df_person (dataframe): dataframe with country from person.csv 
        - save_path (string): path to save the plot e.g. './map.svg'
    """
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

    df_pp = df(location_info, index=[0])

    fig = px.scatter_geo(df_pp, locations="iso_alpha", color="country",hover_name="country",size="value",projection="natural earth",scope=continent.lower(),size_max=15, color_discrete_map={df_pp.iloc[0]['country']: "#ffffff"})
    fig.show()
    if save_path:
        fig.write_image(save_path)
    
def gauge_age(age,save_path=''):
    """A gauge chart representing the person’s current age (from person.csv).
    
        - age (int): Age as an int
        - save_path (string): path to save the plot e.g. './gauge.svg'
    """
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
    if save_path:
        fig_age.write_image(save_path)
    
def stacked_bar_studies(df_edu,figsize,title,save_path=''):
    """A stacked bar chart showing duration (years) spent per study or degree (from education.csv).
    
        - df_edu (dataframe): containing the fields 'start_date', 'end_date', 'study_name'
        - figsize (tuple): Figure size as (width,height)
        - title (string): title of the plot
        - save_path (string): path to save the plot e.g. './stackedbar.svg'
    """
    education_dates = [round(d.days/365) for d in df_edu['diff'].to_list()]
    cumulative_sum =  [sum(education_dates[:i+1]) for i in range(len(education_dates))]
    widths = education_dates
    starts = [sum-wid for wid,sum in zip(widths,cumulative_sum)]

    fig_stacked_bar, ax_stacked_bar = plt.subplots(figsize=figsize)
    colors = ['white', 'black']
    for bar_idx in range(len(df_edu)):
        rects = ax_stacked_bar.barh([0], widths[bar_idx], left=starts[bar_idx], height=0.5, label=df_edu.iloc[bar_idx]['study_name'], color=colors[bar_idx],edgecolor='black')

    colors.reverse()
    for idx_bar, bar, study in zip(np.arange(0,len(df_edu)),ax_stacked_bar.patches, df_edu['study_name']):
        ax_stacked_bar.text(bar.get_x()+bar.get_width()/8,0, study, color = colors[idx_bar], ha = 'left', va = 'center') 
    ax_stacked_bar.set_title(title, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    ax_stacked_bar.set_xlabel('Years studying')
    plt.show()
    if save_path:
        fig_stacked_bar.savefig(save_path, bbox_inches='tight')

def circle_education_courses(ctmp,figsize,title,save_path=''):
    """ A circle chart associating each education entry with its listed courses (from education.csv).
    
        - ctmp: dictionary with data where id=name and datum=value children=list of id and datums e.g. [{'id': 'education', 'datum': 300}]
        - figsize (tuple): Figure size as (width,height)
        - title (string): title of the plot
        - save_path (string): path to save the plot e.g. './stackedbar.svg'
    """
    fig_circ, ax_circ = plt.subplots(figsize=figsize)

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

    ax_circ.set_title(title, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    plt.show()
    if save_path:
        fig_circ.savefig(save_path, bbox_inches='tight')

def pie_experience_type(data,mapping,figsize,title,save_path=''):
    """ A pie chart breaking down experiences by type (e.g., Job, Internship) (from experiences.csv).
    
    - data: list with counts for each project_type
    - mapping: dict mapping of data e.g. {0:'job',1:'PhD', 2:'Internship',3:'Project', 4:'Thesis'})
    - figsize (tuple): Figure size as (width,height)
    - title (string): title of the plot
    - save_path (string): path to save the plot e.g. './stackedbar.svg'
    """
    indexes = data.index
    fig_donut, ax_donut = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))
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

    ax_donut.set_title(title,color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    plt.show()
    if save_path:
        fig_donut.savefig(save_path, bbox_inches='tight')
    
def timeline(sorted_df_exp,figsize,title,save_path=''):
    """ A chronological timeline of experiences with start and end dates (from experiences.csv).
    
        - sorted_df_exp (dataframe): Dataframe with fields 'title', 'diff', 'start_date', 'end_date', 
        - figsize (tuple): Figure size as (width,height)
        - title (string): title of the plot
        - save_path (string): path to save the plot e.g. './timeline.svg'
    """
    timeline_fig, ax_time = plt.subplots(figsize=figsize)
    for index, row in sorted_df_exp.iterrows():
        start_year = mdates.date2num(row.start_date)
        duration = row['diff'].days
        ax_time.broken_barh([(start_year, duration)], 
                        (index-0.5,0.8), 
                        facecolors =('white'),
                       label=row.title)
    ax_time.set_xticks(ax_time.get_xticks())
    ax_time.set_title(title, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    ax_time.set_xlabel('Years')
    ax_time.set_ylabel('Experiences')
    xlabels = [dt.strftime(mdates.num2date(d),'%Y') for d in ax_time.get_xticks()]
    ax_time.set_xticklabels(xlabels)
    ax_time.set_yticks(range(len(sorted_df_exp)),labels=sorted_df_exp['title'])
    plt.show()
    if save_path:
        timeline_fig.savefig(save_path, bbox_inches='tight')

def circle_experiences(df_exp,days_on_project,figsize,title,save_path=''):
    """A circular (radial) chart visualizing experiences by type, title, or role (from experiences.csv).
    
        - df_exp (dataframe): Dataframe with fields 'title'
        - days_on_project (list): List of days spend on project
        - figsize (tuple): Figure size as (width,height)
        - title (string): title of the plot
        - save_path (string): path to save the plot e.g. './timeline.svg'
    """
    circles = circlify.circlify(
        days_on_project.to_list(),
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )
    # Create just a figure and only one subplot
    fig_circle, ax_circle = plt.subplots(figsize=figsize)
    ax_circle.set_title(title, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
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
    if save_path:
        fig_circle.savefig(save_path, bbox_inches='tight')
    
def tree_skills(tmp,width=900,height=700,save_path=''):
    """A treemap showing experiences as top-level categories with nested skills (from experiences.csv).

        - tmp (dataframe): with level_1,level_2,level_3 data  
        - width (int,900): Width of the figure
        - height (int,700): Height of the figure  
        - save_path (string): path to save the plot e.g. './wordcloud_skills.svg'     
    """
    fig_tree = px.treemap(tmp, path=['level_1', 'level_2'], color='level_3', values='level_3',color_continuous_scale='greys',labels={'level_3': 'Days on experience'},width=width, height=height)
    fig_tree.update_layout(
     title={'text':'Experience and relevant skills',
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_tree.show()
    if save_path:
        fig_tree.write_image(save_path)

def wordcloud_skills(text,title,width=800,height=400,save_path=''):
    """A word cloud showing the most frequently used skills across experiences (from experiences.csv).
    
        - text (str): String with all text to be included in wordcloud
        - figsize (tuple): Figure size as (width,height)
        - title (string): title of the plot
        - save_path (string): path to save the plot e.g. './wordcloud_skills.svg'    
    """
    processed_text = WordCloud().process_text(text)
    wordcloud = WordCloud(width=width, height=height, background_color='black',color_func=lambda *args, **kwargs: 'white').fit_words(processed_text)

    fig_wordcloud, ax_wordcloud = plt.subplots(figsize=(10, 5))
    ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
    ax_wordcloud.axis('off') 
    ax_wordcloud.set_title(title, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=0.3))
    plt.show()
    if save_path:
        fig_wordcloud.savefig(save_path, bbox_inches='tight')