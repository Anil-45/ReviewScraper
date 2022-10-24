"""Generate config file for Database Credentials."""
import configparser

CONFIG_FILE = "config.ini"
DATABASE = "Database"
HOST = "Host"
USERNAME = "Username"
PASSWORD = "Password"

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD DATABASE SECTION
config_file.add_section(DATABASE)

# ADD DATABASE CREDENTIALS
config_file.set(DATABASE, HOST, "127.0.0.1")
config_file.set(DATABASE, USERNAME, "root")
config_file.set(DATABASE, PASSWORD, "root")

# SAVE CONFIG FILE
with open(CONFIG_FILE, "w", encoding="utf-8") as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()
