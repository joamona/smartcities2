"""
Created on 21 jul 2023

@author: joamona
"""
import json

class FiwareAnswer():
    answer=None
    url=None
    totalCount=None#número de registros totales que hay en fiware, pero que no recupera todos
            #Solo recupera 1000, de los cuales luego puedes filtrar por usuario
            #con lo que del usuario puede que saques 10, pero hay 100,
            #eso es porque recuperó 1000, y los del usuario empiezan en el 990
            #Nota:
            #   Resulta mejor añadir una propiedad, llamada usuario,  y filtrar por ella.
    retrievedEntitiesCount=None
    status = None
    resultingEntities= None
    message=None
    typeOfResultingEntities=None  #puede ser list o dict
    entity=None
    
    def __init__(self, answer, printInfo=True, entity=None):
        if printInfo:
            print("FiwareAnswer. __init__")
        
        self.url=answer.url
        self.answer=answer
        self.status=answer.status_code    
        self.message = answer.text
        self.prinInfo =printInfo

        if entity is not None:
            self.entity=entity
        try:
            self.count = int(answer.headers["Fiware-Total-Count"])
        except:
            pass 
        self.status=answer.status_code      
        try:
            resultingEntities=answer.json()
            self.setResultingEntities(resultingEntities)
        except:
            pass 
        
        if printInfo:
            self.printRequestAnswer()
    
    def printRequestAnswer(self):
        print("FiwareAnswer.printRequestAnswer")
        self.printResultingEntities()
        print(f"status: {self.status}")
        print(f"totalCount: {self.totalCount}")
        print(f"retrievedEntitiesCount: {self.retrievedEntitiesCount}")
        print(f"url: {self.url}")
        print(f"message: {self.message}")
        if self.entity is not None:
            print("Entity: ")
            self._printDict(d=self.entity)

    def printResultingEntities(self):
        print("FiwareAnswer.printResultingEntities")
        if self.typeOfResultingEntities=="dict":
            self._printDict(self.resultingEntities)
        if self.typeOfResultingEntities=="list":
            self._printListOfDicts(self.resultingEntities)
            
    def _printDict(self,d):
        print(json.dumps(d, indent=4))
    
    def _printListOfDicts(self, l):
        for d in l:
            self._printDict(d) 

    def setEntity(self,entity):
        if self.prinInfo:
            print("FiwareAnswer.setEntity")
        self.entity=entity
            
    def setResultingEntities(self, resultingEntities):
        if self.prinInfo:
            print("FiwareAnswer.setResultingEntities")
        self.resultingEntities=resultingEntities
        if isinstance(self.resultingEntities, list):
            self.retrievedEntitiesCount=len(self.resultingEntities)
            self.typeOfResultingEntities="list"
        elif isinstance(self.resultingEntities, dict):
            self.retrievedEntitiesCount=1
            self.typeOfResultingEntities="dict"
