from myLib.fiware import Fiware
upv=Fiware()
e=upv.createGeoEntity(etype='door', ename='emergency', 
                    coordinates=[-0.34722055,39.4831925])
upv.uploadEntity(e)