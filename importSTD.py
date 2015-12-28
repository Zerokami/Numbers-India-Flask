import csv
from flask_hello_world_app import db, STDcodes

f = open("Std.csv")
csv_f = csv.reader(f)

db.create_all()

i = 0

for row in csv_f:
    STDcode = STDcodes(stdcode=int(row[0]), city= row[1], state=row[2])
    db.session.add(STDcode)
    db.session.commit()
    print(i)
    i += 1


f.close() 
