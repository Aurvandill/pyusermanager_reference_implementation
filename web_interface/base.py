import bottle
from bottle import route, run, post, get, static_file, request, redirect, HTTPResponse, response

import filestuff

app = bottle.app()

config={"api_url":"http://172.28.117.204:1337"}


@app.get('/')
def index():
    return filestuff.get_template("header.html",**config) + filestuff.get_template("index.html") + filestuff.get_template("footer.html")

@app.get('/login')
def login():
    return filestuff.get_template("header.html",**config) + filestuff.get_template("login.html") + filestuff.get_template("footer.html")

@app.get('/users')
def users():
    return filestuff.get_template("header.html",**config) + filestuff.get_template("users.html") + filestuff.get_template("footer.html")

@app.get('/user/<username>')
def user_info(username):
    return filestuff.get_template("header.html",**config) + filestuff.get_template("user.html") + filestuff.get_template("footer.html")

@app.get('/static/<filename>')
def static_files(filename):
    return static_file(str(filename), root="./static/")

@app.get('/jquery.js')
def static_jquery():
    return static_file("jquery.js", root="./jquery/dist")

app.run(host="0.0.0.0" , port=1338, debug=True, server='bjoern')