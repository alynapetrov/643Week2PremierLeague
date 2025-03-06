"""
    Script for taking raw Premier League season data and generating a heatmap
    displaying the difference between expected and actual away goals for each team.
"""

import argparse
from typing import List
import pandas as pd
import altair as alt


def load_data(files: List[str]) -> pd.DataFrame:
    """
    Loading data from csv files into a pandas df.
    """
    cols_to_keep = ['h.title', 'a.title', 'goals.h', 'goals.a', 'xG.h', 'xG.a']
    x_data = pd.DataFrame()
    # Going through each file from the input list
    for i in files:
        data = pd.read_csv(i)
        data = data[cols_to_keep]
        # Adding a col to keep track of season
        season = int(i.split('/')[-1].split('_')[1])
        data['season'] = season
        x_data = pd.concat([x_data, data], ignore_index=True)
    return x_data

def clean_data(x_g_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning the data
    """
    x_goal = x_g_data.groupby('a.title')
    # This filter function gives us only teams that were in each season (every input file)
    x_goal = x_goal.filter(lambda x: x['season'].nunique() == x_g_data['season'].nunique())
    # Adding a data column to represent the difference between away xG and actual away goals.
    x_goal['awayGoalDif'] = x_goal['goals.a'] - x_goal['xG.a']
    x_goal.rename(columns={'a.title': 'team'}, inplace=True)
    # Aggregating our data to get mean of difference between away xG and actual away goals
    x_goal = x_goal.groupby(['season','team']).agg(avgDif=('awayGoalDif','mean')).reset_index()
    return x_goal

def make_heatmap(x_goal: pd.DataFrame) -> alt.Chart:
    """
    Creating a heatmap
    """
    vis = alt.Chart(x_goal).mark_rect().encode(
        x=alt.X("team:N",title='Team', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('season:N', title='Year'),
        # Scale is the color scale we want to use, legend allows us to title the scale
        color=alt.Color('avgDif:Q',
                        scale=alt.Scale(scheme="redyellowgreen"),
                        legend=alt.Legend(title="Avg Goal Difference")
                       )
    ).properties(
        # Setting title and size
        title='Average Difference Between Expected Away Goals and Actual Away Goals',
        width=1150, height=300
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
    rawdata = load_data(args.raw_data)
    # Cleaning the data
    x_goals = clean_data(rawdata)
    # Making the heatmap and saving it to the output file
    heatmap = make_heatmap(x_goals)
    heatmap.save(args.output)
