# https://github.com/sayersauce
# Usage `python3 mc_backup.py {absolute_server_path} {absolute_backup_folder_path} {server_address}`

import os
import sys
from mcstatus import MinecraftServer
from datetime import datetime
from zipfile import ZipFile


def timestamp(zip = False):
    date = datetime.now()
    if zip:
        return f"{date.day}-{date.month}-{date.year} {date.hour}-{date.minute}-{date.second}"
    return f"{date.day}/{date.month}/{date.year} - {date.hour}:{date.minute}:{date.second}"


def create_backup_zip(server_path, backup_folder_path):
    file_paths = []

    # Get all file paths from server
    for root, dirs, files in os.walk(server_path):
        for f in files:
            file_paths.append(os.path.join(root, f))

    zip_path = f"{backup_folder_path}{timestamp(True)}.zip"

    # Zipping
    with ZipFile(zip_path, "w") as zip: 
        for file in file_paths: 
            zip.write(file)

    return zip_path


def player_count(address):
    server = MinecraftServer.lookup(address)
    try:
        status = server.status()
        return status.players.online
    except:
        print("Error pinging Minecraft Server.")
        return 0


if __name__ == "__main__":
    # Check args
    args = sys.argv

    if len(args) > 3:
        server_path = args[1]
        backup_folder_path = args[2]
        server_address = args[3]

        if not server_path.endswith("/"):
            server_path += "/"
        if not backup_folder_path.endswith("/"):
            backup_folder_path += "/"

        # Check that the server has players online
        if player_count(server_address):
            # Perform backup creation
            zip_path = create_backup_zip(server_path, backup_folder_path)
            print("Zip created at " + zip_path + ".")
        else:
            print("No zip created.")
    else:
        print("Usage: mc_backup.py {server_path} {backup_folder_path} {server_address}")
