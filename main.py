import yaml
from yaml import load
yaml.warnings({'YAMLLoadWarning': False})
import subprocess

##Loads information from config file
with open("config.yaml") as file:
    data = load(file)
    toggle = data["toggle"]

subprocess.Popen('python sysbot.py')
subprocess.Popen('python dashboard.py')
if toggle == 1:
    subprocess.Popen('python pokemon/twitch.py')