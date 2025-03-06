# 643Week2PremierLeague

## Introduction
This file script.py loads, cleans, and outputs a heatmap visualization for Premier League matches for any desired combination of years from 2016 to 2019. It reads in raw data files containing goals for each match in a season, filters to only contain teams that were in each season, calculates the difference between actual away goals and expected away goals, and then creates a heapmap visualization to show the means of those calculations by team. 

## Environment Setup
To run this script, make sure that Python is installed. Required packages needed to run the scrupt are pandas, altair, and argparse. To install these, run the following command in a terminal:

pip install pandas altair argparse

Make sure that the files within the PL_data folder of this repo are also downloaded in the environment.

## Script Functionality
The script contains a load_data function, which reads a list of csv files containing Premier League match data for a season. It extracts the needed columns containing home team, away team, and their respective goals for a match. The clean_data function filters teams that were in each season of the given input files and calculates the difference between expected and actual away goals for a team within a season. The make_heatmap function create a heatmap visual showing these calculated results. 

To run the script, you can use the following command:
python script.py PL_data/EPL_2016_matches.csv PL_data/EPL_2017_matches.csv PL_data/EPL_2018_matches.csv PL_data/EPL_2019_matches.csv out.html

Any combinations of files for 2016-2019 as inputs will work similarly.

To see the created heatmap, download the output html in open in in a supported environment (such as Chome). 
