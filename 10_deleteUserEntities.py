from myLib.fiware import Fiware

upv=Fiware(printInfo=True)
#upv.filter(type='door')
le=upv.deleteAllEntitiesOfUser(username='joamona')
