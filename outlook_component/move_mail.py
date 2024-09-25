import os
import imaplib
import re
from dotenv import load_dotenv

load_dotenv()
IMAP_URL = os.getenv("OUTIMAP")

if IMAP_URL is None:
    raise EnvironmentError("IMAP URL is missing. Please check your .env file.")

pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')

class EmailOperationError(Exception):
    pass

def clean(text):
    try:
        return "".join(c if c.isalnum() else "_" for c in text)
    except Exception as e:
        raise EmailOperationError(f"Error in cleaning text: {e}")

def connect(email, password):
    try:
        imap = imaplib.IMAP4_SSL(IMAP_URL)
        imap.login(email, password)
        return imap
    except imaplib.IMAP4.error as e:
        raise EmailOperationError(f"Login failed: {e}")
    except Exception as e:
        raise EmailOperationError(f"Error connecting to IMAP server: {e}")

def disconnect(imap):
    try:
        imap.logout()
    except Exception as e:
        raise EmailOperationError(f"Error disconnecting from IMAP server: {e}")

def parse_uid(data):
    try:
        match = pattern_uid.match(data)
        if not match:
            raise EmailOperationError(f"UID parsing failed: No match found in {data}")
        return match.group('uid')
    except Exception as e:
        raise EmailOperationError(f"Error parsing UID: {e}")

def Create_Folder_For_Body(label, username, password):
    imap = None
    try:
        imap = connect(username, password)
        folder = f"Classification_On_Body/{clean(label)}"
        result = imap.create(folder)
        if result[0] != 'OK':
            raise EmailOperationError(f"Failed to create folder: {folder}")
    except Exception as e:
        raise EmailOperationError(f"Error creating folder: {e}")
    finally:
        if imap:
            disconnect(imap)

def FolderChecker_For_Body(label, username, password):
    imap = None
    try:
        imap = connect(username, password)
        folder_to_check = f"Classification_On_Body/{clean(label)}"
        for i in imap.list()[1]:
            l = i.decode().split(' "/" ')
            if str(l[1]) == folder_to_check:
                return True
        return False
    except Exception as e:
        raise EmailOperationError(f"Error checking folder: {e}")
    finally:
        if imap:
            disconnect(imap)

def Move_Items_For_Body(uid, label, username, password):
    imap = None
    try:
        imap = connect(username, password)
        imap.select(mailbox='Inbox', readonly=False)
        msg_uid = parse_uid(uid[0].decode('utf-8'))
        destination_folder = f"Classification_On_Body/{clean(label)}"
        result = imap.uid('COPY', msg_uid, destination_folder)
        if result[0] != 'OK':
            raise EmailOperationError(f"Failed to move item UID: {msg_uid} to {destination_folder}")
        imap.uid('STORE', msg_uid, '+FLAGS')
        print("DONE")
    except Exception as e:
        raise EmailOperationError(f"Error moving items: {e}")
    finally:
        if imap:
            disconnect(imap)

def inbox_to_folder(uid, label, username, password):
    try:
        if FolderChecker_For_Body(label, username, password):
            Move_Items_For_Body(uid, label, username, password)
        else:
            Create_Folder_For_Body(label, username, password)
            Move_Items_For_Body(uid, label, username, password)
    except Exception as e:
        print(f"Error during migration: {str(e)}")  # Log the error for debugging
        raise ValueError("Not able to migrate mail!!")
