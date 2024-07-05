import subprocess
import schedule
import time
import logging
import os
import json
# from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,format="%(asctime)s::%(levelname)s::%(message)s")
delimeter = "===================================="

class Backup:
    def __init__(self) -> None:
        self.current_dir = os.path.dirname(__file__)
        with open(os.path.join(self.current_dir,'backup_settings.json')) as file:
            content = file.read()
            self.settings = json.loads(content)
        
        self.token = self.settings["GITHUB_TOKEN"]
        self.username = self.settings["GITHUB_USERNAME"]
        self.name_repo  = self.settings["GITHUB_NAME_REPO"]
        self.databases = {}
        settings_values = [self.token,self.username,self.name_repo]
        if "databases" in self.settings:
            for database in self.settings["databases"]:
                self.databases.update({database:{}})
                for key in self.settings["databases"][database]:
                    value = self.settings["databases"][database][key]
                    settings_values.append(value)
                    self.databases[database].update({key:value})
                if len(self.databases[database]) == 0:
                    raise RuntimeError(f"Fill in the data to connect to the database '{database}'")
        for settings_value in settings_values:
            if settings_value is None or settings_value.strip()  ==  "": 
                raise RuntimeError("One or more setting values ​​not found")
        self.repo_dir = os.path.join(self.current_dir,"backup",self.name_repo)
        self.backup_dir = os.path.join(self.current_dir,"backup")

    def run(self) -> None:
        if not os.path.exists(self.repo_dir):
            os.mkdir(self.backup_dir)
            clone_command = f"cd {self.backup_dir} && git clone  https://{self.token}@github.com/{self.username}/{self.name_repo}"
            subprocess.run(clone_command, shell=True)
        checkout_command = "git checkout -b master"
        subprocess.run(checkout_command, shell=True)
        push_command = f"cd {self.repo_dir} && git add . && git commit -m \"Backup\" && git push -f origin master"
        subprocess.run(push_command, shell=True)

        for database in self.databases:
            logging.info(f"Starting backup {database}...")
            values = self.databases[database].copy()
            backup_path = os.path.join(self.repo_dir,values["DB_NAME"] + ".sql")
            command = f'pg_dump --dbname=postgresql://{values["DB_USER"]}:{values["DB_PASSWORD"]}@{values["DB_HOST"]}:{values["DB_PORT"]}/{values["DB_NAME"]} > "{backup_path}"'
            output = subprocess.run(command, shell=True)
            logging.info(f"Backup successfully finished. {output}")
        print(delimeter)

if __name__ == "__main__":
    backup = Backup()
    # Schedule the backup to run every 1 hour
    schedule.every(1).minute.do(backup.run)
    while True:
        schedule.run_pending()
        time.sleep(1)