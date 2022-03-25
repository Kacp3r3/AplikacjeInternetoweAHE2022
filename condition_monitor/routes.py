from flask import redirect, render_template, url_for
from condition_monitor.forms import RegisterForm
from condition_monitor.models import Room, Access, User
from condition_monitor import app
from condition_monitor.models import DBConnection
from condition_monitor.models import User

db = DBConnection()

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/monitor")
def monitor_page():
    rooms = db.getRoomsForUser(1)
    measurements = {}
    for room in rooms:
        measurements[room.name] = db.getLastMeasurementForRoom(room.id)
    print(measurements)
    return render_template("monitor.html", measurements = measurements)

@app.route("/monitor/<uid>")
def monitor_page_user(uid):
    rooms = db.getRoomsForUser(uid)
    measurements = {}
    if rooms != None:
        for room in rooms:
            measurements[room.name] = db.getLastMeasurementForRoom(room.id)
    print(measurements)
    return render_template("monitor.html", measurements = measurements)


@app.route("/tables")
def tables_page():
    rooms = db.getRoomsForUser(1)
    measurements = {}
    for room in rooms:
        measurements[room.name] = db.getMeasurementsForRoom(room.id)
    return render_template("tables.html", measurements = measurements)

@app.route("/tables/<roomid>")
def tables_page_room(roomid):
    room = db.getRoom(roomid)
    measurements = {}
    if room != None:
        measurements[room.name] = db.getMeasurementsForRoom(room.id)
    return render_template("tables.html", measurements = measurements)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('tables_page'))

    if form.errors != {}:
        for error in form.errors.values():
            print(f"Error : {error}")
            
    return render_template("register.html", form=form)