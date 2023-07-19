"""
Module/Script Name: data_transformation.py

This code is a Flask application that processes data from a PostgreSQL database using the SQLAlchemy library. 
It performs various data transformations and uses the OpenAI GPT-3.5 language model to generate responses based 
on user prompts.


Dependencies:

-External Dependecies:
--Flask from flaskx: Flask module from the flask package. Flask is a popular web framework for Python. It is 
designed to build web applications and APIs quickly and with minimal code. Flask provides tools and libraries 
for handling routing, template rendering and request/response handling, making it easy to develop web 
applications in Python.

--pandas: pandas is a powerful data manipulation and analysis library for Python. It provides data structures 
and functions to efficiently handle and manipulate structured data, such as tables and time series. pandas is 
widely used for tasks like data cleaning, transformation, aggregation, and exploration.

--package DateRange from psycopg2.extras: The DateRange class is a data type provided by the psycopg2.extras
module, which is an extension package for the psycopg2 library (a PostgreSQL adapter for Python). The DateRange
class represents a range of dates and provides functionality to manipulate and compare date ranges. It can be 
used when working with PostgreSQL databases to handle date range queries.

--package create_engine from sqlalchemy: The create_engine function is part of the SQLAlchemy library, which is
a SQL toolkit and Object-Relational Mapping (ORM) library for Python. The create_engine function is used to
create a connection to a database engine. It takes a database URL or connection string as input and returns an 
engine object that can be used to interact with the database, execute SQL statements, and perform database
operations.

--openai:  This line imports the OpenAI library. OpenAI develops and provides artificial intelligence technologies, 
including natural language processing models. By importing the OpenAI library, you can utilize their models and APIs 
for various language-related tasks.

--from tenacity import ( retry, stop_after_attempt, wait_random_exponential): The tenacity library is a utility 
for adding retry logic to your Python code. By importing these elements, you can utilize the retry functionality, 
control the number of attempts, and define wait strategies for retries.

-Python Dependecies
--os: The os module in Python provides a way to interact with the operating system. It offers functions for 
working with files and directories, accessing environment variables, managing processes, and performing various 
system-related tasks. The os module is used to write portable code that can work across different operating systems.

--time: provides functions for working with time-related operations. The time module allows you to measure time 
intervals, pause program execution, and work with timestamps.

--datetime: provides classes and functions for manipulating dates and times, as explained earlier.

--schedule: provides a simple and intuitive way to schedule and run Python functions at specified intervals. The 
schedule module allows the creation of scheduled tasks and the automation of certain operations.


Usage:

 The data_transformation.py app needs only to be executed once, either by double-clicking it, by running the
command  python debugging_DataTransformation.py in the Windows Terminal or by accessing the port5000(or any other port you choose) 
 This code needs to be always running on the machine. It will execute its functionalities only if the time
and day are the same ones set in the function schedule_task() 


Author: Heinrich Edelmann, Daten Analyst


Date: 05.07.23

"""
from flask import Flask
import pandas as pd
from psycopg2.extras import DateRange
from sqlalchemy import create_engine
import os
import openai
import time
import datetime
import schedule
from tenacity import ( retry, stop_after_attempt, wait_random_exponential)  # for exponential backoff


# Timer
# Please be attentive when setting the timer, for if the timer is set to for example 3600s(1h) and it is set at 09:05, 
#the function will never be activated for it will never verify the day and time at 01:00, but at 01:05.
def schedule_task():
    today = datetime.date.today()
    if today.day == 6:
        schedule.every().day.at("01:00").do(process_data) # verify if the system date is the 1th at 1AM, if it is the process_data function will be activated
    while True: # infinite loop, 
        schedule.run_pending()
        time.sleep(900) # verify the if the if condition above is correct every 15Min (optional, it can be changed!)

# __name__ used when creating a Flask application instance to tell Flask where to find resources like templates and static files
app = Flask(__name__) 

# openAI-API-Key
openai.api_key = os.getenv('OPENAI_API_KEY', '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')

# Connection with the Database through the engine of the package sqlalchemy
engine = create_engine('postgresql://grafana:secret@localhost:5432/grafana') 


# Guidelines that will help build up the Requests that will be sent to ChatGPT
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
how_to_interpret_theInput = "I'm going to show you a row from my table. The table has 2 columns separated by a tilde. Replace the content of the 1st column, do it based on the content of the second column. The 1st column can have only one word in it. Consider all of the following rules:"
Regeln_fürAufplittung_vonGeneral_undInternalProjects = '''
if you can't apply any of the changes below please change 1st column value to 'Others'!
-change 1st column value to 'Meetings' if: you find the word 'meeting', or 'meetings' (case insensitive).
-change 1st column value to 'Crypto' if: you find anything related to crypto currencies or the word 'crypto' (case insensitive).
-change 1st column value to 'Cardgame' if you find anything related to Cardgame, or the words 'cardgame', 'card', 'game' themselves (case insensitive) in the second column.
-change 1st column value to 'Controlling': if you find any word related to finances or control of finances, words either in english or in german, like 'Lohnzettel', 'Lohnverrechnung','taxes', etc. Also if you find any 'dr notar' or anything related to 'dr' (cos 'dr' should be interpreted here as the word 'Doctor') or bureaucracy related topics/words.
-change 1st column value to 'WavectNFT': if you find anything related to the topic NFTs in the second column, like the word 'NFT' itself.
-change 1st column value to 'IT': if you find anything related to configure, set up, Setup, test, training, check, Checkup, push, internal or fix something in the second column (case insensitive). There are also some other words you should consider, like Clockify (which is a programm used to log the work hours). Please check in your database if the content is related to any type of programm or programming tools...
-change 1st column value to 'Workshops': if you find the words 'web2', 'web3' or the word 'workshop' itself in the second column. Also if you find anything related to workshops in the second column.
-change 1st column value to 'Course': if you find anything related to words like 'learning', 'research', 'knowledge', 'information', 'read' in the second column. Also if you find the name of other programming languages, words related to the topic learn or the word 'Hackathon'.
Following are the rows I mentioned:
'''
Regeln_fürAufplittung_vonMarketing = '''
-change 1st column value to 'Podcast': if you find the word 'podcast' (case insensitive)
-change 1st column value to 'Course': in case you stumble upon the words 'eip', 'Security Course' or'Preparation' written in any form, look also for abbreviations for preparation (case insensitive).
-change 1st column value to 'Social Media': if you find any words that can be related to a function in social networks like Instagram and Facebook, like 'post', 'shorts', 'short', etc ( (case insensitive)). Also if you find the word 'Social Media' (case insensitive).
-change 1st column value to 'Linked_in': the word 'linkedin' written in any form. Also look for any types of possible abbreviations for 'linkedin', like 'li', 'Li', etc  (case insensitive).
-change 1st column value to 'Talks': if you find anything related to talks (as an event) or that can be connected to speaker events  (case insensitive).
-change 1st column value to 'Others' if: you can't apply any of the changes mentioned before or if you find very general words like 'all','general','stuff', 'daily', ' ', etc (case insensitive).
Following are the rows I mentioned:
'''
request_for_no_comments = "Check if the 1st column has only 1 word per row and provide only the 1st column of the new row."
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Defining a route (or URL) endpoint for the Flask web server where the process for the transformation of the data is stored and
#is activated by the function schedule()
@app.route('/process')
def process_data():
    @retry(wait=wait_random_exponential(min=1, max=100), stop=stop_after_attempt(99))
    def completions_with_backoff(prompt, max_tokens=1000):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Data Analyst that provides results of requests without saying anything more."},
                {"role": "user", "content": prompt}
                     ],
            max_tokens=max_tokens,
            )
        return response.choices[0].message
    
    try:
        # Download of the data that was prior in the Database
        with engine.connect() as conn:
            table_KPIHistory = pd.read_sql('SELECT * FROM "KPIHistory"', conn)
            table_KPIs = pd.read_sql('SELECT * FROM "KPI"', conn)
            table_Currency = pd.read_sql('SELECT * FROM "Currency"', conn)
            table_TimePerProject = pd.read_sql('SELECT * FROM "TimePerProject"', conn)

        # for a better visualization the column entsprechendMonat is created in the TimePerProject table
        table_TimePerProject["entsprechendMonat"] = [ "Januar" if r == DateRange(datetime.date(2023, 1, 1), datetime.date(2023, 2, 1), '[)') 
                                                     else "Februar" if r ==  DateRange(datetime.date(2023, 2, 1), datetime.date(2023, 3, 1), '[)')
                                                     else "März" if r ==  DateRange(datetime.date(2023, 3, 1), datetime.date(2023, 4, 1), '[)') 
                                                     else "April" if r ==  DateRange(datetime.date(2023, 4, 1), datetime.date(2023, 5, 1), '[)')
                                                     else "Mai" if r ==  DateRange(datetime.date(2023, 5, 1), datetime.date(2023, 6, 1), '[)')
                                                     else "Juni" if r ==  DateRange(datetime.date(2023, 6, 1), datetime.date(2023, 7, 1), '[)')
                                                     else "Juli" if r ==  DateRange(datetime.date(2023, 7, 1), datetime.date(2023, 8, 1), '[)') 
                                                     else "August" if r ==  DateRange(datetime.date(2023, 8, 1), datetime.date(2023, 9, 1), '[)')
                                                     else "September" if r ==  DateRange(datetime.date(2023, 9, 1), datetime.date(2023, 10, 1), '[)')
                                                     else "Oktober" if r ==  DateRange(datetime.date(2023, 10, 1), datetime.date(2023, 11, 1), '[)')
                                                     else "November" if r ==  DateRange(datetime.date(2023, 11, 1), datetime.date(2023, 12, 1), '[)')
                                                     else "Dezember" for r in table_TimePerProject["MonthYear"]
                                                    ]
        
        #  For the later merge of the tables KPI and KPIHistory the column 'ID' is renamed to 'KPI_ID', for 'KPI_ID' exists in the KPIHistory
        #table and represents the same value as 'ID' in KPI
        table_KPIs.rename(columns = {'ID':'KPI_ID'}, inplace = True)
        # for the merge to work both tables need to have the same named column. 
        # Through the merge of both tables KPI und KPI_History the table table_costs_and_incomesources is created for the analysis and creation
        #of visualizations later
        table_costs_and_incomesources = pd.merge(table_KPIHistory[["KPI_ID", "Value", "Date", "CurrencyID"]],
                                                  table_KPIs[["KPI_ID", "Title"]],
                                                    on="KPI_ID") 
        # for a better visualization the column entsprechendMonat is created in the table table_costs_and_incomesources   
        table_costs_and_incomesources["entsprechendMonat"] = [
            "Januar" if r == datetime.date(2023, 2, 1) else
            "Februar" if r == datetime.date(2023, 3, 1) else
            "März" if r == datetime.date(2023, 4, 1) else
            "April" if r == datetime.date(2023, 5, 1) else
            "Mai" if r == datetime.date(2023, 6, 1) else
            "Juni" if r == datetime.date(2023, 7, 1) else
            "Juli" if r == datetime.date(2023, 8, 1) else
            "August" if r == datetime.date(2023, 9, 1) else
            "September" if r == datetime.date(2023, 10, 1) else
            "Oktober" if r == datetime.date(2023, 11, 1) else
            "November" if r == datetime.date(2023, 12, 1) else
            "Dezember" for r in table_costs_and_incomesources["Date"]
        ]

        # 2 tables are created for the later creation of calculated tables, one table with only the costs and one with only the income values
        table_costs = table_costs_and_incomesources[table_costs_and_incomesources["Title"].str.contains('Costs|costs|Cost|cost|expenses', regex=True)]
        table_income = table_costs_and_incomesources[~table_costs_and_incomesources["Title"].str.contains('Costs|costs|Cost|cost|expenses', regex=True)]

        # Cleaning data from typos
        table_TimePerProject["Project"] = table_TimePerProject["Project"].replace("internal projects", "Internal Projects")
        table_TimePerProject["Project"] = table_TimePerProject["Project"].replace("Internal projects", "Internal Projects")
        table_TimePerProject["Project"] = table_TimePerProject["Project"].replace("DebtRay ", "DebtRay")
        table_TimePerProject["Project"] = table_TimePerProject["Project"].replace("MartinDionne", "Martin Dionne")


        # Separating the data in different tables to minimize the number of requests to be sent to ChatGPT,
        # not to mention the named projects don't need to be sorted so their rows need to be maintened untouched.

        df_general_internalprojects = table_TimePerProject[(table_TimePerProject["Project"] == "General") | (table_TimePerProject["Project"] == "Internal Projects")]
        #putting projects wrongliy saved in "General" or "Internal Projects" back to the correct project
        for p in table_TimePerProject["Project"].unique(): 
            df_general_internalprojects.loc[df_general_internalprojects["Description"].str.contains(f'(?i).*{p}.*|{p}.*|.*{p}'), 'Project'] = p

        # The data must be separated in smaller dataframes to not overload the servers of ChatGPT
        df_general = df_general_internalprojects[(df_general_internalprojects["Project"] == "General")]
        df_internalprojects = df_general_internalprojects[df_general_internalprojects["Project"] == "Internal Projects"]
        df_marketing = table_TimePerProject[table_TimePerProject["Project"] == "Marketing"]
        df_restZeilen = table_TimePerProject[ (table_TimePerProject["Project"] != "General") 
                                             & (table_TimePerProject["Project"] != "Internal Projects") 
                                             & (table_TimePerProject["Project"] != "Marketing") ]
        #restZeilen contains each of the already named projects that wavecr.io is or was working on


        # ChatGPTs Part:
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         Separation of the under "General" logged projects into the categories: 
#       'Meetings', 'Crypto', 'Cardgame', 'Controlling', 'WavectNFT', 'IT', 'Workshops', 'Course', 'Others'.

#         The requests that will be sent on ChatGPT need to be a string value. So the requests are formed with the sum of the strings:
#  
#       * how_to_interpret_theInput → tells ChatGPT how to interpret the row that will be sent to him;
#       * Regeln_fürAufplittung_vonGeneral_undInternalProjects / Regeln_fürAufplittung_vonMarketing → rules for the sorting into new
#       categories that were created in colaboration with Waveact.io;
#       * row_str → this string is built with the join of the content of the columns "Project" and "Description" separated by a tilde 
#       "~". ChatGPT is made aware of it in the string how_to_interpret_theInput;
#       * request_for_no_comments → requests ChatGPT to give the answer I need alone, without any additional comments;

#       Why are there 2 sets of rules you might ask?
#      A.: Cause the rules for the under 'Marketing' logged projects differ from those meant to 'General' and 'Internal Projects',
#      the request sent for the 'Marketing' rows uses the string Regeln_fürAufplittung_vonMarketing instead of Regeln_fürAufplittung_vonGeneral_undInternalProjects
#       'Marketing' will be separated into the categories: 'Podcast','Course','Social Media','Linked_in','Talks','Others'

        # Sorting of "General"
        list_mit_transformiertenZeilen_General = []
        for index, row in df_general[["Project","Description"]].iterrows():
            row_str = '~'.join(row.astype(str))
            anforderung = how_to_interpret_theInput + Regeln_fürAufplittung_vonGeneral_undInternalProjects + row_str  + request_for_no_comments 
            completion_text = completions_with_backoff(anforderung, max_tokens=1000)
            list_mit_transformiertenZeilen_General.append(completion_text["content"])

        valid_projects = ['Meetings', 'Crypto', 'Cardgame', 'Controlling', 'WavectNFT', 'IT', 'Workshops', 'Course', 'Others']

       # The original values are replaced with the new values from ChatGPT
        df_general["Project"] = list_mit_transformiertenZeilen_General
       # In the case that ChatGPT doesn't sort any row correctly, cos this can happen, the not sorted row will be put on the project "Others" 
       #for the analysis.
        df_general.loc[~df_general['Project'].isin(valid_projects), 'Project'] = 'Others' 

        # Sorting of "Internal Projects" 
        list_mit_transformiertenZeilen_InternalProjects =[]
        for index, row in df_internalprojects[["Project","Description"]].iterrows():
            row_str = '~'.join(row.astype(str))
            anforderung = how_to_interpret_theInput + Regeln_fürAufplittung_vonGeneral_undInternalProjects + row_str  + request_for_no_comments
            completion_text = completions_with_backoff(anforderung, max_tokens=1000)
            list_mit_transformiertenZeilen_InternalProjects.append(completion_text["content"])

       # The original values are replaced with the new values from ChatGPT
        df_internalprojects["Project"] = list_mit_transformiertenZeilen_InternalProjects
       # In the case that ChatGPT doesn't sort any row correctly, cos this can happen, the not sorted row will be put on the project "Others" 
       #for the analysis.
        df_internalprojects.loc[~df_internalprojects['Project'].isin(valid_projects), 'Project'] = 'Others' 

        # Sorting of "Marketing" 
        list_mit_transformiertenZeilen_Marketing = []
        for index, row in df_marketing[["Project","Description"]].iterrows():
            row_str = '~'.join(row.astype(str))
            anforderung = how_to_interpret_theInput + Regeln_fürAufplittung_vonMarketing + row_str  + request_for_no_comments 
            completion_text = completions_with_backoff(anforderung, max_tokens=1000)
            list_mit_transformiertenZeilen_Marketing.append(completion_text["content"])

       # The original values are replaced with the new values from ChatGPT
        df_marketing["Project"] = list_mit_transformiertenZeilen_Marketing
        valid_projects_marketing = ['Podcast','Course','Social Media','Linked_in','Talks','Others']
       # In the case that ChatGPT doesn't sort a row correctly, cos this can happen... the not sorted row will be put on the project "Others" 
       #for the analysis.
        df_marketing.loc[~df_marketing['Project'].isin(valid_projects_marketing), 'Project'] = 'Others' 

       # All the new categorized tables are brought together into one table. A Table that will be used for the Data Transformation and Data Analysis
        verarbeitete_df_TimePerProject = pd.concat([df_general, df_internalprojects, df_marketing, df_restZeilen], axis=0)
        verarbeitete_df_TimePerProject.sort_index(inplace=True)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Perform the necessary transformations on the tables:



        # Reindexing of the DataFrame with the new order "new_order", to put the months into their correct order in the year cos
        #somehow "Januar" were loggend second to "Februar", so this new_order will bring the months into the correct order
        new_order = [1,0,2,3,4,5,6,7,8,9,10,11] 

        # month_mapping is used to transform months into month numbers, these will be necessary for the correlation matrix
        month_mapping = {
            'Januar': 1,
            'Februar': 2,
            'März': 3,
            'April': 4,
            'Mai': 5,
            'Juni':6,
            'Juli':7,
            'August':8,
            'September':9,
            'Oktober':10,
            'November':11,
            'Dezember':12
        }

        # the costs per month are calculated and put into a pivot table
        pivot_table_gesamteKosten = pd.pivot_table(table_costs, values='Value', index="entsprechendMonat", columns='Title', aggfunc='sum')
        pivot_table_gesamteKosten = pivot_table_gesamteKosten.reset_index().reset_index(drop=True)
        # the new costs table is reindexed with the new_order list and the result is put into the variable gesamteKosten
        gesamteKosten = pivot_table_gesamteKosten.reindex(new_order)
        gesamteKosten = gesamteKosten.reset_index(drop=True)
        # The table gesamteKosten will be important for the creation of the tables that shall be uploaded into the Database.

        # the costs per month are calculated and put into a pivot table
        table_gesamteEinkommen = pd.pivot_table(table_income, values='Value', index="entsprechendMonat", columns='Title', aggfunc='sum')
        table_gesamteEinkommen = table_gesamteEinkommen.reset_index().reset_index(drop=True)
        # the new income table is reindexed with the new_order list and the result is put into the variable gesamteEinkommen
        gesamteEinkommen = table_gesamteEinkommen.reindex(new_order)
        gesamteEinkommen = gesamteEinkommen.reset_index(drop=True)
        # The table gesamteEinkommen will be important for the creation of the tables that shall be uploaded into the Database.

        # Function that calculates the amount of hours spent in each project
        def gearbeiteteStunden_nachProjekt(monat):
            try:
                df = verarbeitete_df_TimePerProject[verarbeitete_df_TimePerProject["entsprechendMonat"] == monat]
                result = []
                for e in df["Project"].unique():
                    total_hours = df[df["Project"] == e]["Time (h)"].sum()
                    total_hours_decimal = df[df["Project"] == e]["Time (decimal)"].sum()
                    result.append([e, total_hours, total_hours_decimal, monat])
                return pd.DataFrame(result, columns=["Project", "Total Hours", "Time (decimal)", "Month"])
            except:
                return f'Bitte geben Sie den Monat als String ein, wie z.B.: gearbeiteteStunden_nachProjekt("Februar")'
            
        months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        # list to store the DataFrames for each month
        dfs = []
        # Iteration over the months and creation of DataFrames
        for month in months:
            df_gearbeiteteStunden_nachProjekt = pd.DataFrame(gearbeiteteStunden_nachProjekt(month))
            dfs.append(df_gearbeiteteStunden_nachProjekt)
        # Concatenate all the previously created DataFrames with the amount of hours per Project
        total_hours = pd.concat(dfs, axis=0).reset_index(drop=True)
        # the monthly amount of worked hours is then calculated using a pivot table and stored in the gesamteStunden variable
        gesamteStunden = pd.pivot_table(total_hours, values='Time (decimal)', index="Month", aggfunc='sum').reset_index()
        gesamteStunden = gesamteStunden.reindex(new_order)
        gesamteStunden = gesamteStunden.reset_index(drop=True)
        gesamteStunden.dropna(inplace=True)

        # amount of hours spent on each project in calculated in stored in the variable gesamte_hoursperProject_andMonth for latter use
        hoursperProject_andMonth = pd.pivot_table(total_hours, values='Time (decimal)', index="Month", columns="Project", aggfunc='sum').reset_index()
        hoursperProject_andMonth = hoursperProject_andMonth.fillna(0)
        gesamte_hoursperProject_andMonth = hoursperProject_andMonth.reindex(new_order)
        gesamte_hoursperProject_andMonth = gesamte_hoursperProject_andMonth.reset_index(drop=True)

        # creation of the table Einkommen_Kosten_Stunden for the later creation of the table für_dieKorrelation,
        #that contains the total amount of hours per project and costs and incomes per Month.
        Einkommen_Kosten_Stunden = pd.concat([gesamteKosten, gesamteEinkommen.drop(columns="entsprechendMonat"), 
                                gesamteStunden["Time (decimal)"]],axis=1).reset_index(drop=True)
        Einkommen_Kosten_Stunden["Profit"] = Einkommen_Kosten_Stunden["Monthly Revenue"] - (Einkommen_Kosten_Stunden["Monthly Employee Costs"] + Einkommen_Kosten_Stunden["Monthly Freelancer costs"] + Einkommen_Kosten_Stunden["Other expenses"])
        Einkommen_Kosten_Stunden.reset_index(drop=True)

        gesamte_hoursperProject_andMonth["Month"] = gesamte_hoursperProject_andMonth["Month"].replace(month_mapping)
        # Replace the values in the "entsprechendMonat" column cos a Correlation Matrix was done with this table and a Correlation Matrix
        #can only be calculated when the table only 
        Einkommen_Kosten_Stunden['entsprechendMonat'] = Einkommen_Kosten_Stunden['entsprechendMonat'].replace(month_mapping)
        Einkommen_Kosten_Stunden.dropna(inplace=True)

        # für_dieKorrelation contains the total income and costs per Month and the amount of hours per project in each month
        für_dieKorrelation = pd.concat([Einkommen_Kosten_Stunden, gesamte_hoursperProject_andMonth.drop(columns="Month")], axis=1)
        columns = für_dieKorrelation.columns.tolist()
        # putting some column at the end of the table for a better visualization of the correlation matrix
        columns.remove('Monthly Employee Costs')
        columns.remove('Monthly Freelancer costs')
        columns.remove('Other expenses')
        columns.remove('Profit')
        columns.remove('Monthly Revenue')
        columns.extend(['Monthly Employee Costs','Monthly Freelancer costs','Other expenses','Profit','Monthly Revenue'])
        für_dieKorrelation = für_dieKorrelation[columns]
        für_dieKorrelation.dropna(inplace=True)


        # Calculation of the income brought by the projects paid by the hour, the time spent on them and by who worked on them
        hourly_paid_projects = verarbeitete_df_TimePerProject[verarbeitete_df_TimePerProject['Project'].isin(['Boba', 'FTWDao'])]
        grouped_data_hourly_paied_projects = hourly_paid_projects.groupby(['Project', 'entsprechendMonat', 'Person']).agg(
                                                                                                    TotalHours=('Time (decimal)', 'sum')
                                                                                                ).reset_index()
        # New projects can be added to this function, if their hourly rate is known...
        def calculate_total_amount(row):
            if row['Project'] == 'Boba':
                return 80 * row['TotalHours']
            elif row['Project'] == 'FTWDao':
                return 113.40 * row['TotalHours']
            else:
                return None
        grouped_data_hourly_paied_projects['TotalAmount'] = grouped_data_hourly_paied_projects.apply(calculate_total_amount, axis=1)
        ohnequivr = grouped_data_hourly_paied_projects.sort_values(by='entsprechendMonat')


        # Calculation of the income brought by the projects paid monthly, the time spent on them and by who worked on them
        monthly_paid_projects = verarbeitete_df_TimePerProject[verarbeitete_df_TimePerProject['Project'] == 'Quivr']
        grouped_data_monthly_paid_projects = monthly_paid_projects.groupby(['Person', 'entsprechendMonat', 'Project']).agg(
                                                                                                TotalHours=('Time (decimal)', 'sum')
                                                                                                ).reset_index()
        grouped_data_monthly_paid_projects['TotalAmount'] = grouped_data_monthly_paid_projects.groupby('entsprechendMonat')['TotalHours'].transform(
                                                                                                            lambda x: 7288.91 * x / x.sum()
                                                                                                            )
        sofarnurquivr = grouped_data_monthly_paid_projects.sort_values(by=['Person', 'entsprechendMonat'])

        # The table Data_mit_Umsätze is then created with all the values of income and time sorted by month and worker
        Data_mit_Umsätze = pd.concat([ohnequivr, sofarnurquivr])
        Data_mit_Umsätze.reset_index(inplace=True)
        Data_mit_Umsätze.sort_values(by="Project", inplace=True)
        Data_mit_Umsätze.drop(columns="index", inplace=True)

        # investierteZeit_inSocialMedia table is created for the visualization of the time spent in the Marketing campaigns
        Zeit_ = pd.pivot_table(verarbeitete_df_TimePerProject, values='Time (decimal)', index='entsprechendMonat', columns='Project', aggfunc='sum')
        investierteZeit_inSocialMedia = Zeit_[['Podcast','Linked_in','Workshops','Social Media']]
        investierteZeit_inSocialMedia.reset_index(inplace=True)
        investierteZeit_inSocialMedia.loc[:, :] = investierteZeit_inSocialMedia.fillna(0)



        # Upload the resulting tables from the Data Transformation to the database
        with engine.connect() as conn:
            Data_mit_Umsätze.to_sql('data_mit_umsätze', conn, if_exists='replace', index=False)
            für_dieKorrelation.to_sql('Stunden_und_Umsätze', conn, if_exists='replace', index=False)
            investierteZeit_inSocialMedia.to_sql('investierteZeit_inSocialMedia', conn, if_exists='replace', index=False)
            table_costs_and_incomesources.to_sql('Costs_and_Incomeavenues', conn, if_exists='replace', index=False)

        return 'Process completed, die Tabellen data_mit_umsätze, Stunden_und_Umsätze, investierteZeit_inSocialMedia und Costs_and_Incomeavenues wurden hochgeladen und können in Grafana visualisiert werden'

    except Exception as e:
        return f'Error: {e}'




if __name__ == '__main__': #  accessing the port5000(optional, one can also use other ports) 
    app.run(port=5000)     # will execute the application
    schedule_task()

