from flask import Flask, render_template, request, make_response, redirect, flash, render_template_string
from helper.sso import (
    authenticate,
    get_cas_client,
)

from repository.culture_repository import CultureRepository, QueryType
from repository.model.culture import Culture
from helper.auth import get_current_user
import config
import json
import sys
import csv

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = "fasilkom"
app.jinja_env.globals.update(get_current_user=get_current_user)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/search')
def search():
    query = request.args.get("query")
    search_by = request.args.get("filter")
   
    if search_by:
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
            redirect_script = ''' 
            <script>
            window.opener.location = '/';
            window.close();
            </script>
            '''
            res = make_response(render_template_string(redirect_script))
            res.set_cookie('user_name', sso_profile["username"])
            return res
        else:
            flash("Error on login with SSO UI!")
            return redirect("/")
            
@app.route('/logout')
def logout():
    res = make_response(redirect("/"))
    res.delete_cookie('user_name')
    return res

@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        c_type = request.form['type']
        province = request.form['province']
        url = request.form['url']

        culture_object = Culture(name, c_type, province, url)
        r.create([culture_object])
        persist_to_storage(config.DB_FILE)
        flash("Data berhasil ditambahkan")
        redirect('/search')
    
    if get_current_user() == None:
        flash("Anda harus login untuk menambahkan budaya!")
        return redirect('/')

    return render_template('culture_detail.html', page_type="add")


@app.route('/edit/<name>', methods = ['POST', 'GET'])
def edit_culture(name):
    if request.method == "POST":
        name = request.form['name']
        c_type = request.form['type']
        province = request.form['province']
        url = request.form['url']
        r.update(Culture(name, c_type, province, url))
        persist_to_storage(config.DB_FILE)
        flash("Data berhasil diubah")
        return redirect('/search')
    obj = r.find_by_name(name)

    if get_current_user() == None:
        flash("Anda harus login untuk mengubah budaya!")
        return redirect('/')

    return render_template('culture_detail.html', page_type="edit", obj = obj)

@app.route('/delete/<name>')
def delete_culture(name):
    r.delete(name)
    persist_to_storage(config.DB_FILE)
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
            if len(record) != 4:
                continue
            newCulture = Culture(record[0], record[1], record[2], record[3])
            inputs.append(newCulture)
        r.create(inputs)
        flash("Data berhasil diimpor")
        return redirect('/')

@app.route('/statistics/<name>')
def statistics(name):
    if name == "type":
        res = r.count_by_type()
        return render_template('statistics.html', stat = res)
    elif name == "province":
        res = r.count_by_province()
        return render_template('statistics.html', stat = res)

@app.errorhandler(500)
def internal_error(error):
    flash("Unexpected error happened!")
    return redirect('/')

@app.errorhandler(404)
def not_found(error):
    flash("Oops! Page not found")
    return redirect('/')

def persist_to_storage(storage_dir: str):
    file = open(storage_dir, "w")
    res = [str(i) for i in r.find_all()]
    content = '\n'.join(res)
    file.write(content)
    file.close()

if __name__ == '__main__':
    r = CultureRepository()

    # Load database file
    with open(config.DB_FILE, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        rows = []
        for row in csv_reader:
            newCulture = Culture(row[0], row[1], row[2], row[3])
            rows.append(newCulture)
        csv_file.close()
    r.create(rows)
    
    app.run(debug=True)
   