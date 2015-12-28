from flask_hello_world_app import db, pinCodes 

districts = ["Adilabad","Hyderabad", "Karim Nagar", "Khammam", "Mahabub Nagar", "Medak", "Nalgonda", "Nizamabad", "K.V.Rangareddy", "Warangal"]

for di in districts:
    try:
        admin = pinCodes.query.filter_by(district=di).all()
        for a in admin:
            print a.state
            a.state = "TELANGANA"
            db.session.commit()
            print("Commited")

    except:
        pass

print("Finished")