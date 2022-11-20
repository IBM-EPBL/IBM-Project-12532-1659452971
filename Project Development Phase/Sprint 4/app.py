from flask import Flask, redirect, url_for, request, render_template
import urllib.parse
import ibm_db
import requests
import sendgrid

import os
from sendgrid.helpers.mail import *
app = Flask(__name__)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA .crt;UID=cxv46470;PWD=gjV37V3l8fdjQjbQ",'','')
print(conn)
print("Connection successful")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/aboutus')
def aboutus():
	return render_template('aboutus.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/requested', methods=['GET','POST'])
def requested():
	clean_data = ''
	if request.method == 'POST':
		content = request.get_data()
		# Parse query string part of a URL, and return a dictionary of the data
		x = urllib.parse.parse_qs(content)
		# clean noise that is, remove prefix character 'b
		for k, v in x.items():
			for i in v:
				clean_data = clean_data + i.decode('utf-8')+"\n"
		clean_data = clean_data.split("\n")
		# Enumerate user data
		blood = clean_data[0]
		address = clean_data[1]
		msg = "Need Plasma of your blood group for: "+address
		sql = "SELECT email FROM register WHERE bloodgroup='"+blood+"'"
		stmt = ibm_db.exec_immediate(conn, sql)
		dictionary = ibm_db.fetch_both(stmt)
		while dictionary != False:
			email = dictionary[0]
		        sg = sendgrid.SendGridAPIClient(api_key= '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' )

	                from_email = Email("19cs052@syedengg.co.in")
	                to_email = To(email)
	                subject = "Request for plasma"
	                content = Content("text/plain", msg)
	                mail = Mail(from_email, to_email, subject, content)
	                response = sg.client.mail.send.post(request_body=mail.get())
	                print(response.status_code)
	                print(response.body)
	                print(response.headers)
			dictionary = ibm_db.fetch_both(stmt)
		messages = {'message': 'Your request is sent to the concerned people.'}
		return render_template('request.html', messages=messages)
	return render_template('request.html')

@app.route('/signin',  methods=['GET', 'POST'])
def signin():
	clean_data = ''
	if request.method == 'POST':
		content = request.get_data()
		# Parse query string part of a URL, and return a dictionary of the data
		x = urllib.parse.parse_qs(content)
		# clean noise that is, remove prefix character 'b
		for k, v in x.items():
			for i in v:
				clean_data = clean_data + i.decode('utf-8')+"\n"
		clean_data = clean_data.split("\n")
		# Enumerate user data
		email = clean_data[0]
		password = clean_data[1]
		sql = "SELECT * FROM register WHERE email =? AND password=?"
		stmt = ibm_db.prepare(conn, sql)
		ibm_db.bind_param(stmt,1,email)
		ibm_db.bind_param(stmt,2,password)
		ibm_db.execute(stmt)
		account = ibm_db.fetch_assoc(stmt)
		if account:
			return redirect(url_for('statistics'))
		else:
			messages = {'message': 'Login unsuccessful. Incorrect username / password !'}
			return render_template('login.html', messages=messages)
	return render_template('login.html')

@app.route('/statistics')
def statistics():
	sql = "SELECT bloodgroup, count(bloodgroup) FROM register group by bloodgroup"
	stmt = ibm_db.exec_immediate(conn, sql)
	dictionary = ibm_db.fetch_both(stmt)
	data = []
	while dictionary != False:
		case = {'group': dictionary[0], 'count': dictionary[1]}
		data.append(case)
		dictionary = ibm_db.fetch_both(stmt)
	return render_template('statistics.html', data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
	clean_data = ''
	if request.method == 'POST':
		content = request.get_data()
		# Parse query string part of a URL, and return a dictionary of the data
		x = urllib.parse.parse_qs(content)
		# Remove prefix character 'b
		for k, v in x.items():
			for i in v:
				clean_data = clean_data + i.decode('utf-8')+"\n"
		clean_data = clean_data.split("\n")
		# Enumerate user data
		name = clean_data[0]
		email = clean_data[1]
		phone = clean_data[2]
		age=clean_data[3]
		sex = clean_data[4]
		bloodgroup = clean_data[5]
		address= clean_data[6]
		password = clean_data[7]
		cpassword=clean_data[8]
		query = "SELECT * FROM register WHERE email ='"+email+"'"
		stmt = ibm_db.exec_immediate(conn, query)
		row = ibm_db.fetch_assoc(stmt)
		if row:
			messages = {'message':'User already exist. Please login with details'}
			return render_template('register.html', messages=messages)
		else:
			insert_sql = "INSERT INTO register VALUES (?, ?, ?, ?, ?, ?, ?,?,?)"
			prep_stmt = ibm_db.prepare(conn, insert_sql)
			ibm_db.bind_param(prep_stmt, 1, name)
			ibm_db.bind_param(prep_stmt, 2, email)
			ibm_db.bind_param(prep_stmt, 3, phone)
			ibm_db.bind_param(prep_stmt, 4, age)
			ibm_db.bind_param(prep_stmt, 5, sex)
			ibm_db.bind_param(prep_stmt, 6, bloodgroup)
			ibm_db.bind_param(prep_stmt, 7, address)
			ibm_db.bind_param(prep_stmt, 8, password)
			ibm_db.bind_param(prep_stmt, 9, cpassword)
			ibm_db.execute(prep_stmt)
			messages = {'message': 'Registration success. Please login'}
			return render_template('register.html', messages=messages)
	else:
		return render_template('register.html')

if __name__ == '__main__':
       app.debug = True
       app.run()
