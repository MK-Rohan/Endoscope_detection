from flask import Flask, redirect, url_for, request, render_template, request
import glob, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
SCOPES = 'https://www.googleapis.com/auth/drive.file'

@app.route('/', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        return redirect(url_for("Pages"))
    else:
    	return render_template('index.html')

@app.route('/Pages', methods=['GET', 'POST'])
def Pages():
    """ Saving Files and Images Analysis """
    if request.method == 'POST':
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
    os.system("bash run.sh")
    path = './static/out_img/*'
    file_list = glob.glob(path)
    return render_template('results.html', image_file=file_list)

if __name__ == '__main__':
    app.debug = True
    app.run(port = "5000", debug=True)