import os








from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
app=Flask(__name__)
engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/register")
def register():
	table = db.execute("SELECT * FROM flights").fetchall()
	return render_template("register.html", table=table)

@app.route("/flights")
def flights():
	table=db.execute("SELECT * FROM flights").fetchall()
	return render_template("flights.html", table=table)

@app.route("/delete", methods=["GET", "POST"])
def delete():
	if request.method=="GET":
		table=db.execute("SELECT * FROM flights").fetchall()
		return render_template("delete.html", table=table)
	id=request.form.get("flight")
	if not id:
		table=db.execute("SELECT * FROM flights").fetchall()
		return render_template("delete.html", table=table)
	db.execute("DELETE FROM passengers WHERE flight_id=:id",{"id":id})
	db.execute("DELETE FROM flights WHERE id=:id", {"id": id})
	db.commit()
	return redirect("/")
@app.route("/<int:flight_id>")
def passengers(flight_id):
	table=db.execute("SELECT * FROM flights WHERE id=:flight_id", {"flight_id": flight_id}).fetchall()
	passenger=db.execute("SELECT * FROM passengers WHERE flight_id=:flight_id", {"flight_id": flight_id}).fetchall()
	
	return render_template("passengers.html", table=table[0], passengers=passenger)
	
@app.route("/registrant", methods=["POST"])
def success():
	id=request.form.get("id")
	name=request.form.get("Name")
	db.execute("INSERT INTO passengers(flight_id, name) VALUES(:flight_id, :name)", {"flight_id":id, "name":name})
	db.commit()
	w=db.execute("SELECT * FROM flights WHERE id=:id",{"id":id}).fetchall()
	words=w[0][1]+"-"+w[0][2]
	return render_template("success.html", words=words)
#Check for if exists, and make work...
@app.route("/create", methods=["GET", "POST"])
def create():
	if request.method=="GET":
		return render_template("create.html")
	origin=request.form.get("origin")
	destination=request.form.get("destination")
	time=request.form.get("duration")
	destination=destination.upper()
	origin=origin.upper()
	if not origin or not destination or not time:
		print("Not Inputted", flush=True)
		return render_template("create.html")
	if not time.isdigit():
		print("Digits", flush=True)
		return render_template("create.html")
	db.execute("INSERT INTO flights(origin, destination, time) VALUES(:origin, :destination, :time)", {"origin": origin, "destination": destination, "time": time})
	db.commit()
	return redirect("/")
	

@app.route("/<string:origin><string:destination><int:duration>")
def make(origin, destination, duration):
	value=str(duration)
	db.execute("INSERT INTO flights(origin, destination, duration) VALUES(:origin, :destination, :duration);", {"origin":origin, "destination":destination, "duration":value})
	db.commit()
	return redirect("/")
