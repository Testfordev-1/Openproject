from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("employees.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary INTEGER
    )
    """)

    conn.close()

create_table()


@app.route("/")
def home():

    conn=sqlite3.connect("employees.db")
    cursor=conn.cursor()

    cursor.execute(
        "SELECT * FROM employees"
    )

    employees=cursor.fetchall()

    conn.close()

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

        conn=sqlite3.connect(
            "employees.db"
        )

        cursor=conn.cursor()

        cursor.execute(
        """
        INSERT INTO employees
        (name,department,salary)

        VALUES(?,?,?)
        """,
        (name,department,salary)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template(
        "add.html"
    )


@app.route("/delete/<int:id>")
def delete_employee(id):

    conn=sqlite3.connect(
    "employees.db"
    )

    cursor=conn.cursor()

    cursor.execute(
    "DELETE FROM employees WHERE id=?",
    (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)