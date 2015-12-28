import csv
from flask_hello_world_app import db, pinCodes

f = open("all_india_pin_code.csv")
csv_f = csv.reader(f)

db.create_all()

i = 0

for row in csv_f:
    pinCode = pinCodes(officename=row[0], pincode= int(row[1]), taluk=row[7], district = row[8], state=row[9])
    db.session.add(pinCode)
    db.session.commit()
    print(i)
    i += 1


f.close() 
