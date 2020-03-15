# MC-Backup
A spigot plugin which periodically, and on command, emails a back-up of a Minecraft server.

Created with both Java and Python.

## Setup
#### Details on SMTP
An email account for sending and receiving the backups will need to be made. Details regarding using gmail for this can be found here: https://www.androidauthority.com/gmail-smtp-settings-801100/
#### Python Script
- Place `mc_backup.py` into a directory of choice along with a `config.json` file.
- Fill in config.json with the appropriate configurations. <br> ```javascript
{
    "server_path" : "",
    "backup_folder_path" : "",
    "ignored_directories" : [],
    "ignored_files" : [],
    "sender_email" : "",
    "sender_password" : "",
    "receiver_emails" : [],
    "email_title" : "Minecraft SMP",
    "smtp_server" : "",
    "smtp_port" : 0
}```
- Many email providers put limits onto attachment capacity, to avoid maximising the space available, directories such as `plugins` and files such as the `server.jar` can be ignored in backups.
#### Spigot Plugin
- Place `backup.jar` into the server's plugins folder.
- Go into the `config.yml` file and fill in the configurations.<br>`frequency: 72000
path: path/script.py
python: python3
debug: false`
- `frequency` is the interval in ticks in which backups are made.
- `path` is the path to the python script.
- `python` is the python command, dependent on os.
- `debug` shows errors and output of the python script.

## Usage
Backups are sent to the `receiver_emails` in the `config.json` file, and stored in the `backup_folder_path` folder. In game, operators can issue the command `/backup` to backup the server. If they wish to send the backup to another email, or multiple, they can issue the command with arguments `/backup a@gmail.com b@gmail.com`.
