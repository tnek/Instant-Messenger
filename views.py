#!/usr/bin/python3
import json

from http_serv.session import *
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
            appdata.leave(session["username"])
        session.delete()
    resp.redirect("/")

def get_users(req, resp):
    resp.headers["Content-Type"] = "application/json"
    resp.write(str(json.dumps(appdata.usernames())))

def conversations(req, resp):
    session = session_store.get_store(req)

    if not "username" in session:
        resp.redirect("/")
        return

    resp.headers["Content-Type"] = "application/json"

#    user = appdata.get_user(username)
#    resp.write(json.dumps([i.jsonify() for i in appdata.conversations))
#    output = {
#            "conversations": appdata.conversations.jsonify()
#            "pms": user.get_pms()
#            }

def message(req, resp):
    pass

serv.handle("/", index, methods=["GET", "POST"])
serv.handle("/users", get_users)
serv.handle("/messenger", messenger, methods=["GET", "POST"])
serv.handle("/logout", logout)
serv.handle("/conversations", conversations)

