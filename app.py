from flask import Flask,request, render_template,abort, session, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
import sqlite3,folium
from flask_admin.contrib.sqla import ModelView
import os, json
#.\env\Scripts\activate.ps1
from sqlalchemy.ext.automap import automap_base
from impl2 import *

app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=None
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\sem 4\mini project\project\coordinates.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
coordinates = Base.classes.coordinates
hints = Base.classes.hints
admin = Admin(app)
 
#login for admin

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

admin.add_view(SecureModelView(coordinates, db.session))
admin.add_view(SecureModelView(hints, db.session))
    

@app.route("/")
def home():
    return render_template('homepage.html')

#ignore
@app.route('/map')
def map():
    return render_template('routes.html')

#ignore

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "admin123" and request.form.get("password") == "admin1234":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed=True)
    return render_template("login.html")

@app.route("/trial")
def onw():
    return render_template("geoloc.html")

@app.route("/mpmaps", methods=["GET", "POST"])
def ont():
    try:
        sqliteConnection = sqlite3.connect('E:\sem 4\mini project\project\coordinates.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
 
        sqlite_select_query = """SELECT x_coord, y_coord,name,description,fac_type,image FROM coordinates;"""
       
        cursor.execute(sqlite_select_query)
       
        items = cursor.fetchall()
        #print(items)
        data2=[{"x_coord":19.076999,"y_coord":72.900914,"name":"somaiya vidyavihar","des":"welcome to svv"}]
        print(data2)
        cursor.execute("select sname,count(*)from log group by sname order by count(sname) desc limit 3")
        loglist=cursor.fetchall()
        loglist=[x[0].capitalize() for x in loglist]
        print(loglist)
        sugg=[]
        if request.method == "POST":
            # sugg=[]
            book = request.form['book']
            cursor.execute("SELECT x_coord, y_coord,name,description,fac_type,image FROM coordinates WHERE lower(name) like '"+str(book).lower()+"' or name  in (SELECT hints.name from hints where lower(hints.keyword) = '"+str(book).lower()+"')")
            sqliteConnection.commit()
            data = cursor.fetchall()
            #data=data+data1
            print("data:",data)
            if len(data)==0:
                cursor.execute("select name from coordinates")
                datanon = cursor.fetchall()
                prob=exec(datanon,book)
                print(prob)
                topp="Try searching for '"+ str(prob[0][0]) +"' instead"
                sugg.append(topp)
                print(sugg[0])
            data1=list()
            cursor.execute("insert into log(sname) values('"+str(book).lower()+"')")
            sqliteConnection.commit()
            for item in data:
                item1={"x_coord":item[0],"y_coord":item[1],"name":item[2],"des":item[3],"image":item[5]}
                data1.append(item1)
            print(data1)
            
            return render_template('map6.html',data=data1,items=items,sugg=sugg,loglist=loglist)
        else:
            return render_template('map6.html',data=data2,items=items,sugg=sugg,loglist=loglist)
 
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
    return render_template('map6.html',data=data2,items=items)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)

#.\env\Scripts\activate.ps1