import os
import openai
from dotenv import load_dotenv
from classification_model.prompt import create_classification_prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise EnvironmentError("API key is missing. Please check your .env file.")

openai.api_key = api_key

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
                {"role": "system", "content": "You are an expert at HR domain."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0
        )

        category = response['choices'][0]['message']['content'].strip()

        if category not in labels and category != "Other":
            raise ValueError(f"Invalid category returned: {category}")
        
        return category

    except openai.error.OpenAIError as e:
        raise Exception(f"OpenAI API error occurred: {str(e)}")

    except Exception as e:
        raise Exception(f"An error occurred during classification: {str(e)}")
