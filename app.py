from flask import Flask,request, render_template,abort, session, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
import sqlite3,folium
from flask_admin.contrib.sqla import ModelView
import os, json
#.\env\Scripts\activate.ps1
from sqlalchemy.ext.automap import automap_base

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


@app.route('/gmap',methods=['GET', 'POST'])
def dolp():
    try:
        sqliteConnection = sqlite3.connect('E:\sem 4\mini project\project\coordinates.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
 
        sqlite_select_query = """SELECT x_coord, y_coord,name,description,fac_type FROM coordinates;"""
       
        cursor.execute(sqlite_select_query)
       
        items = cursor.fetchall()
        print(items)
        data2=[{"x_coord":19.076999,"y_coord":72.900914,"name":"somaiya vidyavihar","des":"welcome to svv"}]
        #data=[(19.076999, 72.900914,"somaiya vidyavihar","welcome to svv","uni")]
        #cursor.close()
        if request.method == "POST":
            book = request.form['book']
            cursor.execute("SELECT x_coord, y_coord,name,description,fac_type,image FROM coordinates WHERE lower(name) like '"+str(book).lower()+"' or name  in (SELECT hints.name from hints where lower(hints.keyword) = '"+str(book).lower()+"')")
            sqliteConnection.commit()
            data = cursor.fetchall()
            #data=data+data1
            print(data)
            data1=list()
            for item in data:
                item1={"x_coord":item[0],"y_coord":item[1],"name":item[2],"des":item[3]}
                data1.append(item1)
            print(data1)
            return render_template('map1.html',data=data1,leng=len(data1))
            
 
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
    return render_template('map1.html',data=data2,leng=len(data2))
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

@app.route("/trial2", methods=["GET", "POST"])
def ont():
    try:
        sqliteConnection = sqlite3.connect('E:\sem 4\mini project\project\coordinates.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
 
        sqlite_select_query = """SELECT x_coord, y_coord,name,description,fac_type FROM coordinates;"""
       
        cursor.execute(sqlite_select_query)
       
        items = cursor.fetchall()
        #print(items)
        data2=[{"x_coord":19.076999,"y_coord":72.900914,"name":"somaiya vidyavihar","des":"welcome to svv"}]
        print(data2)
        #data=[(19.076999, 72.900914,"somaiya vidyavihar","welcome to svv","uni")]
        #cursor.close()
        if request.method == "POST":
            book = request.form['book']
            cursor.execute("SELECT x_coord, y_coord,name,description,fac_type,image FROM coordinates WHERE lower(name) like '"+str(book).lower()+"' or name  in (SELECT hints.name from hints where lower(hints.keyword) = '"+str(book).lower()+"')")
            sqliteConnection.commit()
            data = cursor.fetchall()
            #data=data+data1
            print(data)
            data1=list()
            for item in data:
                item1={"x_coord":item[0],"y_coord":item[1],"name":item[2],"des":item[3]}
                data1.append(item1)
            print(data1)
            return render_template('map5.html',data=data1,leng=len(data1))
        else:
            return render_template('map5.html',data=data2,leng=len(data2))
 
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
    return render_template('map5.html',data=data2,leng=len(data2))

@app.route("/trial5")
def ond():
    return render_template("map4.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/gmap1',methods=['GET', 'POST'])
def holp():
    try:
        sqliteConnection = sqlite3.connect('E:\sem 4\mini project\project\coordinates.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
 
        sqlite_select_query = """SELECT x_coord, y_coord,name,description,fac_type,image FROM coordinates;"""
       
        cursor.execute(sqlite_select_query)
       
        items = cursor.fetchall()
        data2=[{"x_coord":19.076999,"y_coord":72.900914,"name":"somaiya vidyavihar","des":"welcome to svv"}]
        
    # data3=[(19.076999, 72.900914,"somaiya vidyavihar","welcome to svv","uni",'https://img.collegepravesh.com/2018/11/KJSCE-Mumbai.jpg')]
    
        if request.method == "POST":
            #data2=[{"x_coord":19.076999,"y_coord":72.900914,"name":"somaiya vidyavihar","des":"welcome to svv"}]
            book = request.form['book']
            cursor.execute("SELECT x_coord, y_coord,name,description,fac_type,image FROM coordinates WHERE lower(name) like '"+str(book).lower()+"' or name  in (SELECT hints.name from hints where lower(hints.keyword) = '"+str(book).lower()+"')")
            sqliteConnection.commit()
            data = cursor.fetchall()
            #data=data+data1
            print(data+["1"])
            data1=[(19.076999, 72.900914,"somaiya vidyavihar","welcome to svv","uni",'https://img.collegepravesh.com/2018/11/KJSCE-Mumbai.jpg')]
            for item in data:
                item1={"x_coord":item[0],"y_coord":item[1],"name":item[2],"des":item[3],"img":item[5]}
                data1.append(item1)
            print(data1+["2"])
            return render_template('map3.html',data=data1,leng=len(data1),items=items)
            
 
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
        # item1={"x_coord":19.076999,"y_coord":72.900914,"name":"somaiya vidyavihar","des":"welcome to svv"}
        # data2.append(item1)
    print(data2+["3"])
    return render_template('map3.html',data=data2,leng=len(data2),items=items)


if __name__ == '__main__':
    app.run(debug=True)

