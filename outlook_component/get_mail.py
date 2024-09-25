import imaplib
import email
import os
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()
IMAP_SERVER = os.getenv("OUTIMAP")

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def obtain_header(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else 'utf-8')
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding if encoding else 'utf-8')
    return subject, From

def download_attachment(part, subject):
    filename = part.get_filename()
    if filename:
        folder_name = clean(subject)
        folder_name = os.path.join("attachment", folder_name)
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        filepath = os.path.join(folder_name, filename)
        with open(filepath, "wb") as file:
            file.write(part.get_payload(decode=True))
    return filepath

def Mail_Reader(username, password, types):
    try:
        m = imaplib.IMAP4_SSL(IMAP_SERVER)
    except Exception as imap_conn_error:
        raise ConnectionError(f"Failed to connect to IMAP server: {imap_conn_error}")

    try:
        m.login(username, password)
    except imaplib.IMAP4.error as login_error:
        raise PermissionError(f"Failed to login to the server: {login_error}")

    try:
        m.select(mailbox='Inbox', readonly=False)
    except Exception as select_error:
        raise Exception(f"Failed to select the mailbox: {select_error}")

    try:
        result, data = m.search(None, types)
        if result != 'OK':
            raise ValueError("Failed to search the mailbox.")

        for num in data[0].split():
            result, data = m.fetch(num, '(RFC822)')
            if result != 'OK':
                raise Exception("Failed to fetch the email.")

            resp, uid = m.fetch(num, "(UID)")
            email_message = email.message_from_bytes(data[0][-1])
            subject, From = obtain_header(email_message)
            mail_data = {"Subject": subject, "From": From, "UID": uid}

            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        try:
                            body = part.get_payload(decode=True).decode()
                            mail_data["Body"] = body
                        except Exception as body_error:
                            raise ValueError(f"Failed to decode email body: {body_error}")
                    elif "attachment" in content_disposition:
                        filepath = download_attachment(part, subject)
                        if filepath:
                            mail_data["Attachment"] = filepath
            else:
                content_type = email_message.get_content_type()
                body = email_message.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    mail_data["Body"] = body

            return mail_data

    except Exception as e:
        raise Exception(f"An error occurred during email processing: {e}")
    finally:
        try:
            m.close()
            m.logout()
        except Exception as logout_error:
            raise Exception(f"Failed to logout from the server: {logout_error}")
