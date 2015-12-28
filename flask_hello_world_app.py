from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

import requests
import re
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///numbersindia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class mobileNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    operator = db.Column(db.String(24), nullable=False)
    state = db.Column(db.String(52), nullable=False)
    icon = db.Column(db.Integer, nullable=False)
    __tablename__ = "mobileNumbers"

    def __init__(self, number, operator, state,icon):
        self.number = number
        self.operator = operator
        self.state = state
        self.icon = icon

    def __repr__(self):
        return '<operator {}>'.format(self.operator)


class pinCodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officename = db.Column(db.String(60), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    taluk = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    __tablename__ = "pincodes"

    def __init__(self, officename, pincode, taluk, district, state):
        self.officename = officename
        self.pincode = pincode
        self.taluk = taluk
        self.district = district
        self.state = state 

    def __repr__(self):
        return '<officename {}>'.format(self.officename)



class STDcodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stdcode = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)


    def __init__(self, stdcode, city, state):
        self.stdcode = stdcode
        self.city = city
        self.state = state

    def __repr__(self):
        return '<City {}>'.format(self.city)

	



@app.route('/')
def index():
    return render_template('index.html')

def fmt_pin(code):
	return code.replace(" ","").replace("-","").replace("_","").strip()

def int_pin(code):
	code = fmt_pin(code)
	return int(code)


@app.route('/find_pin_codes', methods=['POST','GET'])
def pincodes():
    if request.method == 'POST':  

        if request.form.get("pincode", "") != "":
            pincode = request.form['pincode']
            pincode = int_pin(pincode)
            bypincode = pinCodes.query.filter(pinCodes.pincode == 506001).all()
            print(bypincode)
            return render_template('pincodes.html',
                	                    bypincode = bypincode,                                      
                                        )
            
        elif request.form.get("area", "") != "":
            if len(request.form.get("area", ""))>3:
                area = request.form['area']
                area = area.strip()
                try:
                    byoffice = pinCodes.query.filter(pinCodes.officename.startswith(area)).all()
                    print(byoffice)
                    bytaluk = pinCodes.query.filter(pinCodes.taluk.startswith(area)).all()
                    return render_template('pincodes.html',
                                            byoffice = byoffice,
                                            bytaluk = bytaluk,
                                            area = area,
                                           )
                except Exception as e:
                    return render_template('pincodes.html', 
                                            error = e
                                          ) 
            else:
                return render_template('pincodes.html', 
                                        error = "Please enter an area with atleast 4 letters"
                                        )
        
        else:
            return render_template('pincodes.html',
                                error = "No value was entered!"                             
                               )
                                      
    else:
        return render_template('pincodes.html', 
                               )


def dnd_return(number,my_timeout):
    try:
        r =requests.get("https://dndcheck.p.mashape.com/index.php?mobilenos={}".format(number), timeout =my_timeout,headers ={"X-Mashape-Key": "obqeZksomumshUE8EvVYIqvRXWNsp1waVYpjsnUOa3brsHCokK"})
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        return "Error fetching DND info"
    else:
        return r.text

def fmt_mobile(number):
    number = number.replace("+91","")
    number =  re.sub(r'[^\d.]+', '', number)
    return number.strip()

def int_strip4(number):
    number = fmt_mobile(number)
    return int(number[:4])



@app.route('/track_mobile_numbers', methods=['POST','GET'])
def mobile():
    if request.method == 'POST':
        if request.form.get("number", "") != "":
            number = request.form['number']
            dnd_list = []
            if len(fmt_mobile(number)) == 10:
                try:
                    dnd_dump = dnd_return(fmt_mobile(number),9)
                    json_dump = json.loads(dnd_dump)
                    j = json_dump[0]
                    
                    if j['DND_status'] != "deactivated" and j['DND_status'] != "off":
                        dnd_list.append("DND status : "+j['DND_status'])
                        dnd_list.append("Date of Activation : "+j['activation_date'])
                        dnd_list.append("Preference : "+j['current_preference'])
                    
                    else:
                        dnd_list.append("DND status : "+j['DND_status'])
                except Exception as e:
                    dnd_list.append(e)
            else:
                dnd_list.append("The number should contain 10 digits")
            
            
            try:
                num = mobileNumbers.query.filter_by(number = int_strip4(number)).first()
                return render_template('mobilenumbers.html', 
                                        strnumber = "Mobile number : " + fmt_mobile(number), 
                                        operator = "Operator : " + num.operator, 
                                        state = "State : " + num.state,
                                        dnd = dnd_list
                                      )
            except Exception as err:
                return render_template('mobilenumbers.html',
                                        error = err
                                      )
        else:
            return render_template('mobilenumbers.html',
                                    error = "Please enter a valid number"
                                  )
    else:
        return render_template('mobilenumbers.html')


@app.route('/find_std_codes', methods=['POST','GET'])
def stdcodes():
    if request.method == 'POST':
        if request.form.get("city", "") != "":
            city = request.form["city"]
            city = city.strip()
            try:
                bycity = STDcodes.query.filter(STDcodes.city.startswith(city)).all() 
                return render_template('stdcodes.html',
                                        bycity = bycity,
                                        city = city,
                                       ) 
            except Exception as e:
                return render_template('stdcodes.html',
                                        error =e,
                                        )
        else:
            return render_template('stdcodes.html',
                                    error = "No value was entered!"                             
                                   )
                    
    else:
        return render_template('stdcodes.html')




@app.route('/track_vehicle_numbers', methods=['POST','GET'])
def vehicle():
    if request.method == 'POST':
        return render_template('vehicle.html')
    else:
        return render_template('vehicle.html')




if __name__ == '__main__':
    app.run(debug=True)
