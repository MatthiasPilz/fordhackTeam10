# python for interpreting the json response
import json

with open('camdenFeatures.txt') as json_file:
    data = json.load(json_file)

    count = 0
    result = [0]*580
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

    print(result)

    f = open("camdenParkingBays.txt", "w+")
    for i in range(len(result)):
        f.write(str(i) + ' ' + str(result[i]) + "\n")
    f.close()
