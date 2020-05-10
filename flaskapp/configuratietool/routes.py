from flask import render_template, url_for, request, redirect, flash, session
from configuratietool import app
from configuratietool.formulieren import RegistratieFormulier, LoginFormulier
from configuratietool.models import User

@app.route("/")
@app.route("/home")
def home():
    if "user" in session:
        user = session["user"]
        return render_template("home.html", user=user)
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
    if "user" in session:
        user = session["user"]
        return render_template('registreren.html', title='Register', user=user, form=form)
    else:
        if form.validate_on_submit():
            hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            usr = User(username=form.username.data, password=hash_pwd)  
            db.session.add(usr)
            db.session.commit()
            flash(f'Account aangemaakt voor {form.username.data}!', 'success')
            return redirect(url_for('login'))
            
            
            
            
            #if User.query.filter_by(username=form.username.data).first().username:
            #    flash(f'Probeer het overnieuw!', 'danger')
            #else:    
                #session["user"] = form.username.data
                #session.permanent = True
            
    return render_template('registreren.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if "user" in session:
        user = session["user"]
        flash(f'U bent ingelogd als {user}', 'success')
        return redirect(url_for("home"))
    else:
        form = LoginFormulier()
        if form.validate_on_submit():
            #flash(f'test {user_exist.naam}!', 'success')
            
            if form.username.data == User.query.filter_by(username=form.username.data, password=form.password.data).first().username:
                session.permanent = True
                session["user"] = User.query.filter_by(username=form.username.data, password=form.password.data).first().username
                flash(f'Je bent ingelogd als {session["user"]}!', 'success')
                return redirect(url_for('home'))
            else:
                flash(f'Inloggen niet gelukt, probeer het overnieuw.', 'danger')
        return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash(f'Uitgelogd!', 'success')
    return redirect(url_for('login'))