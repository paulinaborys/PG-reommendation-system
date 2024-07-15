# Recommendation System for University Candidates

This project is a prototype recommendation system designed to help candidates determine their suitability for various courses at Gdańsk University of Technology.

## Table of Contents

- [About](#about)
- [Setup](#setup)

## About
This project aims to create a web application that implements a recommendation tool for prospective students at Gdańsk University of Technology. The system leverages exploratory data analysis from the MojaPG system to provide personalized recommendations.

### Inputs:
- 5 preferred fields of study
- Number of points obtained in the admission process
### Outputs:
- Recommendation of the field of study with the highest success rate
- Recommendation of the field of study with the highest predicted average score
- Visualization of exploratory analysis results for each of the selected fields of study
### Important Note:
This is a prototype system that does not return actual results because the data from the MojaPG system is private and protected. The names of the tables in the database and the specific data are confidential and not authorized for public sharing. This prototype is intended for demonstration purposes only and does not access or use any real candidate or university data.

## Setup
### Set up a virtual environment
python3 -m venv venv

### Activate the virtual environment
source venv/bin/activate

### Install the required dependencies
pip install -r requirements.txt

### Start application
(venv) $ python app.py
