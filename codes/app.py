from flask import Flask,render_template,redirect,request,url_for,session
from database import db
from views import User,Motivation,Portforio,Post,Feedback
from datetime import timedelta
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivation.db'
app.config['SECRET_KEY'] = 'sjfsjifshnvsddvnv'
db.init_app(app)

app.permanent_session_lifetime = timedelta(minutes=50)

with app.app_context():
    db.drop_all()
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

@app.route('/motivation', methods=['GET', 'POST'])
def motivation_button():
    if request.method == 'POST':
      #フォームの作成
      motivation = request.form.get('motivation')
      theme = request.form.get('theme')

      #モデルクラスのインスタンスを作成
      motivation_data = Motivation(percentage = motivation,theme_name=theme)
      #theme_data = Theme(theme_name = theme)
      
      #データベースに保存する
      db.session.add(motivation_data)
      db.session.commit()
      db.session.close()

      return redirect(url_for('motivation'))

    else:
      #データベースからデータを取り出す
      motivations = db.session.query(Motivation).all()
    
      motivation_datas = db.session.query(Motivation.percentage).all()
      list_data = []
      for motivation_data in motivation_datas:
        print(motivation_data)
        list_data.append(motivation_data[0])
      
      motivation_data = json.dumps(list(list_data))
      
      theme_dates = db.session.query(Motivation.theme_name).all()
      list_data2 = []
      for theme_data in theme_dates:
        list_data2.append(theme_data[0])

      theme_data = json.dumps(list(list_data2))      
      
      return render_template('motivation.html', motivations = motivations, motivation_data = motivation_data, theme_data = theme_data)


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
    
    return render_template('signup.html')

@app.route('/')
def already_signup():
    return render_template('login.html')

@app.route('/already_signup_button', methods=['GET', 'POST'])
def already_signup_button():
    if request.method == 'POST':
        return redirect(url_for('already_signup'))

    return render_template('login.html')


    

@app.route("/register", methods = ["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    db.session.add(User(username=username,e_mail=email,password=password))
    db.session.commit()
    return render_template("home.html")
  else:
    return render_template("login.html")

@app.route("/login",methods = ["GET","POST"])
def login():

  session.clear()

  if request.method == "POST":
    e_mail = request.form.get("email")
    password = request.form.get("password")
    user = db.session.query(User).filter(User.e_mail == e_mail).all()[0]
    user_id = user.id
    user_password = user.password

    session.permanent = True
    session["user_id"] = user_id
    return render_template("home.html")

@app.route("/logout",methods = ["GET","POST"])
def logout():
  session.pop("user_id", None)
  return redirect("/")




if __name__=="__main__":
  app.run(debug=True)
  


