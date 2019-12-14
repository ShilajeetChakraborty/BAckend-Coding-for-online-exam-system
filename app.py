#this is the back end program only.

import json
import subprocess

from flask import Flask, request
from flask_cors import CORS
import pymysql
from flask_mail import Mail
from flask_mail import Message

import mysql.connector
import checkTestCasePassed

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

##creating database
mydb = pymysql.connect(
    host='192.168.0.216',
    user='trainee',
    password='123456',
    database='new_schema'
    )

print(mydb)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE MY_DATABASE")
# mycursor.execute("CREATE TABLE PROGRAMS (id INT AUTO_INCREMENT PRIMARY KEY, code VARCHAR(255))")
# mycursor.execute("CREATE TABLE CANDIDATE_SKILL (id INT AUTO_INCREMENT PRIMARY KEY, SKILL VARCHAR(255))")
# mycursor.execute(
#    "CREATE TABLE CANDIDATE_DETAILS (id INT AUTO_INCREMENT PRIMARY KEY ,First_Name varchar(255),Last_Name varchar(255),Email varchar(255),Ph_No varchar(255),College varchar(255),Work_Exp varchar(255),Company_Name varchar(255),"
#    "Years varchar(255),Skills varchar(255),Current_CTC varchar(255),Expected_CTC varchar(255),Current_Location "
#    "varchar(255),checked boolean DEFAULT false, score INT default 0)")


@app.route('/get_skills', methods=['GET'])
def get_skills():
    mycursor.execute("SELECT * FROM CANDIDATE_SKILL ")
    skl = mycursor.fetchall()

    return {"skills": skl}

# once used for creating the table and then close the hashs.

# #First Name:
# Last Name:
# Email:
# Phone Number:
# College:
# Work Exper:if:Fresher:(stop asking)......else:Company Name, Number of years,.
# Skills: (Word by word)
# Current CTC: (if experienced)
# Expected CTC:....(As per market).
# Current Location.


@app.route('/get_data_form', methods=['POST'])
def get_data_form():
    data = request.form

    print(data)
    print(type(data))

    First_Name = data["fname"]
    Last_Name = data["lname"]
    Email = data["email"]
    Ph_No = data["number"]
    College = data["college"]
    Work_Exp = data["exp"]
    Company_Name = data["company"]
    Years = data["noOfYear"]
    Skills = data["skills"]
    Current_CTC = data["current_ctc"]
    Expected_CTC = data["expected_ctc"]
    Current_Location = data["current_loc"]
    # RESUME = par["RESUME"]

    mydb = pymysql.connect(host='192.168.0.216',
                           database='new_schema',
                           user='trainee',
                           password='123456')


    mycursor = mydb.cursor()
    mycursor.execute("""INSERT INTO CANDIDATE_DETAILS(First_Name,Last_Name,Email,Ph_No,College,Work_Exp,Company_Name,Years,Skills,Current_CTC,Expected_CTC,Current_Location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(First_Name, Last_Name, Email, Ph_No, College, Work_Exp, Company_Name,Years, Skills, Current_CTC, Expected_CTC, Current_Location))
    mydb.commit()



    return {"message":"value inserted"},200

    # except pymysql.connect.Error as error:
    #     mydb.rollback()  # rollback if any exception occured
    #     print("Failed inserting record into python_users table {}".format(error))
    #     # closing database connection.
    #
    #     if mydb.is_connect():
    #         cursor.close()
    #         mydb.close()
    # print("MySQL connection is closed")

@app.route('/receiveSkills')
def receiveSkills():
    mydb = pymysql.connect(host='192.168.0.216',
                           database='new_schema',
                           user='trainee',
                           password='123456')

    mycursor = mydb.cursor()
    mycursor.execute("""SELECT skills FROM CANDIDATE_DETAILS""")
    rows = mycursor.fetchall()

    # row_list = list(rows)
    print("Record inserted successfully into python_users table")
    return {"message": "value received", "data": rows}, 200

@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


@app.route('/check_code', methods=['POST'])
def check_code():
    data = request.data
    par = json.loads(data)
    with open('candidate.py', 'w+') as f:
        read_data = f.write(par["code"])

        # mycursor = mydb.cursor()

        # sql = "INSERT INTO code (par['code']) VALUES (%s, %s)"
        # val = ("John", "Highway 21")
        # mycursor.execute(sql, val)

        mydb.commit()
    out = subprocess.Popen(["python", "candidate.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    if stdout == b'':
        return {"status": 200, "message": "Code Syntax Correct"}, 200
    else:
        return {"status": 200, "message": "Code Syntax In-Correct"}, 200


@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.data
    par = json.loads(data)
    print(data)
    with open('candidate.py', 'w+') as f:
        read_data = f.write(par["code"])

    testCases = getattr(__import__(par["testCases"]), par["testFuncName"])
    testCasesList = testCases()
    print(testCasesList)

    try:
        checkSingleTestCase = checkTestCasePassed.singleTestCasePassed("candidate", par["defCode"], par["codeFunc"],
                                                                       testCasesList[0])

        print(checkSingleTestCase)
        if checkSingleTestCase:
            return {"status": 200, "message": "Code Executes and running Successfully"}, 200
        else:
            return {"status": 200, "message": "Output not correct"}, 200
    except Exception as e:
        return {"status": 200, "message": "Code Not Correct"}, 200


@app.route('/test_case_passed', methods=['POST'])
def test_case_passed():
    data = request.data
    par = json.loads(data)
    with open("candidate.py", "w+") as f:
        read_data = f.write(par["code"])
    testCases = getattr(__import__(par["testCases"]), par["testFuncName"])
    testCasesList = testCases()
    try:
        checkTestCases, passCounter, failCounter = checkTestCasePassed.testCasePassed("candidate", par["defCode"],
                                                                                      par["codeFunc"],
                                                                                      testCasesList)
        if checkTestCases:
            return {"status": 200, "message": "User Passed", "passCounter": passCounter,
                    "failCounter": failCounter}, 200
        else:
            return {"status": 200, "message": "User Not Passed", "passCounter": passCounter,
                    "failCounter": failCounter}, 200
    except Exception as e:
        return {"status": 200, "message": "Code Not Correct"}, 200


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'chakraborty.shilajeet145@gmail.com',
    MAIL_PASSWORD = 'mniag12345&*',
))

mail = Mail(app)

@app.route("/sendMail")
def sendMail():

    msg = Message("Hello",sender="chakraborty.shilajeet145@gmail.com",recipients=["chakraborty.shilajeet14@gmail.com"])
    msg.body = "Hi, your cv is shortlisted. Here is the link for the coding round. Please enter into the link to proceed : http://localhost:4200/codingEnv"

    mail.send(msg)
    return {"message":"message sent"},200
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
