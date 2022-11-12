# BACKEND-DJANGO
![Image text](/django.png)

## PROJECT DOWNLOAD

* HTTPS type
~~~sh
git clone https://github.com/JFOZ1010/backend-django.git
~~~

* SSH type
~~~sh
git clone git@github.com:JFOZ1010/backend-django.git
~~~

* Github CLI
~~~sh
gh repo clone JFOZ1010/backend-django
~~~


## INSTALL

Dependency: python3

* Windows
~~~sh
cd backend-django
pip install virtualenv
virtualenv -p py env
./env/Scripts/activate
pip install -r requirements.txt 
~~~

* MacOS
~~~sh
cd backend-django
python3 -m venv venv
alias avenv=source\ venv/bin/activate
avenv
pip install -r requirements.txt 
~~~

* Linux
~~~sh
cd backend-django
python3 -m pip install --upgrade pip
pip install virtualenv
virtualenv env --python=python3
source env/bin/activate
pip install -r requirements.txt 
~~~