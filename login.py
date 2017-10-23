from flask import session


def login(role, password):
    if role == "scheduler" and password == "scheduler":
        session['loggedin'] = True
        session['role'] = "scheduler"
    elif role == "presenter" and password == "presenter":
        session['logginin'] = True
        session['role'] = "presenter"
