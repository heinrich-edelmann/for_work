-- this project consists in webscraping Wikipedia for data, creating a FASTAPI, uploading the data using this API and the building of a log system, where everytime when any type of change was made in the uploaded files (like deleting files or uploading new ones) a log entry should be automatically made, stating the type of change and when the change was made.


-- the files are organized as follows:

- fastapi_aufgabe  →  the code containing the webcraping and the log-system
- import_uvicorn  →  creation of the hosting server
- Aufgabe_API_log.docx  →  the actual exercises and questions for this project