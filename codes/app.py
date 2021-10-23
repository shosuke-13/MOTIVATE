import os
from flask import Flask,render_template,redirect,request,url_for,session,jsonify,send_from_directory
from database import db
from views import User,Motivation,Portforio,Post,Feedback
from datetime import timedelta
import json
from datetime import date,datetime
import numpy as np
from werkzeug.utils import secure_filename
from sqlalchemy import desc


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivation.db'
app.config['SECRET_KEY'] = 'sjfsjifshnvsddvnv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

app.permanent_session_lifetime = timedelta(minutes=50)

with app.app_context():
    db.drop_all()
    db.create_all()

def allwed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    portfolios= db.session.query(Portforio).order_by(desc(Portforio.id)).all()
    posts= db.session.query(Post).order_by(desc(Post.id)).all()
    return render_template('home.html',portfolios=portfolios,posts=posts)

@app.route('/home_button', methods=['GET', 'POST'])
def home_button():
    if request.method == 'POST':
        return redirect(url_for('home'))
    portfolios= db.session.query(Portforio).order_by(desc(Portforio.id)).all()
    posts= db.session.query(Post).order_by(desc(Post.id)).all()
    return render_template('home.html',portfolios=portfolios,posts=posts)


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
      due = request.form.get("due")
      valence = request.form.get("valence")
      instrumentary = request.form.get("instrumentary")
      expectancy = request.form.get("expectancy")

      #モデルクラスのインスタンスを作成
      due = datetime.strptime(due,"%Y-%m-%d")
      motivation_data = Motivation(
          percentage=motivation,
          theme_name=theme, 
          due=due,
          valence=valence,
          instrumentary=instrumentary,
          expectancy=expectancy)

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
        list_data.append(motivation_data[0])
      
      motivation_data = json.dumps(list(list_data))
      
      theme_datas = db.session.query(Motivation.theme_name).all()
      list_data2 = []
      for theme_data in theme_datas:
        list_data2.append(theme_data[0])

      theme_data = json.dumps(list(list_data2))      

      date_datas = db.session.query(Motivation.due).all()
      list_data3 = []
      for date_data in date_datas:
          list_data3.append(date_data[0])

      # date, datetimeの変換関数
      def json_serial(obj):
          if isinstance(obj,date):
              return obj.isoformat()

      date_data = json.dumps(list(list_data3),default=json_serial)

      V_datas = db.session.query(Motivation.valence).all()
      list_data4 = []
      for V_data in V_datas:
          list_data4.append(V_data[0])
      V_data = list(list_data4)

      I_datas = db.session.query(Motivation.instrumentary).all()
      list_data5 = []
      for I_data in I_datas:
          list_data5.append(I_data[0])
      I_data = list(list_data5)

      E_datas = db.session.query(Motivation.expectancy).all()
      list_data6 = []
      for E_data in E_datas:
          list_data6.append(E_data[0])
      E_data = list(list_data6)

      array_add = list(map(lambda x,y:x*y,V_data,I_data))
      F_value = list(map(lambda x,y:x*y,array_add,E_data))
      F_value = (np.array(F_value)*100).tolist()
      F_val = json.dumps(F_value)

 
      return render_template('motivation.html',
       motivations = motivations,
       motivation_data = motivation_data, 
       theme_data = theme_data, 
       date_data=date_data, 
       F_value = F_val)

@app.route('/theme_delete/<int:id>')
def theme_delete(id):
    d_theme = db.session.query(Motivation).get(id)
    if d_theme is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response

    db.session.delete(d_theme)
    db.session.commit()

    return redirect(url_for('motivation_button'))



#ポートフォリオ
@app.route('/portfolio',methods=['GET', 'POST'])
def portfolio():
    portfolios= db.session.query(Portforio).order_by(desc(Portforio.id)).all()
    return render_template('portfolio.html',portfolios=portfolios)

@app.route("/portfolio_edit", methods = ["GET", "POST"])
def portfolio_edit():
    if request.method == "POST":
        portfolio_title = request.form.get("portfolio_title")
        portfolio_text = request.form.get("portfolio_text")
        file = request.files['portfolio_img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_url = './uploads/' + filename
        #theme = request.form.get("theme")
        #theme_id = db.session.query(Theme.id).filter(Theme.theme_name == theme,Theme.user_id == session["user_id"])
        db.session.add(Portforio(portforio_title=portfolio_title,portforio_text=portfolio_text,portforio_img=img_url,user_id=session["user_id"]))
        db.session.commit()
        return render_template("home.html")
    else:
        return render_template("portfolio.html")
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/portfolio_button', methods=['GET', 'POST'])
def portfolio_button():
    if request.method == 'POST':        
        return redirect(url_for('portfolio'))
    portfolios= db.session.query(Portforio).order_by(desc(Portforio.id)).all()
    return render_template('portfolio.html',portfolios=portfolios)
        

#投
@app.route('/post',methods=['GET', 'POST'])
def post():
    posts= db.session.query(Post).order_by(desc(Post.id)).all()
    return render_template('post.html',posts=posts)

@app.route("/post_edit", methods = ["GET", "POST"])
def post_edit():
    if request.method == "POST":
        post_title = request.form.get("post_title")
        post_text = request.form.get("post_text")
        file = request.files['post_img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_url = './uploads/' + filename
        #theme = request.form.get("theme")
        #theme_id = db.session.query(Theme.id).filter(Theme.theme_name == theme,Theme.user_id == session["user_id"])
        db.session.add(Post(post_title=post_title,post_text=post_text,post_img=img_url,user_id=session["user_id"]))
        db.session.commit()
        return render_template("home.html")
    else:
        return render_template("post.html")

@app.route('/post_button', methods=['GET', 'POST'])
def post_button():
    if request.method == 'POST':        
        return redirect(url_for('post'))
    posts= db.session.query(Post).order_by(desc(Post.id)).all()
    return render_template('post.html',posts=posts)



@app.route('/')
def logOut():
    return render_template('login.html')



@app.route('/logOut_button', methods=['GET', 'POST'])
def logOut_button():
    if request.method == 'POST':
        return redirect(url_for('logOut'))

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_button', methods=['GET', 'POST'])
def index_button():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/')
def index2():
    return render_template('index2.html')

@app.route('/index2_button', methods=['GET', 'POST'])
def index2_button():
    if request.method == 'POST':
        return redirect(url_for('index2'))

    return render_template('index2.html')



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

@app.route('/logout_button', methods=['GET', 'POST'])
def logout_button():
    if request.method == 'POST':
        return redirect(url_for('logout'))
    return render_template('login.html')





if __name__=="__main__":
  app.run(debug=True)
  


