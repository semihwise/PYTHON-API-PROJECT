import cx_Oracle
import json
from json import JSONEncoder
from flask import Flask, request,jsonify
from flask_restful import Resource, Api
import pandas as pd
import logging
import sys
import traceback
import re
import requests
from flask_cors import CORS



logging.basicConfig(stream=sys.stderr)

app =  Flask(__name__)
api = Api(app)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"


class EmployeeEncoder(JSONEncoder):
        def default(self, o):
            return (o.__dict__)

class Employee:
    def __init__(self, employee_id, first_name, last_name):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
      
	

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4,ensure_ascii=False)
			
def getConnection():
    host = 'DESKTOP-G7L5UG4.mshome.net:1521/orcl.mshome.net'  # hostaddr:port
    uname = 'HR'
    pw = 'hr'
    constr=uname+'/'+pw+'@'+host
    connection = cx_Oracle.connect(constr,encoding = "UTF-8", nencoding = "UTF-8")
    return connection

		
def fn_adlari_getir():
		db = getConnection();
		cursor = db.cursor()
		cursor.execute("SELECT EMPLOYEE_ID,FIRST_NAME,LAST_NAME FROM EMPLOYEES_X")
		row2 = cursor.fetchall
		my_list=[]
		me = Object()
		try:

			while row2:
  		
				#print (row)
				row = cursor.fetchone()
				say=0
				#print(row[0])
				#me = Object()
	
				for r in row:
	
					say=say+1
					#print("say:"+str(say)+ " Deger:"+row[0]+" -- "+row[1]+" - "+row[2])
					me.id=row[0]
					me.first_name=row[1]
					me.last_name=row[2]
					me2=Employee(row[0],row[1],row[2])
					
					my_list.append(me2)
					#my_list=my_list.encode('utf-8')
					#my_list.append(me.adi)
					#my_list.append(me.soyadi)
					#print(me2.toJSON())
					break

			
		except Exception as e:
			print(e)		
	
		return (my_list)


#POST METODU---------------------------------------------------------------------------

def fn_adlari_gonder():
		db = getConnection();
		cursor = db.cursor()
		cursor.execute("SELECT EMPLOYEE_ID,FIRST_NAME,LAST_NAME FROM EMPLOYEES_X")
		row2 = cursor.fetchall()
		data = {'employee_id':'employee_id',
				'first_name':'first_name',
				'last_name': 'last_name'}

		res = requests.post('http://127.0.0.1:5000/bilgileri_gonder',
							 data = json.dumps(data))
		print(data)
	
#GET METODU-------------------------------------------------------------------------------------------
class bilgileri_getir(Resource):
		def get(self):
			# conn = getConnection  # connect to database
			# query = conn.execute("SELECT *  FROM networks.NETWORKS_CONCURRENT_QUEUES  WHERE CONCURRENT_QUEUE_ID in (21,22,23,5,13)")  # This line performs query and returns json result
			data  = fn_adlari_getir()	
			#return (EmployeeEncoder().encode(data)).encode('utf-8')
			return (EmployeeEncoder().encode(data))
			
#POST METODU---------------------------------------------------------------------------------------------

class bilgileri_gonder(Resource):
		def post(self):
			content_type = request.headers.get('Content-Type')
			
			#posted_data = request.get_json()
			#print(posted_data)
			raw_cocktail = request.get_json()

			if (content_type == 'application/json'):
				#print(raw_cocktail['adi'])
				print(raw_cocktail['your_data'][0]['email'])
				db = getConnection();
				cursor = db.cursor()
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES ")
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES (%s, %s, %s)", (var1, var2, var3))
				#cursor.execute("Insert into HR.EMPLOYEES_X (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL)  Values  (%d, %s, %s, %s)",raw_cocktail['your_data'][1]['id'],raw_cocktail['your_data'][1]['adi'],raw_cocktail['your_data'][1]['soyadi'],raw_cocktail['your_data'][1]['email'])
				cursor.execute("INSERT INTO EMPLOYEES_X (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL) VALUES (:1, :2, :3, :4)", (raw_cocktail['your_data'][0]['id'],raw_cocktail['your_data'][0]['adi'],raw_cocktail['your_data'][0]['soyadi'],raw_cocktail['your_data'][0]['email']))
				
				cursor.close()

				db.commit()

				return "TAMAM"

#DELETE METODU-------------------------------------------------------------------------------------------------

class bilgileri_sil(Resource):
		def post(self):
			content_type = request.headers.get('Content-Type')
			
			#posted_data = request.get_json()
			#print(posted_data)
			raw_cocktail = request.get_json()

			if (content_type == 'application/json'):
				print(raw_cocktail['your_data'][0]['id'])
				#print(raw_cocktail['your_data'][0]['id'])
				db = getConnection();
				cursor = db.cursor()
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES ")
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES (%s, %s, %s)", (var1, var2, var3))
				#cursor.execute("Insert into HR.EMPLOYEES_X (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL)  Values  (%d, %s, %s, %s)",raw_cocktail['your_data'][1]['id'],raw_cocktail['your_data'][1]['adi'],raw_cocktail['your_data'][1]['soyadi'],raw_cocktail['your_data'][1]['email'])
				cursor.execute("DELETE FROM EMPLOYEES_X WHERE EMPLOYEE_ID=:id ", {'id':(raw_cocktail['your_data'][0]['id'])})
				#cur.execute(statement, {'id':1})

				
				cursor.close()

				db.commit()

				return "2"

#UPDATE METODU------------------------------------------------------------------------------------------------------------------


class bilgileri_guncelle(Resource):
		def post(self):
			content_type = request.headers.get('Content-Type')
			
			#posted_data = request.get_json()
			#print(posted_data)
			raw_cocktail = request.get_json()

			if (content_type == 'application/json'):
				print(raw_cocktail['your_data'][0]['id'])
				#print(raw_cocktail['your_data'][0]['id'])
				db = getConnection();
				cursor = db.cursor()
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES ")
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES (%s, %s, %s)", (var1, var2, var3))
				#cursor.execute("Insert into HR.EMPLOYEES_X (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL)  Values  (%d, %s, %s, %s)",raw_cocktail['your_data'][1]['id'],raw_cocktail['your_data'][1]['adi'],raw_cocktail['your_data'][1]['soyadi'],raw_cocktail['your_data'][1]['email'])
				cursor.execute("UPDATE EMPLOYEES_X  SET FIRST_NAME=:2, LAST_NAME=:3, EMAIL=:4  WHERE EMPLOYEE_ID=:5",{'2':(raw_cocktail['your_data'][0]['adi']),'3':(raw_cocktail['your_data'][0]['soyadi']),'4':(raw_cocktail['your_data'][0]['email']),'5':(raw_cocktail['your_data'][0]['id'])})
				#cur.execute(statement, {'id':1})
				
				cursor.close()

				db.commit()

				return "TAMAMLANDI"


#***********************************************************************************************************************************    


class uname_pass(Resource):
		def post(self):
			content_type = request.headers.get('Content-Type')
			
			#posted_data = request.get_json()
			#print(posted_data)
			raw_cocktail = request.get_json()

			if (content_type == 'application/json'):
				print(raw_cocktail['your_data'][0]['uname'])
				print(raw_cocktail['your_data'][0]['password'])
				#print(raw_cocktail['your_data'][0]['id'])
				db = getConnection();
				cursor = db.cursor()
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES ")
				#cursor.execute("INSERT INTO EMPLOYEES_X VALUES (%s, %s, %s)", (var1, var2, var3))
				#cursor.execute("Insert into HR.EMPLOYEES_X (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL)  Values  (%d, %s, %s, %s)",raw_cocktail['your_data'][1]['id'],raw_cocktail['your_data'][1]['adi'],raw_cocktail['your_data'][1]['soyadi'],raw_cocktail['your_data'][1]['email'])
				#cursor.execute=('''SELECT * FROM LOGIN WHERE @uname = [uname] AND @password = [passwd]''')#WHERE UNAME =:1 AND PASSWORD = :2"
				#cursor.execute("SELECT count(*) FROM LOGIN WHERE UNAME = :uname AND PASSWORD = :pssword", (raw_cocktail['your_data'][0]['uname'],raw_cocktail['your_data'][0]['passwd']))
				#cursor.execute("SELECT * FROM LOGIN WHERE uname="+raw_cocktail['your_data'][0]['uname']+"AND password=" + raw_cocktail['your_data'][0]['passwd'])
				# {'1':(raw_cocktail['your_data'][0]['uname']),'2':(raw_cocktail['your_data'][0]['passwd'])})
				#sql = (cursor.execute("SELECT COUNT(*) FROM LOGIN WHERE uname=:uname AND password=:passwd", {"uname" : uname}, {"password" : passwd}).fetchall()[0][0] == 0)
				#cur.execute(statement, {'id':1})
				#sql = "select * from sometable where somefield = :myField and otherfield = :anotherOne"
				
				# fetch the row
				cursor.execute("""
        		select count(*)
        		from LOGIN
        		where UNAME = :uname and PASSWORD = :passwd""", uname=raw_cocktail['your_data'][0]['uname'],passwd=raw_cocktail['your_data'][0]['password'])
				count_id = str(cursor.fetchone()).replace("(","").replace(")","").replace(",","")
				
				cursor.close()

				db.commit()

				#return count_id
				#return (EmployeeEncoder().encode("data":count_id))
				#x='{"sonuc":'+'"'+count_id+'"}'
				x='{"sonuc":'+'"'+count_id+'"}'
				#return (toJSON("data",count_id))
				#return json.dumps(x)
				json_object = json.loads(x)
				#employee_string = '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'
				#check data type with type() method
				#print(type(employee_string))
				return json_object
				#convert string to  object

				




    			   
#*******************************************************************************************************************************************************
api.add_resource(bilgileri_getir, '/bilgileri_getir') # Route_1
api.add_resource(bilgileri_gonder, '/bilgileri_gonder',methods=['POST'])
api.add_resource(bilgileri_sil, '/bilgileri_sil', methods=['POST'])
api.add_resource(bilgileri_guncelle, '/bilgileri_guncelle', methods=['POST'])
api.add_resource(uname_pass, '/uname_pass', methods=['POST']) # Route_1

if __name__ == '__main__':
    print("the  main")
    bilgileri_getir()
    app.run(
        debug=True,
        #host = '127.0.0.1',
        host = '194.27.53.5',
        port = 5000
    )