from myLib.fiware import Fiware

upv=Fiware(printInfo=True)
#upv.filter(type='door')


le=upv.filter(fieldsValuesDict={"username":"joamona","strength":500})
