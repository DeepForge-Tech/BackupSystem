## BackupSystem - system for making backup in sql files for postgresql database.
### For backup:
###### backup_settings.json
```json
{
    "GITHUB_TOKEN":"",
    "GITHUB_USERNAME":"",
    "GITHUB_NAME_REPO":"",
    "databases": {
        "name_db": {
            "DB_NAME":"name_db",
            "DB_HOST":"host_db",
            "DB_USER":"user_db",
            "DB_PASSWORD":"password_user",
            "DB_PORT":"port_db"
        }
    }
}
```

### For restore:
###### restore_settings.json
```json
{
    "databases": {
        "name_db": {
            "DB_NAME":"name_db",
            "DB_HOST":"host_db",
            "DB_USER":"user_db",
            "DB_PASSWORD":"password_user",
            "DB_PORT":"port_db",
            "BACKUP_PATH":"path/to/backup.sql"
        }
    }
}
```