from flask import Flask,render_template,redirect,request,url_for
from database import db
from views import User,Theme,Motivation,Portforio,Post,Feedback

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivation.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home_button', methods=['GET', 'POST'])
def home_button():
    if request.method == 'POST':
        return redirect(url_for('home'))

    return render_template('home.html')

@app.route('/')
def account():
    return render_template('account.html')

@app.route('/account_button', methods=['GET', 'POST'])
def account_button():
    if request.method == 'POST':
        return redirect(url_for('account'))

    return render_template('account.html')


@app.route('/')
def motivation():
    return render_template('motivation.html')

@app.route('/motivation_button', methods=['GET', 'POST'])
def motivation_button():
    if request.method == 'POST':
        return redirect(url_for('motivation'))

    return render_template('motivation.html')


@app.route('/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/portfolio_button', methods=['GET', 'POST'])
def portfolio_button():
    if request.method == 'POST':
        return redirect(url_for('portfolio'))

    return render_template('portfolio.html')


@app.route('/')
def post():
    return render_template('post.html')

@app.route('/post_button', methods=['GET', 'POST'])
def post_button():
    if request.method == 'POST':
        return redirect(url_for('post'))

    return render_template('post.html')


@app.route('/')
def logout():
    return render_template('login.html')

@app.route('/logout_button', methods=['GET', 'POST'])
def logout_button():
    if request.method == 'POST':
        return redirect(url_for('logout'))

    return render_template('login.html')


@app.route('/')
def not_signup():
    return render_template('signup.html')

@app.route('/not_signup_button', methods=['GET', 'POST'])
def not_signup_button():
    if request.method == 'POST':
        return redirect(url_for('not_signup'))

    return render_template('signup.html')


@app.route('/')
def already_signup():
    return render_template('login.html')

@app.route('/already_signup_button', methods=['GET', 'POST'])
def already_signup_button():
    if request.method == 'POST':
        return redirect(url_for('already_signup'))

    return render_template('login.html')


if __name__=="__main__":
  app.run(debug=True)


