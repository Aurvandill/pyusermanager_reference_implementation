from gevent import monkey
monkey.patch_all()
from bottle import route, run, post, get, static_file, request, redirect, HTTPResponse

import filestuff

@get('/')
def index():
    return filestuff.get_template("header.html") + filestuff.get_template("index.html") + filestuff.get_template("footer.html")


@get('/static/<filename>')
def static_files(filename):
    return static_file(str(filename), root="./static/")

run(host="127.0.0.1" , port=1338, debug=True, server='gevent')