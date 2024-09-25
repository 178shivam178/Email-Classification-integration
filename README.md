# HR Email Classification and Extraction System

## Overview
The HR Email Classification and Extraction System is designed to streamline the management of incoming emails within the Human Resources department. By integrating a dedicated email system, this project aims to automatically classify and process various HR-related emails, enhancing efficiency and organization.

## Objectives
1. **Email Integration:** The system monitors a dedicated email account for new incoming messages.
2. **Email Classification:** Incoming emails are classified into predefined categories:
   - Job Application
   - Interview Request
   - Onboarding
   - Employee Inquiry
   - Performance Review
   - Resignation
   - Training Request
   - Benefits Enrollment
   - Policy Update
   - Payroll Issue

3. **Data Storage:** Essential email information is stored in a MySQL database to ensure secure and organized data management.

4. **Folder Creation in Outlook:** After classification, the system automatically creates folders in Outlook corresponding to the classified labels and transfers the respective emails into these folders for easy access.

5. **Document Extraction:** For emails classified as "Job Application" containing resumes or CVs, the system extracts key entities from various document formats (PDF, images, CSV, DOCX, Excel, etc.). The key entities to be extracted include:
   - Name
   - Email
   - Phone
   - Total Experience (in years and months)
   - LinkedIn Profile
   - Employment History (including Company Name, Role, Start and End Dates, Time Spent, and Project Details)
   - Key Skills
   - Education
   - Hackathons and Achievements
   - Activities and Interests

6. **Data Organization:** Extracted key entities are stored in the MySQL database in a structured format for efficient retrieval and analysis. The structure includes:

   ```json
   {
     "Name": "<Name>",
     "Email": "<Email>",
     "Phone": "<Phone>",
     "Total_Experience": "<Total Experience (in years and months)>",
     "LinkedIn_Profile": "<LinkedIn Profile>",
     "Companies": [
       {
         "Company_Name": "<Company Name>",
         "Role": "<Role>",
         "Start_Date": "<Start Date>",
         "End_Date": "<End Date>",
         "Time_Spent": "<Time Spent (in years and months)>",
         "Projects": [
           {
             "Project_Name": "<Project Name>",
             "Project_Overview": "<Short Overview of the Project>"
           }
         ]
       }
     ],
     "Key_Skills": ["<Skill 1>", "<Skill 2>"],
     "Education": "<Education>",
     "Hackathons_and_Achievements": "<Hackathons and Achievements>",
     "Activities_and_Interests": ["<Activity 1>", "<Interest 1>"]
   }


## Project Setup

This README provides instructions to set up the project environment, install dependencies, configure the environment variables, and run the application.

## Prerequisites

## Ensure you have Python 3.8.13 installed on your system. You can check your Python version with the following command:

python --version
Step 1: Create a Virtual Environment
Create a virtual environment for the project using Python 3.8.13:

```bash 
python3.8 -m venv venv
```
## Activate the virtual environment:

On macOS and Linux:
 ```bash
source venv/bin/activate
```

## Step 2: Install Requirements
With the virtual environment activated, install the required packages listed in requirements.txt:

```bash
pip install -r requirements.txt
```

## Step 3: Set Up Environment Variables
Create a .env file in the project root directory and add the following variables:

```bash
OUTIMAP=your_outlook_imap_server
OUTLOOK_USERNAME=your_outlook_email
OUTLOOK_PASSWORD=your_outlook_password
DBHOST=your_database_host
DBUSER=your_database_username
DBPASS=your_database_password
DATABASE=email
HOST=127.0.0.1
PORT=5000
BASE_HOST=127.0.0.1
BASE_PORT=3008
OPENAI_API_KEY=your_openai_api_key
```
Replace the placeholder values with your actual credentials.

## Step 4: Run the Application
You can now run the server using the following commands:

To run the main API server:
```bash
python api.py
```
To run the 24x7 tracking server:

```bash
python 24x7_api.py
```

The application will now be running and will continuously track emails.

Notes
Ensure that you have access to the Outlook account and the database before starting the application.
Make sure to keep your credentials secure and not share them publicly.