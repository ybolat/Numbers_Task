In bracnh master you can see the code

Download libraries, if you don't have them.

Create database, and in yerassyl/yerassyl/setting.py change database name, user, password.

In order to start project, first open console in the directory where manage.py file, and write "python manage.py makemigrations", then "python manage.py migrate", 
and then write "python manage.py runserver"

Link to the Google Sheets : https://docs.google.com/spreadsheets/d/16r9rIrvH3GuZ-GFH9XlVd7mBuy8vwOS0njFraYn1dhE/edit#gid=0

Project will run on http://localhost:8000

In the opened page you will see table with data from Google Sheets, with column price in RUB. 

You can edit Google Sheets, and when you refresh the page, we will see edited data.
