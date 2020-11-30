from flask import Blueprint, current_app, Markup, jsonify, json, render_template
from flask import make_response, session, flash, redirect, url_for, request, Response
from model import Users, Datas
from serializerUser import UsersSchema
from serializerData import DatasSchema
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
import pdfkit
import json
from time import time
from datetime import datetime
import random
from bs4 import BeautifulSoup
import requests
import httplib2


bp_users = Blueprint('users', __name__)


# @bp_users.route("/")
# def index():
#     return redirect(url_for('users.login'))
#     return render_template('login.html')


@bp_users.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['nm']
        password = hashlib.sha1(
            request.form['pwd'].encode('utf-8')).hexdigest()
        pw = Users.query.filter_by(password=password).first()
        user = Users.query.filter_by(email=email).first()
        if not user or not pw:
            message = Markup(
                "<strong><i>E-mail</i></strong> ou <strong><i>senha</i></strong> inválidos, verifique!!")
            flash(message, "error")
            return redirect(url_for("users.login"))
        login_user(user)
        session.permanent = True
        return redirect(url_for("users.home"))
    return render_template('login.html')


@bp_users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']
        email = request.form['email']
        password = request.form['password']
        aditional_infos = request.form['aditional_infos']

        # verifica se tem vazio
        # if (first_name == "") or (last_name == "") or (birthday == "") or (email == "") or (password == "") or (aditional_infos == ""):
        # flash("Preencha todos os campos")

        us = UsersSchema()

        # cria usuario para passar as infos recebidas
        user = Users()
        user.first_name = first_name
        user.last_name = last_name
        user.birthday = birthday
        user.email = email
        user.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        user.aditional_infos = aditional_infos

        # salva no banco o usuario
        current_app.db.session.add(user)
        current_app.db.session.commit()
        message = Markup("Dados Atualizados!!")
        flash(message, "success")
    return render_template("register.html")


@bp_users.route('/home')
def home():
    return render_template('base.html')


@bp_users.route('/homeDadosTabela')
def homeDadosTabela():
    datas = DatasSchema(many=True)
    my_user = current_user.get_id()
    result = Datas.query.join(Users, Users.id == Datas.id_user).filter(
        Datas.id_user == my_user).order_by(Datas.id.desc()).limit(5)
    return datas.jsonify(result)


@bp_users.route('/profile')
def profile():
    return render_template('profile.html')


@bp_users.route('/RelatorioSimples')
def RelatorioSimples():
    return render_template('table.html')


@bp_users.route('/ListDatas')
def ListDatas():
    datas = DatasSchema(many=True)
    my_user = current_user.get_id()
    result = Datas.query.join(Users, Users.id == Datas.id_user).filter(
        Datas.id_user == my_user).order_by(Datas.id.desc()).all()
    return datas.jsonify(result), 200


@bp_users.route('/GenerateSimpleReport', methods=['GET', 'POST'])
def GenerateSimpleReport():
    datas = DatasSchema(many=True)
    my_user = current_user.get_id()
    result = Datas.query.join(Users, Users.id == Datas.id_user).filter(
        Datas.id_user == my_user).all()

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    html = render_template("reports_pdf.html", result=result)

    pdf = pdfkit.from_string(
        html, False, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=relatorio_simples.pdf"
    return response
    return redirect(url_for('users.ListDatas'))
    return render_template('table.html', result=result)


@bp_users.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            list_item = []
            content = httplib2.Http().request(
                "http://joaovks.pythonanywhere.com/set")
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 'value': str(int(content[1]))})
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    return Response(generate_random_data(), mimetype='text/event-stream')


@bp_users.route('/inserirDados', methods=['POST'])
def inserirDados():
    #my_user = current_user.get_id()
    my_user = 1
    while True:
        content = httplib2.Http().request(
            "http://joaovks.pythonanywhere.com/set")

        data_atual = str(datetime.now())
        id_user = my_user
        batimento = str(int(content[1]))

        data = DatasSchema(many=True)
        dados = Datas()
        dados.id_user = id_user
        dados.date = data_atual
        dados.data = batimento
        print(data)

        current_app.db.session.add(dados)
        current_app.db.session.commit()
    return data.jsonify(dados), 200


@bp_users.route('/insertDadosApp', methods=['POST'])
def insertDadosApp():
    id_user = request.json['id_user']
    data_atual = request.json['date']
    batimento = request.json['data']

    # verifica se tem vazio
    if (id_user == "") or (data_atual == "") or (batimento == ""):
        return jsonify("Verificar se os dados estão corretos"), 401

    data = DatasSchema()
    dados = Datas()
    dados.id_user = id_user
    dados.date = data_atual
    dados.data = batimento
    print(dados)

    # salva no banco os dados
    current_app.db.session.add(dados)
    try:
        current_app.db.session.commit()
    except:
        return data.jsonify("Erro"), 401

    return data.jsonify(dados), 201


@bp_users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@bp_users.route('/selectJson', methods=['GET', 'POST'])
def selectJson():
    us = UsersSchema(many=True)
    result = Users.query.all()
    return us.jsonify(result), 200


@bp_users.route('/users')
def users():
    us = UsersSchema(many=True)
    result = Users.query.all()
    # return us.jsonify(result), 200
    return render_template('index.html',  title='Dados', result=result)


@bp_users.route('/delete/<id>', methods=['GET'])
def delete(id):
    Users.query.filter(Users.id == id).delete()
    current_app.db.session.commit()

    return jsonify('Deleted Success!!')


@bp_users.route('/update/<int:id>', methods=['POST'])
def update(id):
    updateQuery = Users.query.filter(Users.id == id)
    updateQuery.update(request.json)

    us = UsersSchema()

    current_app.db.session.commit()
    return us.jsonify(updateQuery.first())


@bp_users.route('/update_profile/<int:id>', methods=['GET', 'POST'])
def update_teste(id):
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthday = request.form['birthday']
        email = request.form['email']
        password = hashlib.sha1(
            request.form['password'].encode('utf-8')).hexdigest()
        aditional_infos = request.form['aditional_infos']

        updateQuery = Users.query.filter(Users.id == id)

        updateQuery.update({Users.first_name: first_name, Users.last_name: last_name, Users.birthday: birthday,
                            Users.email: email, Users.password: password,
                            Users.aditional_infos: aditional_infos})

        current_app.db.session.commit()

        message = Markup("Dados Atualizados!!")
        flash(message, "success")
        return redirect(url_for('users.profile'))
    return render_template("profile.html")


@bp_users.route('/insert', methods=['POST'])
def insert():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    birthday = request.json['birthday']
    email = request.json['email']
    password = request.json['password']
    aditional_infos = request.json['aditional_infos']

    # verifica se tem vazio
    if (first_name == "") or (last_name == "") or (birthday == "") or (email == "") or (password == "") or (aditional_infos == ""):
        return jsonify("Preencha todos os campos"), 401

    us = UsersSchema()

    # cria usuario para passar as infos recebidas
    user = Users()
    user.first_name = first_name
    user.last_name = last_name
    user.birthday = birthday
    user.email = email
    user.password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    user.aditional_infos = aditional_infos

    # salva no banco o usuario
    current_app.db.session.add(user)
    try:
        current_app.db.session.commit()
    except:
        return us.jsonify("Erro"), 401

    return us.jsonify(user), 201
