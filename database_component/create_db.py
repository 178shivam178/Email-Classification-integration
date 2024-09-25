import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST'),
            user=os.getenv('DBUSER'),
            password=os.getenv('DBPASS'),
            database=os.getenv('DATABASE')
        )

        with connection.cursor() as cursor:
            create_table_query_email = """
            CREATE TABLE IF NOT EXISTS Emails (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                SenderEmail VARCHAR(255),
                RecipientEmail VARCHAR(255),
                Subject VARCHAR(255),
                AttachmentPath VARCHAR(255),
                MessageText TEXT
            );
            """

            create_table_query_classification = """
            CREATE TABLE IF NOT EXISTS EmailClassificationResult (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                SenderEmail VARCHAR(255),
                RecipientEmail VARCHAR(255),
                Subject VARCHAR(255),
                AttachmentPath VARCHAR(255),
                MessageText TEXT,
                Label VARCHAR(255)
            );
            """
            
            create_table_query_users = """
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                Email VARCHAR(255),
                Phone VARCHAR(50),
                Total_Experience VARCHAR(50),
                LinkedIn_Profile VARCHAR(255),
                Education TEXT,
                Hackathons_and_Achievements TEXT,
                Activities_and_Interests TEXT
            );
            """

            create_table_query_companies = """
            CREATE TABLE IF NOT EXISTS Companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                Company_Name VARCHAR(255),
                Role VARCHAR(100),
                Start_Date VARCHAR(50),
                End_Date VARCHAR(50),
                Time_Spent VARCHAR(50),
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            );
            """

            create_table_query_projects = """
            CREATE TABLE IF NOT EXISTS Projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_id INT,
                Project_Name VARCHAR(255),
                Project_Overview TEXT,
                FOREIGN KEY (company_id) REFERENCES Companies(id) ON DELETE CASCADE
            );
            """

            # Execute all the table creation queries
            cursor.execute(create_table_query_email)
            cursor.execute(create_table_query_classification)
            cursor.execute(create_table_query_users)
            cursor.execute(create_table_query_companies)
            cursor.execute(create_table_query_projects)

            connection.commit()

        print("Tables created successfully!")

    except mysql.connector.Error as error:
        print(f"Error occurred: {error}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    create_tables()
