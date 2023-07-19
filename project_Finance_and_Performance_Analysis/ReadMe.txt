Code-Documentation: Description of the functionality of the code


This code is a Flask application that processes data from a PostgreSQL database using the SQLAlchemy library. It performs various data transformations and uses the OpenAI GPT-3.5 language model to generate responses based on user prompts.

The code imports several required libraries, including Flask, pandas, datetime, psycopg2, sqlalchemy, os, openai, time, schedule, and tenacity.

The schedule_task() function is defined to schedule a task to run at 2:00 AM on the first day of every month. It uses the schedule library to set up the scheduling and the time library to add a delay between each check.

The Flask application is created using Flask(__name__), which sets up the Flask instance and provides the necessary resources for templates and static files.

The OpenAI API key is retrieved from the environment variable OPENAI_API_KEY or set to a default value if not found. The PostgreSQL database connection is created using the create_engine function from SQLAlchemy.

The code defines several string variables that serve as instructions or rules for processing the data. These include how_to_interpret_theInput, Regeln_fürAufplittung_vonGeneral_undInternalProjects, and Regeln_fürAufplittung_vonMarketing. These variables contain guidelines for splitting the data into different categories based on specific rules.

The /process route is defined as a Flask route that processes the data. It uses the process_data() function as the route handler. Within this function, there is a nested function completions_with_backoff() that handles the interaction with the OpenAI GPT-3.5 model. It uses the retry decorator from the tenacity library to implement exponential backoff and retry logic in case of any API errors and to avoid the RateLimitError the programm is put in a pause until the server recovers or reset the RateLimit for the provided OpenAI-API.

The function connects to the PostgreSQL database using the create_engine object and retrieves data from several tables using SQL queries. The retrieved data is stored in Pandas DataFrames for further processing.

The code performs various data cleaning and transformation steps, such as replacing values in columns, separating data into different DataFrames based on project categories, and applying specific rules for splitting the data.

The ChatGPT model is used to process the data in the "General", "Internal Projects" and "Marketing" categories, where for the categorization of "General" and "Internal Projects" the same rules are applied whereas "Marketing" has its own set of rules. For each row in these DataFrames, a prompt is constructed based on the rules and the row's content in the column "Description". The completions_with_backoff() function sends the prompt to the GPT-3.5 model and retrieves the response. The transformed rows are stored in separate lists.

Finally, the transformed data is assigned back to the original DataFrames, and any rows that were not sorted correctly are assigned to the "Others" category. This ensures that all rows have a valid project category.