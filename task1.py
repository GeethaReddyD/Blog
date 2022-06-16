
from flask import Flask,jsonify,request
import sqlite3

app=Flask(__name__) 


con = sqlite3.connect("test.db",check_same_thread=False)   
c = con.cursor() 



c.execute('CREATE TABLE IF NOT EXISTS Employees (id INTEGER PRIMARY KEY NOT NULL,name TEXT,location TEXT)')
c.close()
con.close()


def result(rows):  
    employee_details = [] 
    for items in rows:
        details = {"id":items[0],"name":items[1],"location":items[2]}
        employee_details.append(details)
    return employee_details

@app.route("/read",methods=["GET"])

def read_data(): 
    con = sqlite3.connect("test.db",check_same_thread=False)   
    c = con.cursor() 

    c.execute("select * from Employees")  
    rows = c.fetchall() 
    value = result(rows)
    con.commit()
    return jsonify(value)

@app.route("/insert",methods=["POST"])

def insert_data():

    element = request.json["id"]
    name = request.json["name"]  
    location = request.json["location"]
    con = sqlite3.connect("test.db",check_same_thread=False)   
    c = con.cursor() 
    
    c.execute("INSERT into Employees (id,name,location) values (?,?,?)",(element,name,location))
    con.commit()
    c.execute("select * from Employees")
    rows = c.fetchall() 
    values = result(rows)
    return jsonify(values)

@app.route("/update/<int:id>",methods=["PUT"])

def update_details(id):
    oldvalue = total_list()

    new_name = request.json["name"]
    new_location = request.json["location"] 
    con = sqlite3.connect("test.db",check_same_thread=False)   
    c = con.cursor() 
    c.execute("UPDATE Employees SET name=?,location=? WHERE id=?",(new_name,new_location,id))
    con.commit()
    updated_details = {"id":id,"name":new_name,"location":new_location}
    return {"newvalue":updated_details,"oldvalue": oldvalue}

@app.route("/getone/<int:id>",methods=["GET"])

def getone_details(id):
    con = sqlite3.connect("test.db",check_same_thread=False)   
    c = con.cursor() 

    c.execute(f"SELECT * FROM Employees WHERE id={id}")
    values=c.fetchone()
    con.commit()
    if values == None:
        return "Please enter valid id number"
    else:
       rows={"id":values[0],"name":values[1],"location":values[2]}
       return jsonify(rows)

    
@app.route("/delete/<int:id>",methods=["DELETE"])    

def delete_details(id):
    con = sqlite3.connect("test.db",check_same_thread=False)   
    c = con.cursor() 
    c.execute("DELETE FROM Employees WHERE id=?",(id,))
    con.commit()
    
    return "Deleted Successfully"  

def total_list():
    con = sqlite3.connect("test.db",check_same_thread=False)   
    c = con.cursor() 
    c.execute("select * from Employees")
    rows=c.fetchall()
    value=result(rows)
    con.commit
    return value      
        
    
if __name__ == "__main__":
       app.run(debug=True)
