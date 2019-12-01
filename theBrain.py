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

                    # more potential information:
                    maxStay = reg[0]['rule']['maxStay'] #--> classify!?
                    pricePerHour = pay['rates'][0]['fees'][0] / pay['rates'][0]['durations'][0] * 60
                    #method = pay['methods']
                    try:
                        url = prop['images'][0]
                    except:
                        url = ""

                    timeFrom = reg[0]['timeSpans'][0]['timesOfDay']['from']
                    timeTo = reg[0]['timeSpans'][0]['timesOfDay']['to']

                    # create entry
                    temp = []
                    # parking bay number
                    temp.append(count)

                    # parking bay location
                    avgx = 0.5*( geo[0][1] + geo[1][1] )
                    avgy = 0.5*( geo[0][0] + geo[1][0] )
                    #temp.append([geo[0][1], geo[0][0]])
                    #temp.append([geo[1][1], geo[1][0]])
                    temp.append([avgx, avgy])

                    # long or short maxStay time
                    if ( maxStay <= 60 ):
                        temp.append('short')
                    else:
                        temp.append('long')

                    # price per hour
                    temp.append(pricePerHour)

                    # url to images
                    temp.append(url)

                    # time morning or not
                    if ( timeTo <= "13:30" ):
                        timeSpan = 'morning'
                    else:
                        timeSpan = 'allDay'
                    temp.append(timeSpan)

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

    for _, cord1, cord2, _, _, _, _ in bays:
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
    crimeRadius = 70

    for i in bays:
        count = 0
        for j in crime:
            dist = calc_distance([i[1][0], i[1][1]], [j[0],j[1]])
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
        f.write(str(table[i]) + "\n")
    f.close()

# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################


if __name__ == "__main__":
    #lamps = load_lampData("lamp_position.txt")
    bays = create_parkingBays("camdenFeatures.txt")


    #bays = simplify_parkingBays( create_parkingBays("camdenFeatures.txt") )
    #write_file( bays, "baysTest.txt" )

    crime = load_crimeData("crimeTypeByLocation.txt")
    crimeScore = calc_scoreOfCrime( crime, bays )

    result = []
    for i in range(len(bays)):
        #temp = [bays[i], crimeScore[i]]
        temp = [bays[i]]
        temp.append(crimeScore[i])
        result.append( temp )
        #result.append(bays[i], crimeScore[i])

    write_file( result, "crimeScoringNEW_70.txt" )


    #score = calc_scoreOfLamps(lamps, bays)
