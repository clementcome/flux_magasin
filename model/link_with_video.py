import json
from model import builder

def build_from_video():
    with open("..//data//positions.txt", "r") as inputfile:
        data = json.load(inputfile)
    print(data['polygon_points'])
    Shop = builder(data["polygon_points"],1,[])
#COmpute RMS
