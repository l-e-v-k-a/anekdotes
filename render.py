from flask import Flask, request, redirect, render_template, session
import socket
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"
# app.config['USERS'] = {} # database.login()

@app.route('/deauth')
def deauth():
    session['is_auth'] = False
    return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("loginform.html", error_alert="")
    elif request.method == 'POST':  # Посылаем Логин и Пароль через форму
        username = request.form.get('username')
        password = request.form.get('password')
        #  print(username, password)  # Эта строчка использовалась во время разработки и полезна при отладке
        if username == "olegililev" and password == "pustimenya":
            session["is_auth"] = True  # Если проверка прошла то говорим что пользователь авторизован
            return redirect("/")  # Переадресуем уже авторизованого пользователя на главную
        else:  # Если логин и пароль проверку не прошли то загружаем ту же страницу, но с сообщением об ошибке
            return render_template("loginform.html", error_alert="Неверный логин и/или пароль")

@app.route('/edit/<int:anek>', methods=['POST', 'GET'])
def edit_anek(anek):
    if not session.get('is_auth'):  # Если ты не авторизован то иди авторизуйся
        return redirect("/login")
    if request.method == 'GET':
        info = db.get_joke_by_id(anek)
        fond = db.get_fond_by_num(info[3])
        return render_template("edit.html", num=anek, i=info, fond=fond)
    if request.method == 'POST':
        text = request.form.get('anek_text')
        tags = request.form.get('anek_tags')
        fond = request.form.get('anek_fond')
        if text!='':
            print((anek, f'{text}', f'{tags}', db.get_fond_by_name(fond)))
            db.edit_anek(anek, text, tags, db.get_fond_by_name(fond))
        return redirect(f"/edit/{anek}")


@app.route('/create', methods=['POST', 'GET'])
def add_anek():
    if not session.get('is_auth'):  # Если ты не авторизован то иди авторизуйся
        return redirect("/login")
    if request.method == 'GET':
        return render_template("create.html")
    if request.method == 'POST':
        text = request.form.get('anek_text')
        tags = request.form.get('anek_tags')
        fond = request.form.get('anek_fond')
        if text!='':
            db.create_new_anek(db.get_last_anek()[0]+1, f'{text}', f'{tags}', db.get_fond_by_name(fond))
        print(db.get_last_anek()[0]+1, f'{text}', f'{tags}', db.get_fond_by_name(fond))
        return redirect("/create")


@app.route('/watch/<int:anek>')
def watch_anek(anek):
    info = db.get_joke_by_id(anek)
    fond = db.get_fond_by_num(info[3])
    return render_template("view_anek.html", num=anek, i=info, fond=fond)

@app.route('/delete/<int:anek>')
def delete_anek(anek):
    if not session.get('is_auth'):  # Если ты не авторизован то иди авторизуйся
        return redirect("/login")
    db.delete_anek(anek)
    return redirect("/")

@app.route('/')
def index():
    return render_template("index.html",
                           admin=session.get('is_auth'),
                           info=db.table())

if __name__ == '__main__':
    app.run(debug=True)