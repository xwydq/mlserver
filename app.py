from flask import Flask
import pandas as pd
import os
from flask import request, jsonify, send_file, render_template_string, render_template
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
import sklearn.linear_model
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from mdatparse import ParseMdlDat
from pypinyin import lazy_pinyin


UPLOAD_FOLDER = 'assets/files'
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
app.secret_key = "super secret key"

# curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@E:/data/test.csv" http://127.0.0.1:5000/lm

@app.route('/lm', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # post json parse
        res = request.get_json()
        if res:
            mdat = pd.DataFrame(res)
        else:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            # post CSV file
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                name = file.filename.split('.')[0]
                ext = file.filename.split('.')[1]
                filename = '_'.join(lazy_pinyin(name)) + '.' + ext

                filename = secure_filename(filename)
                file_pth = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(filename)
                file.save(file_pth)
                with open(file_pth) as f:
                    file_encoding = f.encoding

                mdat = pd.read_csv(file_pth, encoding=file_encoding)
                print(mdat)

        if mdat.shape[0] > 5:
            ## 提取数据的变量
            yvar = ParseMdlDat.getyVar(mdat)
            xvars = ParseMdlDat.getxVars(mdat)

            if yvar is not None and xvars is not None:
                xvar = xvars['xdat']
                feature_nms = xvars['features']
                # print(yvar)
                model = sklearn.linear_model.LinearRegression()
                # Train the model
                model.fit(xvar, yvar)
                ypred = model.predict(xvar)

                mae = mean_absolute_error(yvar, ypred)
                mse = mean_squared_error(yvar, ypred)
                r2 = r2_score(yvar, ypred)

                metrics = {
                    "mae":mae,
                    "mse":mse,
                    "r2":r2
                }

                coef_dict = {}
                for coef, feat in zip(model.coef_.tolist()[0], feature_nms):
                    coef_dict[feat] = coef
                    # print(coef, feat)

                    coef_dict["intercept"] = model.intercept_.tolist()[0]

                coef_dict["metrics"] = metrics
                print("                print(coef_dict)")
                print(coef_dict)

                return jsonify(coef_dict)
            else:
                flash('数据格式不满足要求！')
                return redirect(request.url)
                # return redirect(url_for('upload_file', filename=filename))
            # return jsonify(mdat.to_dict())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/', methods=['GET'])
def home():
    return "<h1>指令集机器学习服务接口</h1>" \
           "<p>提供常用机器学习相关算法的API接口</p>"


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

if __name__ == '__main__':
    app.run()
