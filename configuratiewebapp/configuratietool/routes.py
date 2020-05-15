from flask import render_template, url_for, request, redirect, flash, session, jsonify
from configuratietool import app, db, bcrypt
from configuratietool.formulieren import RegistratieFormulier, LoginFormulier, WijzigingFormulier 
from configuratietool.configuraties import ConfiguratieFormulier
from configuratietool.models import User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta


@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    form = ConfiguratieFormulier()
    output = ""

    if current_user.is_authenticated:
        if form.validate_on_submit():
            output += form.configuratie_vpn.data
            output += form.configuratie_interface_wan_ip.data

            if form.configuratie_fanServer.data and form.configuratie_fanSerial.data:
                output += (f"""config log fortianalyzer setting
 set status enable
 set server \""""  + form.configuratie_fanServer.data +  """\" 
 set serial """ + form.configuratie_fanSerial.data + """
end\n""")
        return render_template("home.html", form=form, output=output)
    else:
        return redirect(url_for("login"))

@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = WijzigingFormulier()
    if current_user.is_authenticated:
        usr = User.query.filter_by(username=current_user.username.lower()).first()
        if form.validate_on_submit():
            if usr and bcrypt.check_password_hash(usr.password, form.oldpassword.data):
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                db.session.commit()
                flash(f'{current_user.username} gewijzigd!', 'success')
                return redirect(url_for('account'))
            else:
                flash(f'Inloggegevens niet correct, probeer het overnieuw.', 'danger')
    return render_template("account.html", form=form)
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistratieFormulier()
    if current_user.is_authenticated:

        return redirect(url_for("home"))
    else:
        if form.validate_on_submit():
            hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            usr = User(username=form.username.data.lower(), password=hash_pwd)  
            db.session.add(usr)
            db.session.commit()
            flash(f'Account aangemaakt voor {form.username.data}!', 'success')
            return redirect(url_for('login'))
            
    return render_template('registreren.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'U bent ingelogd als {current_user.username}', 'success')
        return redirect(url_for("home"))
    else:
        form = LoginFormulier()
        if form.validate_on_submit():
            usr = User.query.filter_by(username=form.username.data.lower()).first()
            
            if usr and bcrypt.check_password_hash(usr.password, form.password.data):
                login_user(usr, remember=form.remember.data, duration=timedelta(minutes=5))
                flash(f'U bent ingelogd als {usr.username}!', 'success')
                return redirect(url_for("home"))
            else:
                flash(f'Inloggen niet gelukt, probeer het overnieuw.', 'danger')
        return render_template('login.html', form=form)

@app.route('/generator')
def generator():
    try:
	    return jsonify(result=request.args.get('configuratie_vpn', 0, type=str))
	
    except Exception as e:
	    return str(e)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@app.route("/logout")
def logout():
    logout_user()
    flash(f'Uitgelogd!', 'success')
    return redirect(url_for('login'))