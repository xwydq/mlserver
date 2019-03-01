from flask import Flask
import pandas as pd
import os
from flask import request, jsonify, send_file, render_template_string, render_template
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'assets/files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
app.secret_key = "super secret key"

# curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@E:/data/test.csv" http://127.0.0.1:5000/upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            csvdat = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(csvdat.to_dict())
            # return redirect(url_for('upload_file',
            #                         filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': '回归',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': '分类',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': '聚类',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>指令集机器学习服务接口</h1>" \
           "<p>提供常用机器学习相关算法的API接口</p>"


## 返回json
@app.route('/ml')
def mlpara():
    return jsonify(df.to_dict())


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

## 异常页面
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>访问的资源不存在.</p>", 404

## 返回图片
@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'assets/images/bubble.png'
    else:
       filename = 'assets/images/cloud.png'
    return send_file(filename, mimetype='image/png')


## 返回模板
@app.route('/template')
def get_htmlTmplt():
    rx = request.args['mltype']
    print(rx)
    return render_template_string('<h1 style="color:red">hello {{ what }}</h1>', what=rx)

############ post
## post json
@app.route('/pJson',methods=['POST'])
def login():
    res = request.get_json()
    print(res)
    json_data ={ 'success':'true' }
    return jsonify(json_data)

# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')
#
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       data= genfromtxt(os.path.abspath(f.filename) , delimiter=',')
#       graph = pygal.Line()
#
#       if data.shape[1]==0:
#           graph.add('Data', data)
#       else:
#           graph.add('Data', data[1,:])
#
#       graph_data = graph.render_data_uri()
#       return render_template("upload.html", graph_data = graph_data)

if __name__ == '__main__':
    app.run()
