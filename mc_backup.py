# https://github.com/sayersauce
# Usage, execute using command `python3 mc_backup.py {extra_recipient} {extra_recipient}...`

import smtplib
import ssl
import json
import os
import sys
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from zipfile import ZipFile


FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"


def load_config():
    # Loads configuration from config.json.
    with open(FILE_PATH + "config.json") as config_file:
        return json.load(config_file)


def timestamp(zip = False):
    # Returns a timestamp, format changes due to filename restrictions.
    date = datetime.now()
    if zip:
        return f"{date.day}-{date.month}-{date.year} {date.hour}-{date.minute}-{date.second}"
    return f"{date.day}/{date.month}/{date.year} - {date.hour}:{date.minute}:{date.second}"


def create_backup_zip(server_path, backup_folder_path, ignored_dirs, ignored_files):
    # Zips all server files. Saves the zip to `Backups` folder. Returns the zip's path.
    file_paths = []

    # Get all file paths from server.
    for root, dirs, files in os.walk(server_path):
        skip = False

        for d in ignored_dirs:
            if d in root:
                skip = True
                break

        if skip:
            continue

        for f in files:
            if f not in ignored_files:
                file_paths.append(os.path.join(root, f))

    path = f"{backup_folder_path}{timestamp(True)}.zip"

    # Zipping.
    with ZipFile(path, "w") as zip: 
        for file in file_paths: 
            zip.write(file)

    return path


def send_email(sender, password, recipient, zip_path, subject_title, smtp_server, port):
    # Sends zipfile to recipient email.
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject_title + " " + timestamp()

    # Attaching zip.
    with open(zip_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment; filename= backup.zip"
    )
    message.attach(part)
    
    # Sending email.
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())


if __name__ == "__main__":
    # Check args.
    args = sys.argv
    recipients = []

    if len(args) > 1:
        for arg in args[1:]:
            recipients.append(arg)

    # Config.
    config = load_config()

    # Perform backup creation.
    zip_path = create_backup_zip(FILE_PATH + config["server_path"], FILE_PATH + config["backup_folder_path"], config["ignored_directories"], config["ignored_files"])

    # Send email.
    recipients += config["receiver_emails"]

    for recipient in recipients:
        print(f"Sending to {recipient}")
        send_email(
            config["sender_email"],
            config["sender_password"],
            recipient,
            zip_path,
            config["email_title"],
            config["smtp_server"],
            config["smtp_port"]
        )
