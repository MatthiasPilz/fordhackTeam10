# python for interpreting the json response
import json

with open('example.txt') as json_file:
    data = json.load(json_file)

    for feature in data['features']:
        prop = feature['properties']
        reg = prop['regulations']
        if ( reg[0]['rule']['payment'] ):
            if ( reg[0]['payment'] ):
                pay = reg[0]['payment']
                print(pay['methods'])


