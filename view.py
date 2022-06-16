
from flask import *
import sqlite3
from flask_mail import Mail,Message


app = Flask(__name__)
mail = Mail(app)

con = sqlite3.connect("database.db",check_same_thread=False)   
c = con.cursor() 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USERNAME'] = "flasksample123@gmail.com"
app.config['MAIL_PASSWORD'] = "kpsupjqwrkbcytxl"
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True 

mail = Mail(app)
# create a post table
c.execute('CREATE TABLE IF NOT EXISTS Posts (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,Description TEXT)')
# create a users table
c.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT ,username VARCHAR(50), password VARCHAR(80))')
# create a comments table
c.execute('CREATE TABLE IF NOT EXISTS Comments(id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,created_at DATETIME , post_id INTEGER)')

# create a subscribers table

c.execute('CREATE TABLE IF NOT EXISTS Subscribers(id INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR(50),password VARCHAR(80), Email VARCHAR(80))')


def get_connection():
    con = sqlite3.connect("database.db",check_same_thread=False)   
    c = con.cursor()
    return c


user=[]

# creating a login page
@app.route("/login",methods=["GET","POST"])

def login():
    try:
        if request.method == "POST":
            email=request.form.get('email')
            name = request.form.get("username")
            password = request.form.get("password")

            con = sqlite3.connect("database.db",check_same_thread=False)   
            c = con.cursor()
            
            c.execute('SELECT * FROM Users WHERE username=?',(name,)) 
            result = c.fetchone()


            if not result:
                
                con = sqlite3.connect("database.db",check_same_thread=False)   
                c = con.cursor()
                
                c.execute('INSERT into Users (username,password,Email) values (?,?,?)',(name,password,email) )
                con.commit()
                
            c.execute('SELECT * FROM Users WHERE username=?',(name,))
            user_id = c.fetchone()
            user.append(user_id)

            con.commit()

            return redirect(url_for('home'))
            
        
        else:
            return render_template("about.html")
    except:
        return "Something went wrong.Please try after sometime"

#creating a home page

@app.route("/home" , methods=["GET"])

def home():
    try:
        connect = get_connection()
    # to get all posts 
        connect.execute("select * from Posts")  
        all_posts = connect.fetchall()
    #to get all comments of posts
        connect.execute('select * from Comments')
        all_comments = connect.fetchall()

        return render_template("home.html",all_posts = all_posts,all_comments = all_comments)
    except:
        return "Something went wrong.Please try after sometime"


#to add the new posts
@app.route("/blog" , methods=["GET","POST"])

def blog_post():
    try:

        if len(user) == 0:
            return redirect(url_for('login'))
        else:
            connect = get_connection()
            id = user[0][0]
            connect.execute('SELECT username,password FROM Users WHERE id=?',(id,))
            result = connect.fetchone()
            if result[0] == "admin" and result[1] == "admin@123":

                if request.method == "POST":
                    title1 = request.form.get("ftitle")
                    description1 = request.form.get("fdescription")

                    con = sqlite3.connect("database.db",check_same_thread=False)   
                    c = con.cursor()
            
                    c.execute("INSERT into Posts (title,description) values (?,?)",(title1,description1))
                    c.execute('SELECT Email FROM Subscribers')
                    all_emails = c.fetchall()
                    
                    for email in all_emails:
                        each_id = email[0]
                        Msg = Message('New TravelBlog',sender = 'sample123@gmail.com', recipients = [f'{each_id}'])

                        Msg.body = 'New blog has been posted.Please do visit our blog site' 
                        mail.send(Msg)
                    con.commit()
                    return redirect(url_for("home"))
                else:
                    return render_template("blog.html")
            else:
                return "<h1>Restricted access <h1>"
    except:
        return "Something went wrong"



    
# to delete the comments
@app.route("/home/<int:id>")

def delete_blog(id):
    try:
        con = sqlite3.connect("database.db",check_same_thread=False)   
        c = con.cursor()
        c.execute("DELETE FROM Comments WHERE id=?",(id,))
        con.commit()
        return redirect(url_for('home'))
    except:
        return "Something went wrong"

@app.route("/delete/<int:id>")

def post_blog(id):
    try:
        con = sqlite3.connect("database.db",check_same_thread=False)   
        c = con.cursor()
        c.execute("DELETE FROM Posts WHERE id=?",(id,))
        con.commit()
        return redirect(url_for('home'))
    except:
        return "Something Went Wrong"   


# to post the comments on blog post
@app.route("/comment/<int:id>",methods=["POST"])

def comments(id):
    try:
        if len(user) == 0:
            return redirect(url_for('login'))
        else:

            con = sqlite3.connect("database.db",check_same_thread=False)   
            c = con.cursor() 
            user_id = user[0][0]
            c.execute('SELECT * FROM Users WHERE id=?',(user_id,))
            result = c.fetchone()
            name = result[1]

            text = request.form["comment"]
            
            c.execute('INSERT INTO Comments (text,post_id,user_name) VALUES (?,?,?)',(text,id,name))
            con.commit()
            
            return redirect(url_for('home'))
    except:
        return "Something went wrong.Please try again"

#sending a mail to the subscribers 

@app.route("/subscribe",methods = ["GET","POST"])

def subscribers():
    
    try:

        if request.method == "POST":
            name = request.form['username']
            email = request.form['Email']
            if not name  or not email:
                return render_template("subscribe.html",message = "Enter all the fields")

            con = sqlite3.connect("database.db",check_same_thread=False)   
            c = con.cursor() 
            
            c.execute('INSERT INTO Subscribers (username,Email) VALUES(?,?)',(name,email))

            Msg = Message('New TravelBlog',sender = 'sample123@gmail.com', recipients = [f'{email}'])

            Msg.body = f'Thank You {name}.You will get the notification when new post is uploaded'
            mail.send(Msg)
            con.commit()

            return redirect(url_for('home'))
        return render_template("subscribe.html",message = " ")
    except:
        return "Something went wrong.please try again."

    



if __name__ == "__main__" :
    app.run(debug = True)