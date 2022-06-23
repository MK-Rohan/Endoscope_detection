from flask import Flask, redirect, url_for, request, render_template, request, session
import glob, os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "54321"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/User_list"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@host.docker.internal:3306/User_list"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Information'

    idx = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    password = db.Column(db.String(20, 'utf8mb4_unicode_ci'))

class DataBase(db.Model):
    __tablename__ = 'Corrects'
    idx = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    img = db.Column(db.String(255, 'utf8mb4_unicode_ci'))
    label = db.Column(db.LargeBinary)

@app.route('/', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        return redirect(url_for("Pages"))
    else:
        if not session.get('email'):
            return render_template('index.html')
        else:
            userid = session.get('email')
            return render_template('index.html', userid=userid)

@app.route('/Pages', methods=['GET', 'POST'])
def Pages():
    """ Saving Files and Images Analysis """
    if request.method == 'POST':
        os.system("rm -rf ./static/images/*")
        os.system("rm -rf ./static/out_img*")
        upload = request.files.getlist("file")
        for f in upload:
            f.save("./static/images/" + secure_filename(f.filename))
        return redirect(url_for("results"))
    else:
    	return render_template('Analysis.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return redirect(url_for("contact"))
    else:
        return render_template('contact.html')

@app.route('/example', methods=['GET', 'POST'])
def example():
    if request.method == 'POST':
        return redirect(url_for("example"))
    else:
        return render_template('example.html')

@app.route('/model', methods=['GET', 'POST'])
def model():
    if request.method == 'POST':
        return redirect(url_for("model"))
    else:
        return render_template('Using_model.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        upload = request.form.getlist("checkbox")
        for f in upload:
            img_id = f[-11:]
            src = "./static/images/{}".format(img_id)
            dst = "./static/corrects/{}".format(img_id)
            os.system("cp {} {}".format(src, dst))
        return redirect(url_for("file_upload"))
    else:
        os.system("bash run.sh")
        path = './static/out_img/*'
        file_list = glob.glob(path)
        return render_template('results.html', image_file=file_list)

@app.route('/Signed', methods=['GET', 'POST'])
def signed():
    ##### SQLAlchemy
    if request.method == 'GET':
        return render_template('signed.html')
    else:
        email = request.form.get('email')
        passwd = request.form.get('password')
        try:
            data = User.query.filter_by(email = email, password = passwd).first()
            if data is not None:
                session['email'] = email
                return redirect(url_for("file_upload"))
            else:
                return "Don't Login. Incorrect email address or password."
        except Exception as e:
            return "Don't Login (exception): {}".format(e)


@app.route('/logout', methods=["GET"])
def logout():
    session.pop("email", None)
    return redirect('/')

@app.route('/Register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('email')
        passwd = request.form.get('password')
        con_passwd = request.form.get('con_password')
        if not (email and passwd and con_passwd):
            return "누락된 정보가 있습니다."
        elif passwd != con_passwd:
            return "비밀번호를 확인해주세요."
        else:
            user = User()
            user.password = passwd
            user.email = email
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("signed"))


if __name__ == '__main__':
    app.debug = True
    app.run(port = "5000", debug=True)