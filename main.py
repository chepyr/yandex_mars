import os

import flask
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user

import json

from forms.user import RegisterForm
from forms.loginform import LoginForm
from forms.job import JobsForm

from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def all_jobs():
    session = db_session.create_session()
    data_jobs = session.query(Jobs).all()
    return render_template("work_table.html", title="Журнал работ",
                           data=data_jobs)


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<list_prop>')
def list_prof(list_prop):
    args = {'list': list_prop}
    args['professions'] = ['инженер-исследователь', 'пилот', 'строитель',
                           'экзобиолог', 'врач',
                           'инженер по терраформированию', 'климатолог',
                           'специалист по радиационной защите', 'астрогеолог',
                           'гляциолог',
                           'инженер жизнеобеспечения, метеоролог',
                           'оператор марсохода',
                           'киберинженер', 'штурман', 'пилот дронов']
    return render_template('list_prof.html', **args)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    data = {
        'title': 'Анкета',
        'surname': 'Watney',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': True
    }
    field_names = {
        'surname': 'Фамилия',
        'name': 'Имя',
        'education': 'Образование',
        'profession': 'Профессия',
        'sex': 'Пол',
        'motivation': 'Мотивация',
        'ready': 'Готовы остаться на Марсе?'
    }
    return render_template('auto_answer.html', data=data,
                           field_names=field_names,
                           title=data['title'])


@app.route('/distribution')
def distribution():
    astronauts = ['Том Холланд', 'Эндрю Гарфилд', 'Тоби Магуайр', 'Зендея',
                  'Мариса Томей']
    return render_template('astronauts_accommodation.html',
                           astronauts=astronauts)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    return render_template('cabin_decoration.html', sex=sex, age=age,
                           title='Каюта')


@app.route('/load_photo', methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return render_template("load_photo.html", photo=False)
    elif request.method == 'POST':
        file = request.files['file']
        file.save("static/images/new_pic.jpg")
        return render_template("load_photo.html", photo=True)


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    if request.method == 'POST':
        new_image = request.files['file']
        number = len(os.listdir('static/images/carousel'))
        new_image.save(f"static/images/carousel/{number + 1}.jpg")
    images_names = os.listdir('static/images/carousel')
    return render_template("galery.html", images_names=images_names)


@app.route('/member')
def member():
    with open("templates/members.json", "rt", encoding="utf8") as f:
        data = json.loads(f.read())
    return render_template("member.html", data=data, title='Участник')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/success')
def success():
    return render_template("success.html", title="Успешно")


@app.route('/cookie_test')
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = flask.make_response(f"Вы тут в {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24)
    else:
        res = flask.make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.age.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job', methods=['GET', 'POST'])
@login_required
def add_news():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Добавление работы',
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    main()
