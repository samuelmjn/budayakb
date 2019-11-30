from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def hello_world():
   return render_template('add_culture.html')

@app.route('/login')
def login():
    print(request.headers)

if __name__ == '__main__':
   app.run(debug=True)