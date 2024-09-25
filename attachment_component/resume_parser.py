from dotenv import load_dotenv
import json
import os
import openai
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
from datetime import datetime

def calculate_duration(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%B %Y")  
        
        if end_date.lower() == "present":
            end = datetime.now() 
        else:
            end = datetime.strptime(end_date, "%B %Y")  
        duration_in_months = (end.year - start.year) * 12 + (end.month - start.month)

        years = duration_in_months // 12
        months = duration_in_months % 12
        
        if years > 0:
            return f"{years} year{'s' if years > 1 else ''} and {months} month{'s' if months > 1 else ''}"
        else:
            return f"{months} month{'s' if months > 1 else ''}"
    
    except Exception as e:
        return "None"  

def extract_resume_entities(input_text):
    prompt_template = f"""
    Extract the following key entities from the resume text provided. Return the output in JSON format. For each company project, write only the name and a short overview of the project, not complete paragraphs. If the information is not present, return "None". Calculate the "Time Spent" for each company based on the start and end dates. If the "Time Spent" cannot be calculated, return "None".
    
    If there is a date range mentioned in the format like 'March 2022 to present', or similar formats, calculate the "Time Spent" using proper mathematical calculations based on the start and end dates. Do not just copy the text, but calculate the time accurately.

    Example format for company experience:
    {{
      "Company_Name": "Hobasa India Pvt. Ltd",
      "Role": "Data Scientist",
      "Start_Date": "March 2022",
      "End_Date": "present",
      "Time_Spent": "1 year and 6 months",
      "Projects": [
        {{
          "Project_Name": "Rule Extraction and Execution",
          "Project_Overview": "Developed an NLP-based rule extraction."
        }}
      ]
    }}

    Resume text:
    \"\"\"{input_text}\"\"\"

    Output the response in the following JSON format:

    {{
      "Name": "<Name>",
      "Email": "<Email>",
      "Phone": "<Phone>",
      "Total_Experience": "<Total Experience (in years and months)>",
      "LinkedIn_Profile": "<LinkedIn Profile>",
      "Companies": [
        {{
          "Company_Name": "<Company Name>",
          "Role": "<Role>",
          "Start_Date": "<Start Date (e.g., 'March 2022')>",
          "End_Date": "<End Date (e.g., 'present' or 'December 2023')>",
          "Time_Spent": "<Time Spent (in years and months)>",
          "Projects": [
            {{
              "Project_Name": "<Project Name>",
              "Project_Overview": "<Short Overview of the Project>"
            }}
          ]
        }}
      ],
      "Key_Skills": [
        "<Skill 1>",
        "<Skill 2>"
      ],
      "Education": "<Education>",
      "Hackathons_and_Achievements": "<Hackathons and Achievements>",
      "Activities_and_Interests": [
        "<Activity 1>",
        "<Interest 1>"
      ]
    }}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_template}
            ],
            temperature=0
        )
        extracted_json = response['choices'][0]['message']['content']

        extracted_data = eval(extracted_json)  
        for company in extracted_data['Companies']:
            start_date = company.get("Start_Date", "None")
            end_date = company.get("End_Date", "None")
            company['Time_Spent'] = calculate_duration(start_date, end_date)

        return extracted_data

    except Exception as e:
        return f"Error: {str(e)}"

