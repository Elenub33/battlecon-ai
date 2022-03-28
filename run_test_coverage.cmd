@echo off
if exist htmlcov\ rmdir htmlcov\
pipenv run coverage run --source src -m unittest discover
pipenv run coverage html
if exist .coverage del .coverage