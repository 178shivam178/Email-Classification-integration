import imaplib
import re
import os

pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')

if not os.path.exists('logs'):
    os.makedirs('logs')

def log_error(message):
    with open('logs/move_mail.txt', 'a') as log_file:
        log_file.write(message + "\n")

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def connect(email, password):
    try:
        imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        imap.login(email, password)
        return imap
    except Exception as e:
        log_error(f"Error connecting to IMAP: {e}")
        return None

def disconnect(imap):
    try:
        imap.logout()
    except Exception as e:
        log_error(f"Error disconnecting from IMAP: {e}")

def parse_uid(data):
    try:
        match = pattern_uid.match(data)
        return match.group('uid') if match else None
    except Exception as e:
        log_error(f"Error parsing UID: {e}")
        return None

def Create_Folder_For_Body(label, username, password):
    try:
        IMAP = "imap-mail.outlook.com"
        imap = imaplib.IMAP4_SSL(IMAP)
        imap.login(username, password)
        folder = "Classification_On_Body/{}".format(clean(label))
        imap.create(folder)
        disconnect(imap)
    except Exception as e:
        log_error(f"Error creating folder: {e}")

def FolderChecker_For_Body(label, username, password):
    try:
        IMAP = "imap-mail.outlook.com"
        mail = imaplib.IMAP4_SSL(IMAP)
        mail.login(username, password)
        for i in mail.list()[1]:
            l = i.decode().split(' "/" ')
            match = "Classification_On_Body"+"/"+clean(label)
            if str(l[1]) == str(match):
                disconnect(mail)
                return True
        disconnect(mail)
        return False
    except Exception as e:
        log_error(f"Error checking folder: {e}")
        return False

def Move_Items_For_Body(uid, label, username, password):
    try:
        imap = connect(username, password)
        if imap:
            imap.select(mailbox='Inbox', readonly=False)
            msg_uid = parse_uid(uid[0].decode('utf-8'))
            if msg_uid:
                destination_folder = "Classification_On_Body" + "/" + clean(label)
                result = imap.uid('COPY', msg_uid, destination_folder)
                if result[0] == 'OK':
                    mov, data = imap.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
                    imap.expunge()
                    print("Email moved successfully!")
            disconnect(imap)
    except Exception as e:
        log_error(f"Error moving email: {e}")

def inbox_to_folder(uid, label, username, password):
    try:
        if FolderChecker_For_Body(label, username, password):
            Move_Items_For_Body(uid, label, username, password)
        else:
            Create_Folder_For_Body(label, username, password)
            Move_Items_For_Body(uid, label, username, password)
    except Exception as e:
        log_error(f"Error in inbox_to_folder: {e}")
