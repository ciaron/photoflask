#!/bin/bash
conda activate photoflask
export FLASK_APP=photoflask.py
export FLASK_ENV=development
flask run
