#!/bin/bash
#conda activate photoflask
export FLASK_APP=photoflask.py
export FLASK_ENV=development
flask run --host=0.0.0.0

#flask db init
#flask db migrate -m "new table"
#flask db upgrade # or downgrade

# initial setup in a Python shell
#EMAIL=xxxxx@gmail.com USERNAME=xxxxx PASSWORD=xxxxx python
#>>> from photoflask import app
#>>> from app import db
#>>> with app.app_context():
#...   db.create_all()
#...

