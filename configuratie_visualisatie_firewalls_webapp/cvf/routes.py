import os
from flask import render_template, url_for, request, redirect, flash, session, jsonify
from cvf import app, db, bcrypt
from werkzeug.utils import secure_filename

from cvf.formulieren import RegistratieFormulier, LoginFormulier, WijzigingFormulier 
from cvf.configuraties import ConfiguratieFormulier
from cvf.models import User
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta
from cvf.parsingengine import readFile, cfgFileParsing, verify_filename, verify_filesize, jsonToHTML
from cvf.cfghulpengine import genFortianalyzer

@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    form = ConfiguratieFormulier()
    if current_user.is_authenticated:
        return render_template("home.html", form=form)
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

@app.route("/configuratieimport", methods=['GET', 'POST'])
@login_required
def configuratieimport():
    extension = ""
    if request.method == 'POST':
        if request.files:

            if "filesize" in request.cookies:
                if not verify_filesize(request.cookies["filesize"]):
                    if app.config["DEBUG"]: print("Maximum bestandgrootte overschreden")
                    flash(f'Maximum bestandgrootte van {round(app.config["MAX_FILESIZE"]/1000, 2)}kB overschreden', 'danger')
                    return redirect(request.url)

            cfgbestand = request.files["cfgbestand"]

            if cfgbestand.filename == "":
                print("Geen bestandsnaam")
                return redirect(request.url)

            if verify_filename(cfgbestand.filename):
                bestandsnaam = secure_filename(cfgbestand.filename)

                cfgbestand.save(os.path.join(app.config["CFG_UPLOADS"], bestandsnaam))
                if app.config["DEBUG"]: print("#########################################"); print("Input: ", cfgbestand, bestandsnaam)
                cfgbestand = readFile(bestandsnaam)
                cfgjson = cfgFileParsing(bestandsnaam)
                cfghtml = jsonToHTML(cfgjson)
                return render_template('configuratieimport.html', cfgbestand=cfgbestand, cfgjson=cfgjson, cfghtml=cfghtml)    

            else:
                for x in app.config["ALLOWED_IMPORTFILE_EXTENSIONS"]: extension += "." + x.lower() + " "
                if app.config["DEBUG"]: print("Bestandsextentie niet toegestaan, gebruik", extension)
                flash(f'Bestandsextentie niet toegestaan, gebruik {extension}', 'danger')
                return redirect(request.url)    
    else:
        return render_template('configuratieimport.html')


@app.route("/configuratiehulp", methods=['GET', 'POST'])
@login_required
def configuratiehulp():
    form = ConfiguratieFormulier()
    commandOutput = feedbackOutput = ""
    output = []

    if current_user.is_authenticated:
        if form.validate_on_submit():
            commandOutput += form.configuratie_vpn.data
            commandOutput += form.configuratie_interface_wan_ip.data

            if form.configuratie_fanServer.data and form.configuratie_fanSerial.data:
                output = (genFortianalyzer(form.configuratie_fanServer.data, form.configuratie_fanSerial.data))
                commandOutput += output[0] 
                feedbackOutput += output[1]
        return render_template("configuratiehulp.html", form=form, commandOutput=commandOutput, feedbackOutput=feedbackOutput)
    else:
        return redirect(url_for("login"))

    
   