# mysql_switcher
Console application for updating and switching mysql databases.

Requirements: 
 - Python3.4
 - pymysql lib (Installation: "pip install pymysql")
 

Configurations:
 - add python3.4 to PATH
 - add "C:\xampp\mysql\bin" to PATH
 - in config.py add all mysql databases that you will use with all DB settings
 
Usage:
 - in terminal(cmd) run: python(3) change_db.py XXXXX switch update, 
where XXXXX is key in config.py dictionary. 'switch' and 'update' are 
not required parameters. 'switch' parameter will delete your main LOCAL DB 
and will create it again using structure and data from choosen DB. 'update' will
delete and make again backup DB locally using structure and data from choosen DB.

Examples:
 - python change_db.py LOCAL switch
 - python change_db.py LOCAL update
 - python change_db.py LOCAL switch update



