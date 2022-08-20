from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("user_details.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/users", methods=["GET", "POST"])
def users():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM user")
        users = [
            dict(id=row[0], first_name=row[1], last_name=row[2], company_name=row[3],
            age=row[4], city=row[5], state=row[6], zip=row[7],
            email=row[8], web=row[9]
            )
            for row in cursor.fetchall()
        ]
        if users is not None:
            return jsonify(users)

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        company_name = request.form["company_name"]
        age = request.form["age"]
        city = request.form["city"]
        state = request.form["state"]
        zip = request.form["zip"]
        email = request.form["email"]
        web = request.form["web"]
        sql = """INSERT INTO user (first_name, last_name, company_name,age,city,state,zip,email,web)
                 VALUES (?, ?, ?,?,?,?,?,?,?)"""
        cursor = cursor.execute(sql, (first_name, last_name, company_name,age,city,state,zip,email,web))
        conn.commit()
        return f"user created successfully", 201


@app.route("/user/<int:id>", methods=["GET", "PUT", "DELETE"])
def user(id):
    conn = db_connection()
    cursor = conn.cursor()
    user = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM user WHERE id=?", (id,))
        user = [
            dict(id=row[0], first_name=row[1], last_name=row[2], company_name=row[3],
            age=row[4], city=row[5], state=row[6], zip=row[7],
            email=row[8], web=row[9]
            )
            for row in cursor.fetchall()
        ]
        if user is not None:
            return jsonify(user)
        return 'User not found'

    if request.method == "PUT":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        company_name = request.form["company_name"]
        age = request.form["age"]
        city = request.form["city"]
        state = request.form["state"]
        zip = request.form["zip"]
        email = request.form["email"]
        web = request.form["web"]
        sql = """UPDATE user
                SET first_name=?, last_name=?, company_name=?,age=?,city=?,state=?,zip=?,email=?,web=?
                WHERE id=? """

        updated_user = {
            "id": id,
            "first_name": first_name,
            "last_name": last_name,
            "company_name": company_name,
            "age": age,
            "city": city,
            "state": state,
            "zip": zip,
            "email": email,
            "web": web,
        }
        conn.execute(sql, (first_name, last_name, company_name,age,city,state,zip,email,web,id,))
        conn.commit()
        return jsonify(updated_user)

    if request.method == "DELETE":
        sql = """ DELETE FROM user WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The user with id: {} has been ddeleted.".format(id), 200

@app.route("/search/<first_name>", methods=["GET"])
def search_user(first_name):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM user where first_name like "+'"'+ first_name+'%'+'"')
        user = [
            dict(id=row[0], first_name=row[1], last_name=row[2], company_name=row[3],
            age=row[4], city=row[5], state=row[6], zip=row[7],
            email=row[8], web=row[9]
            )
            for row in cursor.fetchall()
        ]
        if user is not None:
            return jsonify(user)
        return 'User not found'


@app.route('/api/users')
def check():
    default_limit=5
    page=request.args['page']
    limit=request.args['limit']
    name=request.args['name']
    sort=request.args['sort']
    
    conn = db_connection()
    cursor = conn.cursor()
    if '-' not in sort:
        cursor = conn.execute("SELECT * FROM user"+ " where first_name like "+'"'+ name+'%'+'"'+" ORDER BY " +sort[0:]+" ASC")
    else:
        cursor = conn.execute("SELECT * FROM user"+ " where first_name like "+'"'+ name+'%'+'"'+" ORDER BY " +sort[0:]+" DESC")
    users = [
            dict(id=row[0], first_name=row[1], last_name=row[2], company_name=row[3],
            age=row[4], city=row[5], state=row[6], zip=row[7],
            email=row[8], web=row[9]
            )
            for row in cursor.fetchall()
        ]
    
    if(int(page)>1):
        users=users[default_limit*int(page):default_limit*int(page)+int(limit)]
    else:
        users=users[:int(limit)]
    
    return jsonify(users)
    
    
if __name__ == "__main__":
    app.run(debug=True)