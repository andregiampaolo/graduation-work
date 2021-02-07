# Run the project


## 1. Virtual env


To execute this project you could use virtual env if it is your choice.

- To install: `pip install virtualenv`
- To create a virtual env: `virtualenv venv` (pattern of name of virtual env is `venv` but you can choose any valid folder name)
- To activate the virtual env: `source venv/bin/activate`
- To deactivate a virtual env you can type: `deactivate`

Remember not to commit the folder of virtual env

**Important:** The python version is 2.7
To create a virtual env with 2.7 use: `virtualenv --python=PYTHON_PATH <path/to/new/virtualenv/>`
To get PYTHON_PATH open a terminal and execute: `python -m site`
Example: `virtualenv --python=/usr/local/bin/python2.7 venv`

## 2. Install dependencies
1. After activate the virtual env
2. Go to folder `lda`
2. Run `pip install -r requirements.txt`

**Important:** Maybe you'll need this like admin (using `sudo`)

## 3. Run server
1. Execute script run-server
2. Access `http://127.0.0.1:5000/` in web browser