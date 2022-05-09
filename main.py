from flask import Flask, \
    render_template, \
    request, \
    redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

now = datetime.datetime.now()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

login = ""
password = ""
z = False


class Item(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String,
                      nullable=False)
    price = db.Column(db.Integer,
                      nullable=False)
    url = db.Column(db.Text,
                    nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    user_name = db.Column(db.String(20),
                          nullable=False)
    review = db.Column(db.Text,
                       nullable=False)
    date = db.Column(db.Text,
                     nullable=False)


db.create_all()
info = ""


@app.route("/",
           methods=["POST",
                    "GET"])
def index():
    global info
    if request.method == "POST":
        info = request.form["btn"][1:-1].split(",")
        return redirect("/buy/"
                            + info[-1])
    else:
        items = Item.query.all()
        return render_template("index.html",
                               data=items)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/done")
def done():
    return render_template("done.html")


@app.route("/licenses")
def licenses():
    return render_template("licenses.html")


@app.route("/reviews",
           methods=['POST',
                                'GET'])
def reviews():
    if request.method == "POST":
        name = request.form['username']

        if name == "":
            name = "incognito"
        comment = request.form['comment']
        date = now.strftime("%d-%m-%Y %H:%M")

        if comment != "":
            review = Review(user_name=name,
                            review=comment,
                            date=date)

            try:
                db.session.add(review)
                db.session.commit()
                return redirect("/reviews")
            except:
                return "Ошибка," \
                       " Сорян"
    else:
        review = Review.query.all()

        return render_template("reviews.html",
                               data=review)


@app.route("/admin",
           methods=['POST',
                    'GET'])
def admin():
    global login, password
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        if login == "rofl"\
                and password == '111':
            return redirect("/admin_add")
        else:
            return render_template("admin.html")
    else:
        return render_template("admin.html")


@app.route("/admin_add",
           methods=["POST",
                    "GET"])
def admin_add():
    global login,\
        password
    if login != "rofl"\
            or password != '111':
        return redirect("/admin")
    else:
        if request.method == 'POST':
            name = request.form["name"]
            price = request.form["price"]
            url = request.form["url"]
            item = Item(title=name,
                        price=price,
                        url=url)
            try:
                db.session.add(item)
                db.session.commit()
                return redirect("/")
            except:
                return "Ошибка, Сорян"
        else:
            return render_template("admin_add.html")


@app.route('/buy/<id>',
           methods=["POST",
                    "GET"])
def greeting(id):
    if request.method == "POST":
        return redirect("/done")
    else:
        global info
        return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel = "stylesheet" href = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"><meta charset="UTF-8">
    </head>
    <body>
    
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
      <symbol id="check" viewBox="0 0 16 16">
        <title>Check</title>
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"></path>
      </symbol>
    </svg>
    
    <div class="container py-3">
      <header>
        <div class="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
          <a href="/" class="d-flex align-items-center text-dark text-decoration-none">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="32" class="me-2" viewBox="0 0 118 94" role="img"><title>Bootstrap</title><path fill-rule="evenodd" clip-rule="evenodd" d="M24.509 0c-6.733 0-11.715 5.893-11.492 12.284.214 6.14-.064 14.092-2.066 20.577C8.943 39.365 5.547 43.485 0 44.014v5.972c5.547.529 8.943 4.649 10.951 11.153 2.002 6.485 2.28 14.437 2.066 20.577C12.794 88.106 17.776 94 24.51 94H93.5c6.733 0 11.714-5.893 11.491-12.284-.214-6.14.064-14.092 2.066-20.577 2.009-6.504 5.396-10.624 10.943-11.153v-5.972c-5.547-.529-8.934-4.649-10.943-11.153-2.002-6.484-2.28-14.437-2.066-20.577C105.214 5.894 100.233 0 93.5 0H24.508zM80 57.863C80 66.663 73.436 72 62.543 72H44a2 2 0 01-2-2V24a2 2 0 012-2h18.437c9.083 0 15.044 4.92 15.044 12.474 0 5.302-4.01 10.049-9.119 10.88v.277C75.317 46.394 80 51.21 80 57.863zM60.521 28.34H49.948v14.934h8.905c6.884 0 10.68-2.772 10.68-7.727 0-4.643-3.264-7.207-9.012-7.207zM49.948 49.2v16.458H60.91c7.167 0 10.964-2.876 10.964-8.281 0-5.406-3.903-8.178-11.425-8.178H49.948z" fill="currentColor"></path></svg>
            <span class="fs-4">ROFL-SHOP</span>
          </a>
    
          <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
            <a class="me-3 py-2 text-dark text-decoration-none" href="/reviews">Отзывы
            </a>
            <a class="me-3 py-2 text-dark text-decoration-none" href="/admin">Режим админа
            </a>
            <a class="me-3 py-2 text-dark text-decoration-none" href="/licenses">Лицензии
            </a>
            <a class="py-2 text-dark text-decoration-none" href="/about">О нас
            </a>
          </nav>
        </div>
    
        <div class="pricing-header p-3 pb-md-4 mx-auto text-center">
        </div>
      </header>
    
      <main>
      
      
      <div class="card-body">
        <form method="post">
                    <h1 class="card-title pricing-card-title">Название рофлянчика: {info[0][1:-1]}<small class="text-muted fw-light"></small></h1>
                    <h1 class="card-title pricing-card-title">Цена рофлянчика:{info[1]}  ₽<small class="text-muted fw-light"></small></h1>
                    
                    <p>
                        <img src={info[2][2:-1]}
                             alt="упс"></p>
                </div>
    <h1 class="h3 mb-3 font-weight-normal">Для оплаты необходимо заполнить данные вашей банковской карты,</h1>
    <h1 class="h3 mb-3 font-weight-normal">через которую и будет совершаться платеж по картинке,</h1>
    <h1 class="h3 mb-3 font-weight-normal">Которая сделает вас богатым человеком!</h1>
        <form method="post">
        <label for="login" class="sr-only">Номер карты</label>
        <input type="text" class="form-control" name="name" id="name" placeholder="5432 6372 7823 7388" required="">
        <label for="inputPassword" class="sr-only">Срок хранения карты</label>
        <input type="number" name="price" id="price" class="form-control" placeholder="08/24" required="">
        <label for="inputPassword" class="sr-only">СVV-код</label>
        <input type="text" name="url" id="url" class="form-control" placeholder="334" required="">
            <h1> </h1>
            <h1> </h1>
        <button class="btn btn-lg btn-primary btn-block" type="submit" >Оплатить</button>
        <p class="mt-5 mb-3 text-muted">© 2017-2018</p>
    </form>
    
                             
    
      <footer class="pt-4 my-md-5 pt-md-5 border-top">
        <div class="row">
          <div class="col-12 col-md">
            <img class="mb-2" src="/docs/5.1/assets/brand/bootstrap-logo.svg" alt="" width="24" height="19">
            <small class="d-block mb-3 text-muted">© 2017–2021</small>
          </div>
          <div class="col-6 col-md">
            <h5>Features</h5>
            <ul class="list-unstyled text-small">
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Cool stuff</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Random feature</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Team feature</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Stuff for developers</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Another one</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Last time</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>Resources</h5>
            <ul class="list-unstyled text-small">
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Resource</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Resource name</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Another resource</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Final resource</a></li>
            </ul>
          </div>
          <div class="col-6 col-md">
            <h5>About</h5>
            <ul class="list-unstyled text-small">
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Team</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Locations</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Privacy</a></li>
              <li class="mb-1"><a class="link-secondary text-decoration-none" href="#">Terms</a></li>
            </ul>
          </div>
        </div>
      </footer>
      </div>
        <div class="mallbery-caa" style="z-index: 2147483647 !important; text-transform: none !important; position: fixed;">
    
    
    </body>
    </html>"""


if __name__ == "__main__":
    app.run(debug=True)
