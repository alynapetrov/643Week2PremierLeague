import pandas as pd
import numpy as np
import altair as alt
import argparse
from typing import List


def load_data(files: List[str]) -> pd.DataFrame:
    """
    Loading data from csv files into a pandas df.
    """
    colsToKeep = ['h.title', 'a.title', 'goals.h', 'goals.a', 'xG.h', 'xG.a']
    xGData = pd.DataFrame()
    for i in files:
        #data = pd.read_csv(f'PL_data/EPL_{i}_matches.csv')
        data = pd.read_csv(i)
        data = data[colsToKeep]
        # Adding a col to keep track of season
        season = int(i.split('/')[-1].split('_')[1])
        data['season'] = season
        xGData = pd.concat([xGData, data], ignore_index=True)
    return xGData

def clean_data(xGData: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning the data
    """
    # Only keeping teams that were in Premier League all 4 seasons (2016-2019)
    xGoals = xGData.groupby('a.title')
    # This filter function give us only teams that have 4 unique seasons (2016-2019)
    xGoals = xGoals.filter(lambda x: x['season'].nunique() == 4)
    # Adding a data column to represent the difference between away xG and actual away goals.
    xGoals['awayGoalDif'] = xGoals['goals.a'] - xGoals['xG.a']
    xGoals.rename(columns={'a.title': 'team'}, inplace=True)
    # Aggregating our data to get mean of difference between away xG and actual away goals for each season
    xGoals = xGoals.groupby(['season','team']).agg(avgDif=('awayGoalDif','mean')).reset_index()
    return xGoals

def make_heatmap(xGoals: pd.DataFrame) -> alt.Chart:
    """
    Creating a heatmap
    """
    vis = alt.Chart(xGoals).mark_rect().encode(
        x=alt.X("team:N",title='Team', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('season:N', title='Year'),
        # Scale is the color scale we want to use, legend allows us to title the scale
        color=alt.Color('avgDif:Q', scale=alt.Scale(scheme="redyellowgreen"),legend=alt.Legend(title="Avg Goal Difference"))
    ).properties(
        # Setting title and size
        title='Average Difference Between Expected Away Goals and Actual Away Goals',width=1150, height=300
    )
    # Bold text overlay to show the difference value within the squares
    text = vis.mark_text(fontWeight='bold').encode(
        x=alt.X("team:N",title='Team', axis=alt.Axis(labelAngle=0)), 
        y=alt.Y('season:N', title='Year'),
        text=alt.Text('avgDif:Q', format='.2f'),
        color=alt.value('black'),
    )
    return vis+text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_data", nargs='+', help="EPL match raw files")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()
    # Loading the data
    data = load_data(args.raw_data)
    # Cleaning the data
    xGoals = clean_data(data)
    # Making the heatmap and saving it to the output file
    heatmap = make_heatmap(xGoals)
    heatmap.save(args.output)
