from flask import Flask, render_template, redirect, flash, url_for, request
app=Flask(__name__)


app.config['SECRET_KEY'] = '8baf5a82959656033eedcbd7b5dfc383'
import sqlite3
con=sqlite3.connect('site.db', check_same_thread=False)
c=con.cursor()
def create_table():
	c.execute('create table Data(Name text,Age int,Email text,Salary int)')
	con.commit()
#create_table()


@app.route('/insert',methods=['GET','POST'])
def insert_data():
	if request.method=='POST':
		Name=request.form["Name"]
		Age=request.form["Age"]
		Email=request.form["Email"]
		salary=request.form["salary"]
		c.execute("insert into Data (Name,Age,Email,Salary) values (?,?,?,?)",(Name,Age,Email,salary))
		con.commit()
		#return f'<h1>Data Added ---->{Name}--- {Age}-- {Email} ---{salary}</h1>'
		flash(f"{Name} Accountt Added Successfully!")
		return redirect(url_for('read_info'))

	else:
		return render_template('insert.html')




@app.route('/delete/<Name>',methods=['GET','POST'])
def delete_data(Name):
	c.execute("delete from Data where Name=?",(Name,))
	con.commit()
	#return '<h1>Deleted Successfully </h1>'
	flash(f"{Name} Accountt Deleted Successfully!")
	return redirect(url_for('read_info'))

@app.route('/')
def read_info():
	c.execute('select rowid,Name,Age,Email,salary from Data')
	c_data=c.fetchall()
	return render_template('read.html',list_users=c_data)


@app.route('/get/<Name>', methods=['GET','POST'])
def get_data(Name):
	c.execute("select rowid,Name,Age,Email,salary from Data where Name=?",(Name,))
	c_data1=c.fetchall()
	#return f'<h2>{c_data1}</h2>'
	return render_template('update.html',list_users=c_data1)


@app.route("/update/<id>",methods=['POST'])
def update_data(id):
	if request.method=='POST':
		Name=request.form["Name"]
		Age=request.form["Age"]
		Email=request.form["Email"]
		salary=request.form["salary"]
		c.execute("update Data set Name=?,Age=?,Email=?,Salary=? where rowid=?",(Name,Age,Email,salary,id))
		con.commit()
		flash(f"{Name} Updated Successfully!")
		return redirect(url_for('read_info'))


if __name__=="__main__":
	app.run(debug=True)