from flask import Flask, request, send_file, render_template, redirect
from base64 import b64encode, b64decode
from urllib.parse import quote_plus, unquote_plus

app = Flask(__name__, static_url_path='', static_folder='templates/static', template_folder='templates')
database = r"sqlite.db"
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)
app.jinja_env.filters['b64encode'] = lambda u: b64encode(u.encode()).decode()
app.jinja_env.filters['b64decode'] = lambda u: b64decode(u.encode()).decode()

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html") 

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)