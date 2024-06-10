import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
from dataProcessing import *
from Threads import *
from flask import send_file
import time
import os
script = ''
from flask import make_response
from flask import request

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt','docx','png','jpg','pdf','jpeg','zip','rtf','webp'])

# api = API(app)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "null"

def resultE():
    path = "./Segments"
    dir_list = os.listdir(path)
    print(dir_list)
    return render_template('Result.html',dir_list = dir_list)

def resultD():
    return render_template('resultD.html')

@app.route('/encrypt/')
def EncryptInput():
  Segment()
  gatherInfo()
  HybridCrypt()
  return resultE()

@app.route('/decrypt/')
def DecryptMessage():
  st=time.time()
  HybridDeCrypt()
  et=time.time()
  print(et-st)
  trim()
  st=time.time()
  Merge()
  et=time.time()
  print(et-st)
  return resultD()

def start():
  content = open('./Original.txt','rb')
  content.seek(0)
  first_char = content.read(1) 
  if not first_char:
    return render_template('Empty.html')
  else:
    return render_template('Option.html')

@app.route('/')
def index():
  return render_template('index.html')

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/return-files-key/')
def return_files_key():
    try:
        return send_file(
            './Original.txt',
            as_attachment=True,
            download_name='original.txt'
        )
    except Exception as e:
        return str(e)



@app.route('/return-files-data/')
def return_files_data():
    try:
        extension = request.cookies.get('ext')  # Retrieve the value of the 'ext' cookie
        if extension is None:  # Handle the case when the 'ext' cookie is not found
            raise Exception('Cookie not found')

        return send_file(
            './Output.txt',
            as_attachment=True,
            download_name=f'output{extension}'  # Use the obtained extension value in the download name
        )
    except Exception as e:
        return str(e)





@app.route('/data/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return render_template('Nofile.html')
    file = request.files['file']
    if file.filename == '':
      return render_template('Nofile.html')
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      extension = os.path.splitext(filename)[1]
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Original.txt'))
      file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename ))

      # Setting the cookie
      resp = make_response(start())
      resp.set_cookie('ext', extension)  # Setting the 'ext' cookie with the file extension
      return resp
       
    return render_template('Invalid.html')

    
if __name__ == '__main__':
  app.run(debug=True)
