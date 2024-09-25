from flask import Flask, Response, render_template
import requests
import os
import json
import time
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

def call_email_classification_api(username, password):
    try:
        parameters = {
            "username": username,
            "password": password,
            "type": "UNSEEN"
        }
        response = requests.get("http://127.0.0.1:3008/v1/mail_api", params=parameters)
        if response.status_code == 404:
            return {"message": "No new emails found."}
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "API request error: " + str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response')
def get_response():
    try:
        outlook_username = os.getenv('OUTLOOK_USERNAME')
        outlook_password = os.getenv('OUTLOOK_PASSWORD')

        def generate():
            for _ in range(86600):
                response_data = call_email_classification_api(outlook_username, outlook_password)
                yield json.dumps(response_data, indent=2) + '\n'
                time.sleep(5) 

        return Response(generate(), mimetype='application/json')
    except Exception as e:
        return {"error": "An error occurred: " + str(e)}

    
if __name__ == "__main__":
    app.run(host=os.getenv('HOST', '127.0.0.1'), port=int(os.getenv('PORT', 5000)))
