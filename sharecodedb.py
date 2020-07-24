#!/usr/bin/env python3

from flask import Flask, request, render_template, \
    redirect

from model_sqlite import save_code_as_file, \
    read_code_as_file, \
    read_all_codes

app = Flask(__name__)


@app.route('/')
def index():
        return render_template('index.html', data=read_all_codes())


@app.route('/create')
def create():
    uid = save_code_as_file()
    print('ceci est le UID')
    print(uid)
    return redirect("{}edit/{}".format(request.host_url, uid))


@app.route('/edit/<string:uid>/')
def edit(uid):
    row = save_code_as_file(uid)

    if row is None:
        return render_template('error.html', uid=uid)

    d = dict(
        uid=uid,
        content=row[0],
        language=row[1],
        url="{}view/{}".format(request.host_url, uid)
    )

    return render_template('edit.html', **d)



@app.route('/publish', methods=['POST'])
def publish():
    content = request.form['code']
    uid = request.form['uid']
    language = request.form['language']
    save_code_as_file(uid, content, language)
    return redirect("{}{}/{}".format(request.host_url,
                                     request.form['submit'],
                                     uid))


@app.route('/view/<string:uid>/')
def view(uid):
    row = read_code_as_file(uid)

    if row is None:
        return render_template('error.html',uid=uid)

    d = dict(
        uid=uid,
        content=row[0],
        language=row[1],
        url="{}view/{}".format(request.host_url,uid)
    )

    return render_template('view.html', **d)


@app.route('/admin/')
def admin():
    pass


if __name__ == '__main__':
    app.run()