import os
import logging
from flask import Flask, jsonify, request
from outlook_component.get_mail import Mail_Reader
from database_component.email_to_db import insert_email_data
from classification_model.model import classify_mail
from database_component.classification_to_db import insert_body_processed_data
from outlook_component.move_mail import inbox_to_folder
from attachment_component.files import extract_text_from_file
from attachment_component.resume_parser import extract_resume_entities
from database_component.attachment_db import insert_data_attachment

app = Flask(__name__)

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

error_responses = {
    400: {'error': 'Bad Request'},
    401: {'error': 'Unauthorized'},
    404: {'error': 'Not Found'},
    500: {'error': 'Internal Server Error'}
}

def log_and_return_error(error_message, status_code):
    logging.error(error_message)
    print(f"Error: {error_message}")  # Print error message
    return jsonify(error_responses.get(status_code, {})), status_code

@app.route('/v1/mail_api', methods=['GET', 'POST'])
def outlookAPI():
    try:
        if request.method == 'GET':
            username = request.args.get("username")
            password = request.args.get("password")
            types = request.args.get("type")
        elif request.method == 'POST':
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            types = data.get("type")
        else:
            return log_and_return_error("Unsupported HTTP method", 400)

        if not (username and password and types):
            return log_and_return_error("Missing required parameters", 400)
        
        logging.info(f"Request received for user: {username}, type: {types}")
        print(f"Request received for user: {username}, type: {types}")  # Print step

        result = Mail_Reader(username, password, types)
        if result is None:
            return log_and_return_error("No emails found in inbox", 404)

        logging.info("Getting new emails...")
        print("Getting new emails...")  # Print step

        sender_email = result.get('From', None)
        recipient_email = username
        subject = result.get('Subject', None)
        message_text = result.get('Body', None)
        uid = result.get('UID', None)
        attachment_path = result.get('Attachment', None)

        logging.info(f"Email details: From={sender_email}, To={recipient_email}, Subject={subject}")
        print(f"Email details: From={sender_email}, To={recipient_email}, Subject={subject}")  # Print step

        # Insert email data into the database
        try:
            insert_email_data(sender_email, recipient_email, subject, attachment_path, message_text)
            print("Email data inserted into database.")  # Print output
        except Exception as e:
            logging.error(f"Error inserting email data: {str(e)}")
            print(f"Error inserting email data: {str(e)}")  # Print error but continue

        # Model Prediction
        predicted_labels = None
        try:
            logging.info("Model Prediction...")
            print("Model Prediction...")  # Print step
            predicted_labels = classify_mail(message_text)
            print(f"Predicted Labels: {predicted_labels}")  # Print output
            insert_body_processed_data(sender_email, recipient_email, subject, attachment_path, message_text, predicted_labels)
            print("Predicted labels inserted into database.")  # Print output
        except Exception as e:
            logging.error(f"Model Classification Error: {str(e)}")
            print(f"Model Classification Error: {str(e)}")  # Print error but continue

        # Move email to corresponding folder based on prediction
        try:
            logging.info("Moving email to corresponding folder based on prediction...")
            print("Moving email to corresponding folder based on prediction...")  # Print step
            inbox_to_folder(uid, predicted_labels, username, password)
            print("Email moved to folder based on prediction.")  # Print output
        except Exception as e:
            logging.error(f"Data Migration Error on Outlook: {str(e)}")
            print(f"Data Migration Error on Outlook: {str(e)}")  # Print error but continue

        # Process attachment if present
        if attachment_path:
            try:
                logging.info("Extracting text from file...")
                print("Extracting text from file...")  # Print step
                extracted_text = extract_text_from_file(attachment_path)
                print(f"Extracted Text: {extracted_text}")  # Print output
                if not extracted_text:
                    raise ValueError("No text extracted from the document")

                logging.info("Extracting resume entities...")
                print("Extracting resume entities...")  # Print step
                extracted_entities = extract_resume_entities(extracted_text)
                print(f"Extracted Entities: {extracted_entities}")  # Print output

                logging.info("Inserting extracted data into database...")
                print("Inserting extracted data into database...")  # Print step
                insert_data_attachment(extracted_entities)
                print("Extracted data inserted into database.")  # Print output

            except Exception as e:
                logging.error(f"Attachment Processing Error: {str(e)}")
                print(f"Attachment Processing Error: {str(e)}")  # Print error but continue

        print("Done processing the email.")  # Print completion
        return jsonify({'Response': "Ok"}), 200

    except ValueError as ve:
        error_message = str(ve)
        return log_and_return_error(f"Bad Request: {error_message}", 400)

    except Exception as e:
        error_message = str(e)
        return log_and_return_error(f"Internal Server Error: {error_message}", 500)

if __name__ == "__main__":
    app.run(host=os.getenv('BASE_HOST', '127.0.0.1'), port=int(os.getenv('BASE_PORT', 3008)), debug=True)
