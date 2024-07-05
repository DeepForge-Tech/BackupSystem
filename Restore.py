import json
import os
import logging
import subprocess
import argparse

logging.basicConfig(level=logging.INFO,format="%(asctime)s::%(levelname)s::%(message)s")

class Restore:
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        with open(os.path.join(self.current_dir,'restore_settings.json')) as file:
            content = file.read()
            self.settings = json.loads(content)
        self.databases = {}
        settings_values = []
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
    
    def start(self) -> None:
        for database in self.databases:
            logging.info(f"Starting restore {database}...")
            values = self.databases[database].copy()
            backup_path = values["BACKUP_PATH"]
            command = f'psql --dbname=postgresql://{values["DB_USER"]}:{values["DB_PASSWORD"]}@{values["DB_HOST"]}:{values["DB_PORT"]}/{values["DB_NAME"]} -f "{backup_path}"'
            subprocess.call(command, shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
            logging.info(f"Restore successfully finished.")

if __name__ == "__main__":
    restore  =  Restore()
    restore.start()
