from myLib.fiware import Fiware

upv=Fiware()

attributes={
            "color": {
                "type": "Text",
                "value": "black"
            },
            "strength": {
                "type": "Number",
                "value": 200
            }
        }

upv.createEntity(etype='door',ename='main',attributes=attributes)