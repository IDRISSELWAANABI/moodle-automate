
import re
import os


td = re.compile("td|travaux dirigés|exercices|série" , re.IGNORECASE)
tp = re.compile("tp|travaux pratique" , re.IGNORECASE)       
moodle = "http://m.inpt.ac.ma/login/index.php"
profile = "http://m.inpt.ac.ma/user/profile.php?id=&showallcourses=1"
homedir = os.path.expanduser("~")
login_path = os.path.join(homedir, ".login.txt")


         
