from flask_hello_world_app import db, STDcodes 
f = open('telanganastd.txt')

lines = f.readlines()

for line in lines:
    line=line.replace("\n","")
    try:
        admin = STDcodes.query.filter_by(city=line.upper()).first()
        admin.state = "TELANGANA"

        db.session.commit()

    except:
    	pass
