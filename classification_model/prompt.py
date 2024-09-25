def create_classification_prompt(mail_content, labels):
    prompt = f"""
    You are a HR classification model. Your task is to categorize the following content into one of these categories by understanding content properly:

    {', '.join(labels)}.

    If the content of the mail does not clearly fit any of the categories, please classify it as "Other".

    Here is the HR mail content:
    \"\"\"{mail_content}\"\"\"

    Please respond with only one category name from the list above or "Other".
    """
    
    return prompt
