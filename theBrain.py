# python for interpreting the json response
import json
from geopy.distance import great_circle

def create_parkingBays(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

        count = 0
        result = [0]*576
        for feature in data['features']:
            prop = feature['properties']
            reg = prop['regulations']

            if ( reg[0]['rule']['payment'] ):
                if ( reg[0]['payment'] ):
                    pay = reg[0]['payment']
                    geo = feature['geometry']['coordinates']

                    temp = []
                    temp.append([geo[0][1], geo[0][0]])
                    temp.append([geo[1][1], geo[1][0]])

                    #result[count] = [geo[0][1], geo[0][0]]
                    #result[count].append([geo[1][1], geo[1][0]])
                    result[count] = temp
                    count += 1

        return(result)
    '''
        f = open("camdenParkingBays.txt", "w+")
        for i in range(len(result)):
            f.write(str(i) + ' ' + str(result[i]) + "\n")
        f.close()
        
        f = open("camdenParkingBaysCenters.txt", "w+")
        for i in range(len(bays)):
            f.write(str(i) + ' ' + str(bays[i]) + "\n")
        f.close()
    '''

def load_lampData(filename):
    data = open(filename, 'r')

    lamps = []
    for i in data:
        cord1, cord2 = i.split(', ')
        x = float(cord1)
        y = float(cord2)
        #lamps.append([x,y])
        lamps.append([y,x])

    data.close()
    return lamps

def simplify_parkingBays( bays ):
    result = []

    for cord1, cord2 in bays:
        avgx = 0.5*( cord1[0] + cord2[0] )
        avgy = 0.5*( cord1[1] + cord2[1] )
        result.append([avgx, avgy])

    return result

def calc_distance(i, j):
    #dist = ( (i[0]-i[1])^2 + (j[0]-j[1])^2 )**(0.5)
    #return dist*11000
    return (great_circle(i,j).km*1000)


def calc_scoreOfBay( lamps, bays ):
    countList = []
    r = 50
    for i in bays:
        #print(i)
        count = 0
        for j in lamps:
            dist = calc_distance(i,j)
            if( dist < r ):
                count += 1

        countList.append(count)

    maximum = max(countList)
    result = []
    for i in range(len(countList)):
        result.append(countList[i]/maximum)

    return result



if __name__ == "__main__":
    lamps = load_lampData("lamp_position.txt")
    bays = simplify_parkingBays( create_parkingBays("camdenFeatures.txt") )

    score = calc_scoreOfBay(lamps, bays)