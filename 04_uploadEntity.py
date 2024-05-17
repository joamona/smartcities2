from myLib.fiware import Fiware

upv=Fiware()

attributes1={
            "color": {
                "type": "Text",
                "value": "black"
            },
            "strength": {
                "type": "Number",
                "value": 200
            }
        }

attributes2={
            "color": {
                "type": "Text",
                "value": "white"
            },
            "strength": {
                "type": "Number",
                "value": 400
            }
        }

attributes3={
            "color": {
                "type": "Text",
                "value": "red"
            },
            "strength": {
                "type": "Number",
                "value": 500
            }
        }

e1=upv.createEntity(etype='door',ename='p1',attributes=attributes1)
e2=upv.createEntity(etype='door',ename='p2',attributes=attributes2)
e3=upv.createEntity(etype='door',ename='p3',attributes=attributes3)

upv.uploadEntity(entity=e1)
print("********")
upv.uploadEntity(entity=e2)
print("********")
upv.uploadEntity(entity=e3)

