#!/bin/bash
#conda activate photoflask
export FLASK_APP=photoflask.py
export FLASK_ENV=development
flask run

#flask db init
#flask db migrate -m "new table"
#flask db upgrade # or downgrade
