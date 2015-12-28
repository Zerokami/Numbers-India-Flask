import csv


f = open('Std.csv')

csv_f = csv.reader(f)

for row in csv_f:
	print row[2]