import os
import openai
from dotenv import load_dotenv
from classification_model.prompt import create_classification_prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise EnvironmentError("API key is missing. Please check your .env file.")

openai.api_key = api_key

if not os.path.exists('logs'):
    os.makedirs('logs')

def log_error(message):
    with open('logs/model.txt', 'a') as log_file:
        log_file.write(message + "\n")

labels = [
    "Job Application",
    "Interview Request",
    "Onboarding",
    "Employee Inquiry",
    "Performance Review",
    "Resignation",
    "Training Request",
    "Benefits Enrollment",
    "Policy Update",
    "Payroll Issue"
]

def classify_mail(mail_content):
    try:
        prompt = create_classification_prompt(mail_content, labels)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in the HR domain."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0
        )
        category = response['choices'][0]['message']['content'].strip()

        if category not in labels and category != "Other":
            log_error(f"Invalid category returned: {category}")
            return "Other"
        
        return category

    except openai.error.OpenAIError as e:
        log_error(f"OpenAI API error occurred: {str(e)}")
        return "Other"

    except Exception as e:
        log_error(f"An error occurred during classification: {str(e)}")
        return "Other"
