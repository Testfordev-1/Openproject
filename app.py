from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    # database connection
    con = sqlite3.connect("employees.db")

    con.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary INTEGER
    )
    """)

    con.close()

create_table()


@app.route("/")
def home():

    con=sqlite3.connect("employees.db")
    cursor=con.cursor()

    cursor.execute(
        "SELECT * FROM employees"
    )

    employees=cursor.fetchall()

    con.close()

    return render_template(
        "home.html",
        employees=employees
    )


@app.route("/add",methods=["GET","POST"])
def add_employee():

    if request.method=="POST":

        name=request.form["name"]
        department=request.form["department"]
        salary=request.form["salary"]

        con=sqlite3.connect(
            "employees.db"
        )

        cursor=con.cursor()

        cursor.execute(
        """
        INSERT INTO employees
        (name,department,salary)

        VALUES(?,?,?)
        """,
        (name,department,salary)
        )

        con.commit()
        con.close()

        return redirect("/")

    return render_template(
        "add.html"
    )


@app.route("/delete/<int:id>")
def delete_employee(id):

    con=sqlite3.connect(
    "employees.db"
    )

    cursor=con.cursor()

    cursor.execute(
    "DELETE FROM employees WHERE id=?",
    (id,)
    )

    con.commit()

    con.close()

    return redirect("/")
# New application Code

if __name__=="__main__":
    app.run(debug=True)