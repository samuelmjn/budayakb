from flask import Flask, render_template, request, make_response, redirect, flash
from helper.sso import (
    authenticate,
    get_cas_client,
)

from repository.culture_repository import CultureRepository, QueryType
from repository.model.culture import Culture
from helper.auth import is_authenticated
import config
import json

r = CultureRepository()

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = "ngews"
app.jinja_env.globals.update(is_authenticated=is_authenticated)

@app.route('/')
def index():
    return redirect('/search')

@app.route('/search')
def search():
    query = request.args.get("query")
    search_by = request.args.get("filter")
    if query and search_by:
        if search_by == "province":
            query_type = QueryType.PROVINCE
        elif search_by == "name":
            query_type = QueryType.NAME
        elif search_by == "type":
            query_type = QueryType.TYPE
        else:
            query_type = None

        res, _ = r.search(query, query_type)
        return render_template('view_culture.html', result = res)

    return render_template('view_culture.html')

@app.route('/login')
def login():
    ticket = request.args.get("ticket")
    if ticket is not None:
        client = get_cas_client(config.BASE_URL + "/login")
        sso_profile = authenticate(ticket, client)
        print(sso_profile)
        if sso_profile is not None:
            res = make_response(redirect("/"))
            res.set_cookie('user_name', sso_profile["username"])
            return res
        else:
            flash("Error on login")
            return redirect("/")
            


@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        c_type = request.form['type']
        province = request.form['province']
        url = request.form['url']

        culture_object = Culture(name, c_type, province, url)
        r.create([culture_object])
        flash("Data berhasil ditambahkan")
        redirect('/add')
    return render_template('culture_detail.html', page_type="add")


@app.route('/edit/<name>', methods = ['POST', 'GET'])
def edit_culture(name):
    if request.method == "POST":
        name = request.form['name']
        c_type = request.form['type']
        province = request.form['province']
        url = request.form['url']
        r.update(Culture(name, c_type, province, url))
        flash("Data berhasil diubah")
        return redirect('/search')
    obj = r.find_by_name(name)
    return render_template('culture_detail.html', page_type="edit", obj = obj)

@app.route('/delete/<name>')
def delete_culture(name):
    r.delete(name)
    flash("Data berhasil dihapus")
    return redirect('/search')

@app.route('/import', methods=['POST'])
def import_culture():
    if request.method == "POST":
        file = str(request.files['imported_file'].read(), 'utf-8')
        rows = file.split('\n')
        inputs = []
        for row in rows:
            record = row.split(',')
            newCulture = Culture(record[0], record[1], record[2], record[3])
            inputs.append(newCulture)
        r.create(inputs)
        flash("Data berhasil diimpor")
        return redirect('/')

@app.route('/statistics')
def stat():
    return redirect('/statistics/all')

@app.route('/statistics/<name>')
def statistics(name):
    if name == "type":
        res = r.count_by_type()
        return render_template('statistics.html', stat = res)
    elif name == "province":
        res = r.count_by_province()
        return render_template('statistics.html', stat = res)
    elif name == "all":
        return render_template('statistics.html')
    else:
        return redirect('/statistics/all')


if __name__ == '__main__':
   app.run(debug=True)