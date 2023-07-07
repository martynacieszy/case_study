# Case study

The description of this case study can be found in Data_Analyst_Case v2.docx.
The source data for the task was stored in: Airbnb_data_New_York.csv, Property_sales_data_New_York.csv, Weather Data.xlsx.

The case study was devided into two main scripts:
1. Input_data.ipynb
2. Case_study_app.py

In the first script the source data was read, transformed to dataframe and manipulated to acheive the best data quality. It was conducted using Jupyter Notebook.
Output from this procedure is stored as sales_NY.json and airbnb_NY.json. Data from Weather Data.xlsx was not used for this study.
Basing on two mentioned .json files the Case_study_app.py was launched in Streamlit Community Cloud from GitHub executing several functions and resulting in the Streamlit app that can be found on the page: 
https://casestudy-drj4kvlwuew.streamlit.app/ 

To see the results it is not necesarry to run all codes, but to visit the Streamlit app from the link.

File .mapbox_token and requirements.txt are needed to run the app.
