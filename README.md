# internship_mysite
This website is based on the official [django tutorial](https://www.djangoproject.com/start/).
It could be used to start polls or just ask questions. The administrator can create questions and add them to a survey.
Everybody can see the results. On this way the administrator can asks his friends for events or ideas, completly anonym.

Author: Simon Heuschkel


deployment:
* no requirement.txt or Pipfile is written
* django>=2.1.2 and python>=3.5 must be installed  (pip install django)
* to start via command line:  
  * get in the project ordner with the manage.py   
  * type the command: py manage.py runserver  
  * testing the polls app: py manage.py test polls  
* the database is uploaded, to bring some sample data and an admin, that the app could be started without creating a user
  * name=admin
  * password=admin

functionalities:
* Basic funtionalities from the tutorial
* Survey attribute for question
* Admin can create a survey
* List with all questions
* ... some more little changes in the codestyle/html structure etc.
* The application may contain some more code snippets or files, which aren't in use, f.e. forms.py.
  Those are just there, because I will continue working on it after the application periode.
  
 design:
 * [w3css](https://www.w3schools.com/w3css/) is used to design a few parts of the website. It's a lightweight css framework, which requieres no license. 
 * codestyle checked with flake8

  
