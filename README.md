Installation 
------------


How to install Python on Windows 7
https://www.python.org/download/releases/2.7/

1. Download msi for Windows x86/x64

2. Add to $PATH

C:\Python27\;C:\Python27\Scripts\

3. Install virtualenv for Python

C:\pip install virtualenv 

4. Create example directory

C:\myproject

5. Create virtualenv directorey like

C:\myproject\virtualenv venv

6. Put the source code into the created dir C:\myproject

7. Install requirements file: 

C:\myproject\pip install -r requirements.txt

8. Go to Properties




------------
Install on Linux: 

1. Create virtualenv on the directory needed:

/home/b/myproject/ $ pip install virtualenv

2. Put file of the project there: 

3. Install requirements 

$ pip install -r requirements.txt

4. Go to Properties



Properties 
------------

main dir 
./inet_radio  

./inet_radiо/config.py - configuration file


## In the config.py in Linux: 

# Download log
DOWNLOAD_LOG='/home/b/myproject/inet_radio/static/music/downloaded/log_downloaded.txt'

# Download files 
DOWNLOAD_FILES='/home/b/myproject/inet_radio/static/music'



## In the config.py in Windows: 

# Download log
DOWNLOAD_LOG='C:\myproject\inet_radio\static\music\downloaded\log_downloaded.txt'

# Download files 
DOWNLOAD_FILES='C:\myproject\inet_radio\static\music'




Start the app
-------------

Activate virtualenv


## Windows 
Virtualenv activation:

    C:\myproject\cd venv\Scripts
    C:\myproject\venv\Scripts\activate

Deactivation:

    C:\myproject\venv\Scripts\deactivate

Start of the app: 

    C:\myproject\inet_radio\python app.py 

In browser open: 

    http://0.0.0.0:5000/



## Linux: 

    /home/b/myproject $ . venv/bin/activate 

Activated (venv): 

    (venv)/home/bor/myproject $ 

Start app: 

    (venv)/home/bor/myproject/inet_radio $ python app.py 

In browser open:

    http://0.0.0.0:5000/




TODO
---------

Reference
1. How to setup flask for Windows
https://www.youtube.com/watch?v=98JY6MvumVs

2. Python releases
https://www.python.org/download/releases/2.7/

3. Instaling Python on Windows
http://docs.python-guide.org/en/latest/starting/install/win/



