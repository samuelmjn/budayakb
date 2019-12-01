from flask import Flask, render_template, request
from sso.utils import (
    authenticate,
    get_cas_client,
)

app = Flask(__name__)
app.config.from_pyfile('config.py')
@app.route('/')
def hello_world():
   return render_template('add_culture.html')

@app.route('/login')
def login():
    print(request.headers)
    ticket = request.args.get("ticket")
    if ticket is not None:
        client = get_cas_client("https://budayakb.herokuapp.com/login/")
        sso_profile = authenticate(ticket, client)
        print(sso_profile)

if __name__ == '__main__':
   app.run(debug=True)