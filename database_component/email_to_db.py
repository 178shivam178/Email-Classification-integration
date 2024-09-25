import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def insert_email_data(sender_email, recipient_email, subject, attachment_path, message_text):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST'),
            user=os.getenv('DBUSER'),
            password=os.getenv('DBPASS'),
            database=os.getenv('DATABASE')
        )

        cursor = connection.cursor()

        insert_query = """
        INSERT INTO Emails (SenderEmail, RecipientEmail, Subject, AttachmentPath, MessageText)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (str(sender_email), str(recipient_email), str(subject), str(attachment_path), str(message_text)))
        connection.commit()

    except mysql.connector.Error as error:
        raise f"Error inserting data: {error}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
