from myLib.fiware import Fiware

upv=Fiware(printInfo=True)
#upv.filter(type='door')


le=upv.deleteEntityById(entity_id='urn:ngsi-ld:joamona:door:p3')
