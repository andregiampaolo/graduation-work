# Web crawler

This project was created to get resumes from a website [Banco Nacional de Empregos - BNE](https://www.bne.com.br/). It was developed a web crawler with `scrapy` a python library. This web crawler allowed download the resumes and create the 'database' used in my graduation work.

You can find the result of the web crawler inside of `resumes` folder at the root of the project.

**Important:** Unfortunately the BNE website has completely changed (front-end, links...), so this web crawler doesn't work anymore.
If you want make a contribuition to improve the project feel free :) (Tip: change the `parse` function inside `resume.py` file)

## Dependencies

Python version 2.7:

- scrapy=1.5.0

## Execute crawler

The project has two web crawlers:

1. The first called `links_resume` create a list of links, so we can use these links to get the data.
To execute this web crawler:
1.1 go to folder: `./list_resume`
1.2 execute the command: `scrapy crawl links_resume`
The list of links can be found in `./list_resume/list_resume/spinders/links/`. Files `resume-links.txt` and `resume-links1.txt` contains the links used to download the resumes

2. The second called `resume` and get the list of links created before and try to get the data.
To execute this web crawler:
2.1 go to folder: `./list_resume`
2.2 execute the command: `scrapy crawl resume`
The resumes can be found in  `./list_resume/resumes`. Files `resume.txt` and `resume1.txt` contain the data used in my graduation work

## Virtual env

To execute this project you could use virtual env if it is your choice.

- To install: `pip install virtualenv`
- To create a virtual env: `virtualenv venv` (pattern of name of virtual env is `venv` but you can choose any valid folder name)
- To activate the virtual env: `source venv/bin/activate`
- To deactivate a virtual env you can type: `deactivate`

Remember not to commit the folder of virtual env
