import os,sys
from photoflask import app
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    # Check if the existing table contain data, if not then initialize with csv insert
    s = db.session()
    if len(s.query(User).all()) == 0:
        print('No data in the table detected.')
        print('Initialising the table in database.')
        engine = s.get_bind()

        try:
            email = os.environ['EMAIL']
        except KeyError:
            print("$EMAIL not set")
            sys.exit(1)

        try:
            password = os.environ['PASSWORD']
        except KeyError:
            print("$PASSWORD not set")
            sys.exit(1)

        try:
            username = os.environ['USERNAME']
        except KeyError:
            print("$USERNAME not set")
            sys.exit(1)

        new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

app.run(port=5020, debug=True)
