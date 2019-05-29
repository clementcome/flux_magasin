with open("..//..//data//positions.txt", "r") as inputfile:
    data = json.load(inputfile)
print(type(data))
Shop = builder(data["polygon_points"],1,[])
#COmpute RMS
