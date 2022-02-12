import os

from flask import Flask, render_template, redirect, request
import json
from loginform import LoginForm
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
def all_jobs():
    session = db_session.create_session()
    data_jobs = session.query(Jobs).all()
    return render_template("work_table.html", title="Журнал работ", data=data_jobs)


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
    args['professions'] = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач',
                           'инженер по терраформированию', 'климатолог',
                           'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
                           'инженер жизнеобеспечения, метеоролог', 'оператор марсохода',
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
    return render_template('auto_answer.html', data=data, field_names=field_names,
                           title=data['title'])


@app.route('/distribution')
def distribution():
    astronauts = ['Том Холланд', 'Эндрю Гарфилд', 'Тоби Магуайр', 'Зендея', 'Мариса Томей']
    return render_template('astronauts_accommodation.html', astronauts=astronauts)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    return render_template('cabin_decoration.html', sex=sex, age=age, title='Каюта')


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
        return redirect('/success')
    return render_template("login.html", title="Аварийный доступ", form=form)


@app.route('/success')
def success():
    return render_template("success.html", title="Успешно")


if __name__ == '__main__':
    main()
