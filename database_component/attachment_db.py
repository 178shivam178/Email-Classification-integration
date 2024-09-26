import mysql.connector
import os
from dotenv import load_dotenv
import json

load_dotenv()

if not os.path.exists('logs'):
    os.makedirs('logs')

def log_error(message):
    with open('logs/attachment_db.txt', 'a') as log_file:
        log_file.write(message + "\n")

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST'),
            user=os.getenv('DBUSER'),
            password=os.getenv('DBPASS'),
            database=os.getenv('DATABASE')
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        log_error(f"Error connecting to database: {err}")
        return None  

def insert_data_attachment(data):
    """Insert user data and associated companies and projects into the database."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            log_error("No connection could be established.")
            return  

        cursor = connection.cursor()
        user_query = """
        INSERT INTO Users (Name, Email, Phone, Total_Experience, LinkedIn_Profile, Education, Hackathons_and_Achievements, Activities_and_Interests) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        user_values = (
            data['Name'],
            data['Email'],
            data['Phone'],
            data['Total_Experience'],
            data['LinkedIn_Profile'],
            data['Education'],
            data['Hackathons_and_Achievements'],
            json.dumps(data['Activities_and_Interests'])  
        )

        cursor.execute(user_query, user_values)
        user_id = cursor.lastrowid  

        for company in data['Companies']:
            company_query = """
            INSERT INTO Companies (user_id, Company_Name, Role, Start_Date, End_Date, Time_Spent) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            company_values = (
                user_id,
                company['Company_Name'],
                company['Role'],
                company['Start_Date'],
                company['End_Date'],
                company['Time_Spent']
            )

            cursor.execute(company_query, company_values)
            company_id = cursor.lastrowid 
            for project in company['Projects']:
                project_query = """
                INSERT INTO Projects (company_id, Project_Name, Project_Overview) 
                VALUES (%s, %s, %s)
                """
                project_values = (
                    company_id,
                    project['Project_Name'],
                    project['Project_Overview']
                )
                cursor.execute(project_query, project_values)

        connection.commit()  

    except mysql.connector.Error as err:
        log_error(f"Error while inserting data: {err}")
    
    finally:
        if cursor:
            cursor.close() 
        if connection:
            connection.close() 
