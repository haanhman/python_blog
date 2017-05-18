from config import app, url_for, render_template, request, redirect, flash
from mysql import db
from werkzeug.utils import secure_filename
import datetime
import time
import os, errno
import string
@app.route('/blog/index')
def blog_index():
    db.execute("SELECT * FROM tbl_entries ORDER BY id DESC")
    result = db.fetchall()
    return render_template('blog/index.html', items=result)

def uploadThumbnail(post_id = 0):
    thumb = request.files['thumbnail']
    if thumb.filename == '':
        if post_id == 0:
            return redirect(url_for('blog_add'))
        else:
            return redirect(url_for('blog_update', post_id=post_id))

    filename = secure_filename(thumb.filename)
    filename = string.ascii_lowercase + '_' + filename

    print('filename: %s' % filename)
    thumb.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/blog/add', methods=['GET', 'POST'])
def blog_add():
    if request.method == 'POST':
        print(request.files)
        thumbnail = uploadThumbnail(0)
        db.execute('INSERT INTO tbl_entries (title, description, content, thumbnail, create_date, edit_date) VALUES (%s, %s, %s, %s, %s, %s)', (
            request.form['title'].strip(),
            request.form['description'].strip(),
            request.form['content'].strip(),
            thumbnail,
            int(time.time()),
            0
        ))
        return redirect(url_for('blog_index'))
    print('Create new post')
    return render_template('blog/form.html')

@app.route('/blog/detail/<int:post_id>')
def blog_detail(post_id):
    db.execute("SELECT * FROM tbl_entries WHERE id = " + str(post_id))
    entry = db.fetchone()
    if entry is None:
        return "Entry not found!"
    return render_template('blog/detail.html', item = entry)


@app.route('/blog/edit/<int:post_id>')
def blog_edit(post_id):
    db.execute('SELECT * FROM tbl_entries WHERE id = %s', (
        post_id
    ))
    entry = db.fetchone();
    if entry is None:
        return "Entry not found!"
    return render_template('blog/form.html', item = entry)


@app.route('/blog/update/<int:post_id>', methods=['POST'])
def blog_update(post_id):
    db.execute("SELECT * FROM tbl_entries WHERE id = " + str(post_id))
    entry = db.fetchone()
    if entry is None:
        return "Entry not found!"

    thumbnail = entry['thumbnail']
    thumb = request.files['thumbnail']
    if thumb.filename != '':
        #remove old thumbnail
        oldThumbnail = app.config['UPLOAD_FOLDER'] + '/' + thumbnail
        if os.path.exists(oldThumbnail):
            os.remove(oldThumbnail)
            
        thumbnail = uploadThumbnail(0)
    db.execute('UPDATE tbl_entries SET thumbnail = %s, title = %s, description = %s, content = %s, edit_date = %s WHERE id = %s', (
            thumbnail,
            request.form['title'].strip(),
            request.form['description'].strip(),
            request.form['content'].strip(),
            int(time.time()),
            post_id
        ))
    return redirect(url_for('blog_detail', post_id=post_id))

@app.route('/blog/delete/<int:post_id>')
def blog_delete(post_id):
    db.execute('DELETE FROM tbl_entries WHERE id = %s', (post_id))
    return redirect(url_for('blog_index'))

@app.template_filter('datetime')
def formatDate(value):
    return datetime.datetime.fromtimestamp(value).strftime('%d/%m/%Y %H-%M-%S')