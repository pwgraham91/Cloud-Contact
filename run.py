#!flask/bin/python
from app import app
from config import SECRET_KEY

app.secret_key = SECRET_KEY
app.run(debug=True)
