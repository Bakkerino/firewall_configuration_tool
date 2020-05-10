from flask import render_template, url_for, request, redirect, flash, session
from configuratietool import app, db, bcrypt
from configuratietool.formulieren import RegistratieFormulier, LoginFormulier
from configuratietool.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
#@login_required
def home():
    if current_user.is_authenticated:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))

#@app.route("/user", methods=["POST", "GET"])
#def user():
#    if "user" in session:
#        user = session["user"]
#        return render_template("user.html",  user=user, form=form)
#    else:
#        return redirect(url_for("login"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistratieFormulier()
    if current_user.is_authenticated:

        return redirect(url_for("home"))
    else:
        if form.validate_on_submit():
            hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            usr = User(username=form.username.data, password=hash_pwd)  
            db.session.add(usr)
            db.session.commit()
            flash(f'Account aangemaakt voor {form.username.data}!', 'success')
            return redirect(url_for('login'))
            
    return render_template('registreren.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'U bent ingelogd als {current_user.username}', 'success')
        return redirect(url_for("home"))
    else:
        form = LoginFormulier()
        if form.validate_on_submit():
            usr = User.query.filter_by(username=form.username.data).first()
            
            if usr and bcrypt.check_password_hash(usr.password, form.password.data):
                login_user(usr, remember=form.remember.data)
                flash(f'U bent ingelogd als {usr.username}!', 'success')
                return redirect(url_for("home"))
            else:
                flash(f'Inloggen niet gelukt, probeer het overnieuw.', 'danger')
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash(f'Uitgelogd!', 'success')
    return redirect(url_for('login'))