import csv
from flask_hello_world_app import db, mobileNumbers

f = open("mobileNumbers.csv")
csv_f = csv.reader(f)

db.create_all()

i = 0

for row in csv_f:
    mobileNumber = mobileNumbers(number = int(row[0]), operator = row[1], state = row[2], icon = int(row[3]))
    db.session.add(mobileNumber)
    db.session.commit()
    print(i)
    i += 1


f.close() 
