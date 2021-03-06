from flask import redirect, render_template, url_for, flash, request
from condition_monitor.forms import RegisterForm, LoginForm, UserAccessForm
from condition_monitor.models import Room, Access, User
from condition_monitor import app, httpAuth
from condition_monitor.models import DBConnection
from condition_monitor.models import User
from flask_login import login_user, logout_user, login_required, current_user

db = DBConnection()


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/monitor")
@login_required
def monitor_page():
    rooms = db.getRoomsForUser(current_user.id)
    measurements = {}
    for room in rooms:
        ms = db.getMeasurementsForRoom(room.id)
        measurements[room.name] = {}
        measurements[room.name]["temp"] = [ x.temperature for x in ms]
        measurements[room.name]["hum"] = [ x.humidity for x in ms]
        measurements[room.name]["timestamp"] = [ x.timestamp.strftime("%m-%d %H:%M:%S") for x in ms]
    return render_template("monitor.html", measurements = measurements)

@app.route("/monitor/<uid>")
@login_required
def monitor_page_user(uid):
    rooms = db.getRoomsForUser(uid)
    measurements = {}
    if rooms != None:
        for room in rooms:
            measurements[room.name] = db.getLastMeasurementForRoom(room.id)
    return render_template("monitor.html", measurements = measurements)


@app.route("/measurements", methods = ["POST"])
@httpAuth.login_required
def measurement():
    temp = request.form.get("temperature")
    print(temp)
    return ""

@app.route("/tables")
@login_required
def tables_page():
    rooms = db.getRoomsForUser(1)
    measurements = {}
    for room in rooms:
        measurements[room.name] = db.getMeasurementsForRoom(room.id)
    return render_template("tables.html", measurements = measurements)

@app.route("/admin_panel", methods=["GET", "POST"])
@login_required
def admin_panel():
    grantForm = UserAccessForm()
    if current_user.role() == "ADMIN":
        if grantForm.validate_on_submit():
            if not db.getRoom(grantForm.room.data) in db.getRoomsForUser(db.getUser(grantForm.user.data).id):
                db.grantAccess(grantForm.user.data, grantForm.room.data)
                db.flush()
                flash(f"Succesfuly grantet acces to room {grantForm.room.data} to user {grantForm.user.data}", category="success")
            else:
                flash(f"User {grantForm.user.data} already have accesss to room {grantForm.room.data}", category="danger")
        return render_template("admin_panel.html", form = grantForm)
    else:
        flash("You are not administrator of this service!", category="danger")
        return redirect(url_for("home_page"))

@app.route("/tables/<roomname>")
@login_required
def tables_page_room(roomname):
    room = db.getRoom(roomname)
    measurements = {}
    if room != None:
        measurements[room.name] = db.getMeasurementsForRoom(room.id)
    return render_template("tables.html", measurements = measurements)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        flash("You are already logged in", category = "danger")
        return redirect(url_for('home_page'))
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created succesfully! You are now logged in as {user_to_create.username}", category = "success")
        return redirect(url_for('tables_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error with creating a user: {error}', category='danger')
            
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        flash("You are already logged in", category = "danger")
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('monitor_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))