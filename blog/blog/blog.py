from flask import session, flash
from config import app, url_for, render_template, request, redirect
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
    print("UPLOAD FOLDER: %s" % app.config['UPLOAD_FOLDER'])
    return render_template('blog/index.html', items=result)

def uploadThumbnail():
    thumb = request.files['thumbnail']
    if thumb.filename == '':
        return None

    filename = secure_filename(thumb.filename)
    filename = string.ascii_lowercase + '_' + filename

    print('filename: %s' % filename)
    thumb.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/blog/add', methods=['GET', 'POST'])
def blog_add():
    if request.method == 'POST':
        print(request.files)
        thumbnail = uploadThumbnail()
        if thumbnail is None:
            flash('File not found!', 'error')
            return redirect(url_for('blog_add'))

        db.execute('INSERT INTO tbl_entries (title, description, content, thumbnail, create_date, edit_date) VALUES (%s, %s, %s, %s, %s, %s)', (
            request.form['title'].strip(),
            request.form['description'].strip(),
            request.form['content'].strip(),
            thumbnail,
            int(time.time()),
            0
        ))
        flash('Create new post success')
        return redirect(url_for('blog_index'))
    print('Create new post')
    return render_template('blog/form.html')

@app.route('/blog/detail/<int:post_id>')
def blog_detail(post_id):
    db.execute("SELECT * FROM tbl_entries WHERE id = " + str(post_id))
    entry = db.fetchone()
    if entry is None:
        flash('Post not found!', 'error')
        return redirect(url_for('blog_index'))
    return render_template('blog/detail.html', item = entry)


@app.route('/blog/edit/<int:post_id>')
def blog_edit(post_id):
    db.execute('SELECT * FROM tbl_entries WHERE id = %s', (
        post_id
    ))
    entry = db.fetchone();
    if entry is None:
        flash('Post not found!', 'error')
        return redirect(url_for('blog_index'))
    return render_template('blog/form.html', item = entry)


@app.route('/blog/update/<int:post_id>', methods=['POST'])
def blog_update(post_id):
    db.execute("SELECT * FROM tbl_entries WHERE id = " + str(post_id))
    entry = db.fetchone()
    if entry is None:
        flash('Post not found!', 'error')
        return redirect(url_for('blog_index'))

    thumbnail = entry['thumbnail']
    thumb = request.files['thumbnail']
    if thumb.filename != '':
        #remove old thumbnail
        oldThumbnail = app.config['UPLOAD_FOLDER'] + '/' + thumbnail
        if os.path.exists(oldThumbnail):
            os.remove(oldThumbnail)

        thumbnail = uploadThumbnail()
    db.execute('UPDATE tbl_entries SET thumbnail = %s, title = %s, description = %s, content = %s, edit_date = %s WHERE id = %s', (
            thumbnail,
            request.form['title'].strip(),
            request.form['description'].strip(),
            request.form['content'].strip(),
            int(time.time()),
            post_id
        ))
    flash('Update post success')
    return redirect(url_for('blog_detail', post_id=post_id))

@app.route('/blog/delete/<int:post_id>')
def blog_delete(post_id):
    db.execute('DELETE FROM tbl_entries WHERE id = %s', (post_id))
    return redirect(url_for('blog_index'))

@app.template_filter('datetime')
def formatDate(value):
    return datetime.datetime.fromtimestamp(value).strftime('%d/%m/%Y %H-%M-%S')