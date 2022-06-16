import sqlite3
from flask import *

app=Flask(__name__)

#creating a admin database
@app.route("/create")
def create():
    connection = sqlite3.connect("database.db")
    conn = connection.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS admin(id INTEGER PRIMARY KEY,userid VARCHAR(40),password VARCHAR(40),userlogin VARCHAR(40))")
    return "Successfully Created"

#inserting a 
@app.route("/insert")
def insert():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute('INSERT INTO admin VALUES(1,"geetha","geetha@123","failure")')
    connection.commit()
    return "<h1>Data Entered successfully<h1>"

#creating a post database
@app.route("/posttable")
def createpost():
    connection = sqlite3.connect("post.db")
    conn = connection.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS post(title VARCHAR(400),description VARCHAR(400))")
    return "<h1>Successfull<h1>"

#Home Page
@app.route("/")
def home():
    connection = sqlite3.connect("post.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM post")
    mydata = conn.fetchall()
    return render_template("homepage.html",mydata = mydata)

#Login Page
@app.route("/login",methods=["GET","POST"])
def login():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM admin")
    mydata = conn.fetchone()
    data = mydata[3]
    if data == "failure":
        if request.method == "POST":
            userid = request.form['userid']
            password = request.form['password']
            if userid == "geetha" and password == "geetha@123":
                conn.execute("UPDATE admin SET userlogin='success'")
                connection.commit()
                return redirect("/post")
            else:
                render_template("login.html")
    else:
        return redirect("/post")
    return render_template("login.html")

# Posting a blog
@app.route("/post",methods=["GET","POST"])
def post():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM admin")
    mydata = conn.fetchone()
    data = mydata[3]
    if data == "failure":
        return redirect("/login")
    else:
        if request.method == "POST":
            title = request.form["title"]
            description = request.form["description"]
            connection = sqlite3.connect("post.db")
            conn = connection.cursor()
            conn.execute(f'INSERT INTO post VALUES("{title}","{description}")')
            connection.commit()
            conn.execute("SELECT * FROM post")
            mydata = conn.fetchall()
            return render_template("post.html")
        connection = sqlite3.connect("post.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM post")
        postdata = conn.fetchall()
        return render_template("post.html",mydata = postdata)
    return redirect("/login")

@app.route("/delete",methods=["GET","DELETE"])
def delete():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM admin")
    mydata = conn.fetchone()
    data = mydata[3]
    if data == "failure":
        return redirect("/login")
    else:
        name = request.args.get("title")
        connection = sqlite3.connect("post.db")
        conn = connection.cursor()
        conn.execute(f'DELETE FROM post WHERE title="{name}"')
        connection.commit()
        return render_template("delete.html")


@app.route("/put",methods=["GET","PUT"])
def put():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM admin")
    mydata = conn.fetchone()
    data = mydata[3]
    if data == "failure":
        return redirect("/login")
    else:
        name = request.args.get("title")
        description = request.args.get("description")
        connection = sqlite3.connect("post.db")
        conn = connection.cursor()
        conn.execute(f'UPDATE post SET description="{description}" WHERE title="{name}"')
        connection.commit()
        return render_template("put.html")
    return render_template("put.html")

@app.route("/logout")
def logout():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("UPDATE admin SET userlogin='failure'")
    connection.commit()
    return redirect("/login")

# creating the subscription table
@app.route("/createsubscriber")
def createsubscriber():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS subscribers(name VARCHAR(40),email VARCHAR(40),phonenumber INTEGER)")
    return "<h1>Successfull<h1>"

@app.route("/subscribe",methods=["GET","POST"])
def subscribe():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phonenumber = request.form['phonenumber']

        if not name or not email or not phonenumber:
            return render_template("subscribe.html",message="Enter all fields")
        
        message = "You are Subscribed"
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute(f'INSERT INTO subscribers VALUES("{name}","{email}",{phonenumber})')
        connection.commit()
        return render_template("subscribe.html")
    return render_template("subscribe.html")

# creating the comment table
@app.route("/createcomment")
def createcomment():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS comment(name VARCHAR(40),comment VARCHAR(400))")
    return "<h1>Successfull<h1>"

@app.route("/comment",methods=["GET","POST"])
def comment():
    if request.method == "POST":
        name = request.form['name']
        comment = request.form['comment']

        if not name or not comment:
            return render_template("comment.html",message="Enter all fields")
        
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute(f'INSERT INTO comment VALUES("{name}","{comment}")')
        connection.commit()
        return render_template("comment.html")
    return render_template("comment.html")

@app.route("/readcomment")
def readcomment():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM comment")
    mydata = conn.fetchall()
    return render_template("readcomment.html",mydata = mydata)

# getting the subscription data
@app.route("/subscriberslist")
def subscriberslist():
    connection = sqlite3.connect("admin.db")
    conn = connection.cursor()
    conn.execute("SELECT * FROM admin")
    mydata = conn.fetchone()
    data = mydata[3]
    if data == "failure":
        return redirect("/login")
    else:
        connection = sqlite3.connect("admin.db")
        conn = connection.cursor()
        conn.execute("SELECT * FROM subscribers")
        mydata = conn.fetchall()
        return render_template("subscriberslist.html",mydata = mydata)
    return render_template("subscriberslist.html",mydata = mydata)

if __name__=="__main__":
    app.run(debug=True)