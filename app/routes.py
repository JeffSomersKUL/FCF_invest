from app import app
import os
from flask import render_template
from flask import send_from_directory


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),'favicon.ico'
    )

@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")
