import sys
import os

sys.path.append(os.getcwd())
from flask import Flask, render_template, redirect, url_for
import anki_conn

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("revise", candidate_str="_".join(anki_conn.get_learn_state_words())))

@app.route('/revise/<candidate_str>')
def revise(candidate_str):
    return render_template("index.html", candidate_str=candidate_str)

@app.route('/complete')
def complete(candidate_str):
    return render_template("index.html", candidate_str=candidate_str)

app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8700)
