#!/usr/bin/python3
import json

from http_serv.session import *
from models import *
from app import serv, session_store, appdata

def index(req, resp):
    session = session_store.get_store(req)

    if "username" in session:
        resp.redirect("/messenger")

    elif req.method == "GET":
        resp.send_file("./static/html/index.html")

    elif req.method == "POST":
        uname = req.form["username"]

        if appdata.register(uname):
            session["username"] = req.form["username"]
            session.save(req, resp)
            resp.redirect("/messenger")
        else:
            resp.redirect("/")

def messenger(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return
    resp.send_file("./static/html/messenger.html")

def logout(req, resp):
    session = session_store.get_store(req)
    if session:
        if "username" in session:
            appdata.disconnect(session["username"])
        session.delete()
    resp.redirect("/")

def get_users(req, resp):
    resp.headers["Content-Type"] = "application/json"
    resp.write(str(json.dumps(appdata.usernames())))

def serialize_list(items):
    return json.dumps([i.jsonify() for i in items])

def conversations(req, resp):
    session = session_store.get_store(req)

    if not "username" in session:
        resp.redirect("/")
        return

    resp.headers["Content-Type"] = "application/json"
    user = appdata.users[session["username"]]
    resp.write(serialize_list(user.conversations))

def create_group(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return

    print(req.form, req.method)
    if req.method == "POST":
        user = appdata.users[session["username"]]
        #: TODO: proper urldecoding
        participants = req.form["users"].split("%26")
        title = req.form["title"]

        conv = appdata.new_conversation(title, participants)
        resp.write("OK")

def fetch_events(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return

    resp.headers["Content-Type"] = "application/json"
    user = appdata.users[session["username"]]
    e = user.get_events()
    resp.write(serialize_list(e))
    
def msg(req, resp):
    session = session_store.get_store(req)
    if not "username" in session:
        resp.redirect("/")
        return

    if req.method == "POST":
        user = session["username"]
        if "contents" in req.form and "conv" in req.form:
            contents = req.form["contents"] 
            conv = req.form["conv"]
            appdata.msg(user, conv, contents)
            resp.write("OK")

def whoami(req, resp):
    session = session_store.get_store(req)
    if "username" in session:
        resp.write(session["username"])

serv.handle("/", index, methods=["GET", "POST"])
serv.handle("/messenger", messenger, methods=["GET", "POST"])
serv.handle("/conversations", conversations)
serv.handle("/events", fetch_events)
serv.handle("/users", get_users)
serv.handle("/logout", logout)
serv.handle("/whoami", whoami)

serv.handle("/newgroup", create_group, methods=["POST"])
serv.handle("/msg", msg, methods=["POST"])
