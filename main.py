from flask import url_for, Flask, render_template
import json

app = Flask(__name__)


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


@app.route('/member')
def member():
    with open("templates/members.json", "rt", encoding="utf8") as f:
        data = json.loads(f.read())
    return render_template("member.html", data=data, title='Участник')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
