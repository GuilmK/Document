import csv
csvFile = open("instance.csv", "r")
reader = csv.reader(csvFile)
for item in reader:
    print(item) # >>> ['name', 'score']
                # >>> ['Zhang', '100']
                # >>> ['Wang', '80']
                # >>> ['Li', '90']