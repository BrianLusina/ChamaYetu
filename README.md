# ChamaYetu

Application to better manage SME groups and *chamas*.

## Project Structure

    /ChamaYetu
         |-- run.py
         |-- config.py
         |__ /venv             # Virtual Environment, not pushed to git
         |__ /app              # Our Application Module
             |-- __init__.py
             |-- /mod_auth # handles all authentication with logins
                 |-- __init__.py
                 |-- controllers.py
                 |-- models.py
         |-- views.py                
            |__ /templates
                |__ /auth
                    |-- forgot.html
                    |-- login.html
                    |-- signup.html
                404.html
            |__ /static
                |__ ..
                |__ .
            |__ ..
            |__ .

### Project Breakdown


