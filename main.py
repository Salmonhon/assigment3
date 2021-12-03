# from wtforms.fields import form
from configuration import app,db
from flask import Flask,render_template,redirect,request,session
from form import Signup,Login,NewsForm,SubscribeForm
from db import Author, News, subscribe



@app.before_first_request
def creat_all():
    db.create_all()



@app.route("/")
def index():
    message = 'please, login to see data info'
    return render_template("parent.html",message=message)


@app.route('/logout')
def logout():
    session.clear()  # remove author from session
    return redirect('/')


@app.route("/add_article", methods=['GET', 'POST'])
def add_article():
    if 'id' in session:
        author_login = Author.query.filter_by(id=session.get('id')).first()
        form = NewsForm()
        if form.validate_on_submit():
            news_create = News(title=form.title.data, intro=form.intro.data, text=form.text.data, author=author_login)
            print(news_create)  # just to show published news
            db.session.add(news_create)
            db.session.commit()
            return redirect('/post')
        return render_template('add-article.html', form=form)
    else:
        return redirect('/')


@app.route("/post", methods=['GET','POST'])
def post():
    form = SubscribeForm()
    author_login = Author.query.filter_by(id=session.get('id')).first()
    news = News.query.all()
    id = author_login.id
    # sub = Author.query.filter_by(author_login).all()
    print(author_login)
    if form.validate_on_submit():
        a = Author.query.filter_by(id=form.author_id.data).first()
        print(author_login)
        print(a)
        # a.subscribes.append(author_login)
        author_login.subscribes.append(a)
        print(author_login.subscribes)
        db.session.commit()
    followers_id = []
    for i in author_login.subscribes:
        followers_id.append(i.id)


    return render_template("post.html", news=news, form=form, id=id, followers_id=followers_id)





@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        author_login = Author.query.filter_by(email=form.email.data).first()
        if author_login.pswd == form.pswd.data:
            session['id'] = author_login.id

            return render_template('parent.html', message='Login done!')
    return render_template("login.html", form=form)


@app.route("/regist", methods=['GET', 'POST'])
def regist():
    form = Signup()
    if form.validate_on_submit():
        print(form)
        print(form.data)
        author_signup = Author(sname=form.sname.data, email=form.email.data, pswd=form.pswd.data)
        print(author_signup.sname)
        db.session.add(author_signup)  # adding Author-class instance into db
        db.session.commit()  # save db
        return render_template('parent.html', message='signup done!')
    return render_template("regist.html", form=form)


@app.route("/subscriptions")
def subscriptions():
    author_login = Author.query.filter_by(id=session.get('id')).first()
    followers_id = []
    for i in author_login.subscribes:
        followers_id.append(i.id)


    news = News.query.filter(News.author_id.in_(followers_id)).all()
    print(news)
    return render_template("my_subscriptions.html", news=news)


if __name__=="__main__":
    app.run(debug=True)