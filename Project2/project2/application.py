import os

from flask import Flask, request
from flask_socketio import SocketIO, emit
import os
import requests


from flask import Flask, jsonify, render_template, request, session, redirect

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)


channelNames = []


@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    print(username)

    if not username:
        return jsonify({"success": False})

    session["username"] = username

    return jsonify({"success": True, "username": username})


@app.route("/createChannel", methods=["GET", "POST"])
def createChannel():
    if request.method == "GET":
        return render_template("createChannel.html")

    channelName = request.form.get("channelName")


    if not channelName:
        return jsonify({"success": False})

    if channelName not in channelNames:
        channelNames.append(channelName)

    session["channel"] = channelName
    return render_template("layout.html")

@app.route("/showChannelsList", methods=["GET", "POST"])
def showChannelsList():
    return render_template("channels.html", channels=channelNames)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")



