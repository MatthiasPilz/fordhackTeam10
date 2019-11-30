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

                    result[count] = temp
                    count += 1

        return(result)

# ######################################################################################################################


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

# ######################################################################################################################


def simplify_parkingBays( bays ):
    result = []

    for cord1, cord2 in bays:
        avgx = 0.5*( cord1[0] + cord2[0] )
        avgy = 0.5*( cord1[1] + cord2[1] )
        result.append([avgx, avgy])

    return result

# ######################################################################################################################


def calc_distance(i, j):
    return (great_circle(i,j).km*1000)

# ######################################################################################################################


def calc_scoreOfLamps( lamps, bays ):
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

# ######################################################################################################################


def load_crimeData(filename):
    d = {}
    d['violent-crime'] = 5
    d['other-crime'] = 0
    d['burglary'] = 0
    d['drugs'] = 2
    d['anti-social-behaviour'] = 1
    d['criminal-damage-arson'] = 4
    d['possession-of-weapons'] = 5
    d['public-order'] = 1
    d['bicycle-theft'] = 0
    d['other-theft'] = 0
    d['shoplifting'] = 0
    d['theft-from-the-person'] = 0
    d['vehicle-crime'] = 4
    d['robbery'] = 5

    result = []
    with open(filename) as json_file:
        data = json.load(json_file)

        for line in data:
            x = float(line['latitude'])
            y = float(line['longitude'])
            t = int(d[line['category']])
            result.append( [x,y,t] )

    return result

# ######################################################################################################################


def calc_scoreOfCrime(crime, bays):
    countList = []
    crimeRadius = 50

    for i in bays:
        count = 0
        for j in crime:
            dist = calc_distance(i, [j[0],j[1]])
            if (dist < crimeRadius):
                count += j[2]

        countList.append(count)

    maximum = max(countList)
    result = []
    for i in range(len(countList)):
        result.append(countList[i] / maximum)

    return result

# ######################################################################################################################


def write_file( table, name ):
    f = open(name, "w+")
    for i in range(len(table)):
        f.write(str(i) + ' ' + str(table[i]) + "\n")
    f.close()

# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################


if __name__ == "__main__":
    #lamps = load_lampData("lamp_position.txt")

    bays = simplify_parkingBays( create_parkingBays("camdenFeatures.txt") )
    crime = load_crimeData("crimeTypeByLocation.txt")
    crimeScore = calc_scoreOfCrime( crime, bays )

    result = []
    for i in range(len(bays)):
        temp = [bays[i], crimeScore[i]]
        result.append( temp )

    write_file( result, "crimeScoring.txt" )


    #score = calc_scoreOfLamps(lamps, bays)