from flask import Flask,request,flash,redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from  wtforms.validators import DataRequired

# 创建表单类
class Append(FlaskForm):

    aut = StringField(label="作者:",validators=[DataRequired()])
    book = StringField(label="书籍:",validators=[DataRequired()])
    submit = SubmitField("添加")

app = Flask(__name__)

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.194.135:3306/test3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "todobest"

app.config.from_object(Config)

db = SQLAlchemy(app)

class Aut(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)

    books = db.relationship("Book",backref = "aut")

    def __repr__(self):

        return "Aut:%s %s"%(self.name,self.id)

class Book(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    forei_aut_id = db.Column(db.Integer,db.ForeignKey(Aut.id))

    def __repr__(self):

        return "Book:%s %s"%(self.name,self.id)


@app.route('/',methods=["POST","GET"])
def author_book():

    form = Append()

    if form.validate_on_submit():
        aut_name = request.form.get("aut","")
        book_name = request.form.get("book","")
        author = Aut.query.filter(Aut.name == aut_name).first()
        if not author:
            author = Aut(name=aut_name)
            db.session.add(author)
            db.session.commit()

            book = Book(name=book_name,forei_aut_id = author.id)
            db.session.add(book)
            db.session.commit()

        else:
            book_name = Book.query.filter(Book.name == book_name).first()

            if book_name:
                flash("书籍已经存在")
            else:
                book = Book(name=book_name,forei_aut_id = author.id)
                db.session.add(book)
                db.session.commit()


    authors = Aut.query.all()
    return render_template("aut_book.html",authors = authors,form = form)


@app.route('/removeaut/<aut_id>')
def removeaut(aut_id):
    try:
        aut = Aut.query.get(aut_id)
    except Exception as e:
        flash(e)


    if not aut:
        flash("作者不存在")

    else:
        books = aut.books
        for book in books:
            db.session.delete(book)

        db.session.delete(aut)
        db.session.commit()

    return  redirect(url_for("author_book"))

@app.route('/removebook/<bk_id>')
def removebook(bk_id):
    try:
        book = Book.query.get(bk_id)
    except Exception as e:
        flash(e)

    if not book:
        flash("书籍不存在")
    else:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            flash(e)
            db.session.rollback()

    return redirect(url_for('author_book'))

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Aut(name='老王')
    au2 = Aut(name='老尹')
    au3 = Aut(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', forei_aut_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', forei_aut_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', forei_aut_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', forei_aut_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', forei_aut_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()
    app.run(debug=True)








































































