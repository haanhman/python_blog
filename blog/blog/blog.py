from config import app, url_for, render_template, request
from mysql import db
import datetime
import time
@app.route('/blog/index')
def blog_index():
    db.execute("SELECT * FROM tbl_entries ORDER BY id DESC")
    result = db.fetchall()
    return render_template('blog/index.html', items=result)

@app.route('/blog/add', methods=['GET', 'POST'])
def blog_add():
    if request.method == 'POST':
        db.execute('INSERT INTO tbl_entries (title, description, content, create_date) VALUES (%s, %s, %s, %d)' % (request.form['title'], request.form['description'], request.form['content'], int(time.time())))
        db.commit()
        return "OK"
    return render_template('blog/form.html')

@app.route('/blog/detail/<int:post_id>')
def blog_detail(post_id):
    db.execute("SELECT * FROM tbl_entries WHERE id = " + str(post_id))
    entry = db.fetchone()
    if entry is None:
        return "Entry not found!"
    return render_template('blog/detail.html', item = entry)

@app.template_filter('datetime')
def formatDate(value):
    return datetime.datetime.fromtimestamp(value).strftime('%d/%m/%Y %H-%M-%S')