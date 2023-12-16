# Python-507-Final-Project
Final Project
# Data Analysis Dashboard README

## Introduction
This is a Data Analysis Dashboard application that allows users to analyze stock or economic data and generate word clouds based on Reddit posts related to a company or keyword.

## Features
- Retrieve and display stock or economic data.
- Generate word clouds from Reddit posts.
- Choose between stock or economic data analysis.
- Specify search term, start date, and end date for analysis.


## Prerequisites
Before running the application, make sure you have the following dependencies installed:
- Python 3
- Flask
- pandas
- matplotlib
- wordcloud
- yfinance
- praw
- nltk
- selenium (for automated web interaction)

You also need to obtain API keys for Fred and Reddit, and update the `Keys.py` file accordingly.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
pip install Flask pandas matplotlib wordcloud yfinance praw nltk selenium
3. Update the `Keys.py` file with your API keys.

## Usage
1. Run the application by executing `Main_Program.py` in your terminal.
2. Access the dashboard in your web browser at `http://127.0.0.1:5000/`.
3. Choose an option (Stock or Economic Data).
4. Enter a search term, start date, and end date.
5. Click the "Search" button to generate charts and word clouds.
6. To exit the program, click the "Exit Program" button on the Wordcloud page.
