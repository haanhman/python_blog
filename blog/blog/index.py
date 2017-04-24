from config import app, render_template, url_for
@app.route('/')
def index_index():
    return render_template('index/index.html')

@app.route('/version')
def index_version():
    return render_template('index/version.html', version = "1.0.0")