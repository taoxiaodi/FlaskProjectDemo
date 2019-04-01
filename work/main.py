from flask import Flask, render_template, request, redirect, make_response
from datetime import timedelta, datetime
from work.orm import managerorm as manager

app = Flask(__name__)

app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/')
def index():
    user = None
    user = request.cookies.get('id')
    if user:
        user = user.split('|')[1]
    return render_template('index.html', userinfo=user)


@app.route('/regist', methods=["POST", "GET"])
def regist():
    if request.method == 'GET':
        # print("get方法请求")
        # args = request.args
        # print(args)
        return render_template('regist.html')
    elif request.method == "POST":
        # print("post方法请求")
        username = request.form['username']
        password = request.form['password']

        manager.insert(username, password)

        return make_response(redirect('/shoplist'))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        # 第一种重定向
        # return render_template('shoplist.html', shoplist=["商品一", '商品二', "商品三"])
        username = request.form['username']
        password = request.form['password']
        try:
            result = manager.find(username, password)
            # 第二种 带接口的重定向 自动在URL发送请求
            res = make_response(redirect('/shoplist'))
            res.set_cookie('id', result, expires=datetime.now()+timedelta(days=7))
            return res
        except:
            return redirect('/login')


@app.route('/shoplist', methods=['POST', "GET"])
def shoplist():
    # 修改项目
    if request.method == "POST":
        project = request.form['project']
        edit_info = request.form['edit_info']
        manager.amend(int(request.args.get('sid')), project, edit_info)
        make_response(redirect('/shoplist'))
        return make_response(redirect('/shoplist'))

    # 删除项目
    if request.args.get('num'):
        manager.del_user(request.args.get('num'))

    # 项目的展示
    user = request.cookies.get('id')
    if user:
        info = manager.read_project(int(user[0]))
        user = user.split('|')[1]
        return render_template('shoplist.html', shoplist=info, userinfo=user)


@app.route('/details/<detail>')
def details(detail):
    print(detail)
    user = request.cookies.get('id')
    if user:
        user = user.split('|')
        # print(user[0])
        info = manager.read_pro(int(detail))
        return render_template('details.html', userinfo=user[1], userlist=info)


@app.route('/drop')
def drop():
    res = make_response(redirect('/'))
    res.delete_cookie('id')
    return res


@app.route('/edits', methods=['GET', 'POST'])
def edits():
    if request.method == "GET":
        return render_template('edit.html')
    elif request.method == "POST":
        pro_name = request.form['project']
        edit_info = request.form['edit_info']
        user = request.cookies.get('id')
        if user:
            user = user.split('|')
            manager.add_project(pro_name, edit_info, int(user[0]))
            return make_response(redirect('/shoplist'))


@app.route('/redact/<sid>', methods=['POST', "GET"])
def redact(sid):
    if request.method == "GET":
        return render_template('amend.html', sid=sid)
    elif request.method == "POST":
        return redirect("/shoplist")


if __name__ == "__main__":
    app.run(debug=True)
