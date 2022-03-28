@echo off
set SCRIPT_DIR=%~dp0
pipenv run python -m unittest discover %SCRIPT_DIR%test 1> test_stdout.txt 2> test_results.txt