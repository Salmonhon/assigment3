
from flask import Flask
from flask_sqlalchemy import  SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'salmonhon'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""to skip FSA Deprecation Warning"""
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


db = SQLAlchemy(app)
