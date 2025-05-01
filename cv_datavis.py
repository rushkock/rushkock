

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
    from matplotlib.collections import PolyCollection
    from datetime import datetime as dt

    return WordCloud, dt, mdates, mo, plt


@app.cell
def _():
    import pandas as pd
    df = pd.read_csv("data/experiences.csv",delimiter=',',index_col=False)
    return df, pd


@app.cell
def _(df, dt, pd):
    df['start_date'] = df['start_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d'))
    df['end_date'] = df['end_date'].apply(func=lambda x: dt.strptime(x,'%Y-%m-%d') if not pd.isnull(x) else dt.now())

    return


@app.cell
def _(mo):
    mo.md('# Visualize Relevant Skills')
    return


@app.cell
def _(WordCloud, df, plt):
    type = 'skills'
    text = ' '.join(df[type].astype(str).tolist())
    processed_text = WordCloud().process_text(text)
    wordcloud = WordCloud(width=800, height=400, background_color='black',color_func=lambda *args, **kwargs: 'white').fit_words(processed_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off') 
    plt.show()
    return


@app.cell
def _(mo):
    mo.md('# Visualize Employment timeline')
    return


@app.cell
def _(df):
    df['diff'] = df['end_date'] - df['start_date']
    sorted_df = df.sort_values(by='start_date').reset_index()
    return (sorted_df,)


@app.cell
def _(df, dt, mdates, plt, sorted_df):
    timeline_fig, ax_time = plt.subplots(figsize=(8,6))
    for index, row in sorted_df.iterrows():
        start_year = mdates.date2num(row.start_date)
        duration = row['diff'].days
        ax_time.broken_barh([(start_year, duration)], 
                        (index-0.5,0.8), 
                        facecolors =('white'),
                       label=row.title)
    ax_time.set_xticks(ax_time.get_xticks())
    xlabels = [dt.strftime(mdates.num2date(d),'%Y') for d in ax_time.get_xticks()]
    ax_time.set_xticklabels(xlabels)
    ax_time.set_yticks(range(len(df)),labels=sorted_df['title'])
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
