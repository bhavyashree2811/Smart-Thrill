from flask import *
import os
from werkzeug.utils import secure_filename

import sqlite3

app=Flask(__name__)

app.secret_key = "super secret key"

upload_img = 'static/uploads'
allowed_extension = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['upload_img'] = upload_img

@app.route("/")
def indexPage():
    return render_template("index.html")

@app.route("/tohome")
def backHome():
    return render_template("home.html")

@app.route("/register")
def registerUser():
    return render_template("createUser.html")

@app.route("/forgot")
def forgotpassw():
    return render_template("newPassw.html")

@app.route("/toUser")
def intoUser():
    return render_template("updateUser.html")

@app.route("/delUser")
def deleteUser():
    return render_template("deleteUser.html")

@app.route("/toPost")
def intoPost():
    return render_template("updatePost.html")

@app.route("/postNew")
def newPost():
    return render_template("createPost.html")

@app.route("/delPost")
def delPost():
    return render_template("deletePost.html")

@app.route("/toAdmin")
def homeAdmin():
    return render_template("adminHome.html")

@app.route("/report")
def repproblem():
    return render_template("contact.html")

@app.route("/chatUser")
def reChat():
    return redirect("http://127.0.0.1:8000/")

@app.route("/check",methods=['POST'])
def checkPass():

    name = request.form["user"]
    password = request.form["pname"]

    if name == "admin" and password == "12345":
        return render_template("adminHome.html")

    else:
        con = sqlite3.connect("application.db")
        cur = con.cursor()
        session['user'] = name
        obj=cur.execute("SELECT USERNAME,PASSWORD FROM USER WHERE USERNAME=?",(name,))

        for i in obj:
            if i[0] == name and i[1] == password:
                return render_template("home.html")
            else:
                return "Login Failed"


@app.route("/saveRecord", methods= ["POST"])
def saveDetails():
    msg= ""

    if request.method== "POST":
        try:

            name=request.form["uname"]
            email = request.form["email"]
            firstName=request.form["firstname"]
            secondName = request.form["secondname"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            city = request.form["city"]
            gender = request.form["gender"]
            age = request.form["Age"]
            passw = request.form["pname"]

            with sqlite3.connect("application.db")as con:
                cur=con.cursor()
                cur.execute("INSERT INTO USER(USERNAME,USERMAIL,FIRSTNAME,SECONDNAME,CONTACT,DOB,CITY,GENDER,AGE,PASSWORD)VALUES(?,?,?,?,?,?,?,?,?,?)",(name,email,firstName,secondName,contact,dob,city,gender,age,passw))
                con.commit()
                msg="User Successfully Registered"
        except:
            con.rollback()
            msg="We cannot add the user to the list"
        finally:
            return render_template("index.html")

@app.route("/change",methods=["POST"])
def changePassword():
    email = request.form["email"]
    passw = request.form["pname"]


    with sqlite3.connect("application.db") as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE USER SET PASSWORD=? WHERE USERMAIL= ?",(passw,email))
                msg = "record successfullly updated"
            except:
                msg = "can't be updated"
            finally:
                return render_template("index.html")

@app.route("/remove", methods=["POST"])
def removeUser():
    user=request.form["user"]
    with sqlite3.connect("application.db") as con:
        try:
            cur=con.cursor()
            cur.execute("DELETE FROM USER WHERE USERNAME=?",(user,) )
            con.commit()
            msg="record successfullly deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("adminHome.html")


@app.route("/update",methods=["POST"])
def changePost():
    postid=request.form["postid"]
    message = request.form["message"]



    with sqlite3.connect("application.db") as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE POST SET MESSAGE=? WHERE POSTID= ?",(message,postid))
                msg = "record successfullly updated"
            except:
                msg = "can't be updated"
            finally:
                return render_template("adminHome.html")

@app.route("/postremove", methods=["POST"])
def removePost():
    id=request.form["id"]
    with sqlite3.connect("application.db") as con:
        try:
            cur=con.cursor()
            cur.execute("DELETE FROM POST WHERE POSTID=?",(id,) )
            con.commit()
            msg="record successfullly deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("adminHome.html")
@app.route("/savePost", methods= ["POST"])
def savePostDetails():
    msg= ""

    if request.method== "POST":
        try:

            # name=request.form["uname"]
            message=request.form["message"]
            image = request.files['image']
            if image and files_allowed(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['upload_img'], filename))
            imagename = filename
            with sqlite3.connect("application.db")as con:
                cur=con.cursor()
                cur.execute("INSERT INTO POST(NAME,MESSAGE,IMAGE)VALUES(?,?,?)",(session['user'],message,imagename))
                con.commit()
                msg="User Successfully Registered"
        except:
            con.rollback()
            msg="We cannot add the user to the list"
        finally:
            return render_template("home.html", msg=msg)

@app.route("/view")
def viewYourPost():
    with sqlite3.connect('application.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM POST")
        itemData = cur.fetchall()

    itemData = parse(itemData)

    return render_template("viewPost.html", itemData=itemData)



@app.route("/saveProblem", methods= ["POST"])
def saveProbDetails():
    msg= ""

    if request.method== "POST":
        try:

            # name=request.form["uname"]
            query=request.form["query"]

            with sqlite3.connect("application.db")as con:
                cur=con.cursor()
                cur.execute("INSERT INTO ISSUE(NAME,QUERY)VALUES(?,?)",(session['user'],query))
                con.commit()
                msg="Query Successfully Registered"
        except:
            con.rollback()
            msg="We cannot add the Query to the list"
        finally:
            return render_template("home.html")

@app.route("/showIssue")
def showallProb():
    con = sqlite3.connect("application.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM ISSUE")
    rows = cur.fetchall()

    return render_template("userIssues.html", rows=rows)

def files_allowed(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed_extension

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans



if __name__=='__main__':
    app.run(debug=True,port=9000)

