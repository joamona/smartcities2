import requests, folium, json
from myLib import fiwareSettings
from myLib.fiwareAnswer import FiwareAnswer

class Fiware():
    def __init__(self, url=fiwareSettings.SERVER_URL, 
                 user=fiwareSettings.USERNAME, 
                 printInfo=True):
        #attributes
        self.url=url
        self.user=user
        self.entities = "/v2/entities"
        self.urlEntities=self.url + self.entities
        self.headers={"Content-Type": "application/json"}
        self.requesResult = None
        self.printInfo=printInfo
        if self.printInfo:
            print("Fiware class. __init__")
            print(f"Url para las entidades: {self.urlEntities}")
            print(f"Usuario: {self.user}")


    def printDict(self,d):
        if self.printInfo:
            print("Fiware class. printDict")
        print(json.dumps(d, indent=4))
        
    def printListOfDicts(self,l):
        if self.printInfo:
            print("Fiware class. printListOfDicts")        
        for d in l:
            self.printDict(d) 
            
    def getVersion(self):
        url=self.url + "/version"
        res = requests.get(url)
        r=json.dumps(res.json(), indent=4)
        if self.printInfo:
            print("Fiware class.getVersion")
            print(f"Request url: {url}")
            print(r)
        return r

    def createUrn(self,etype,ename):
        urn = f"urn:ngsi-ld:{self.user}:{etype}:{ename}"
        if self.printInfo:
            print("Fiware class. createUrn")
            print(f"urn: {urn}")
        return urn

    def createEntity(self, etype, ename, attributes={}):
        """
        Atributes should be in the format:
        {
            "accuracy": {
                "type": "Float",
                "value": 3.0
            },
            "date": {
                "type": "Text",
                "value": "2019-04-15 09:21:20"
            }
        }
        """
        payload={
            "id": self.createUrn(etype, ename),
            "type":etype,
            "name":{
                "type":"Text",
                "value":ename
                },
            "username":{
                "type":"Text",
                "value":self.user
                }
            }

        for key, value in attributes.items():
            payload[key]=value
            
        entity={
            "type":etype,
            "name":ename,
            "payload":payload
            }
        if self.printInfo:
            print("Fiware.createEntity")
            print(json.dumps(entity, indent=4))
        
        return entity
    
    def uploadEntity(self, entity):
        """
        Fijate que lo que se sube e el payload del diccionario.
        No todo el diccionario.
        """
        self.requesResult=requests.post(
            self.urlEntities,
            headers=self.headers,
            data=json.dumps(entity["payload"])
        )

        fa=FiwareAnswer(answer=self.requesResult,printInfo=self.
            printInfo,entity=entity)
        
        return fa
    def uploadListOfEntities(self,l):
        lStatus=[]
        n=len(l)
        for i in range(len(l)):
            print(f"Uploading entity: {i} of {n}")
            fa=self.uploadEntity(l[i])
            lStatus.append(fa)
        return lStatus
    
    def getEntityById(self,entity_id):
        if self.printInfo:
            print("Fivare.getEntityById")
        url=self.urlEntities + "/" + entity_id
        self.requesResult=requests.get(url)
        return FiwareAnswer(answer=self.requesResult, printInfo=self.printInfo)
    
    def filter(self, idPattern=None, type=None, name=None, fieldsValuesDict=None, limit=1000)->FiwareAnswer:
        """
        This method gets all entities that match with all conditions.
        Makes several interation requests to get 1000 entities,
        and join them in one result.
        Parameters:
            idPattern: search in the id the text idPattern. Can be used to get all entities of a user
            etype: filter by entity type
            fieldsValuesDict: dict key:value to filter
            limit: limit of entities of each iteration
        """
        if idPattern is not None:
            parameters = {
                "idPattern": idPattern,
                "offset": 0,
            }
        else:
            parameters={}
        
        if limit is not None:
            parameters["limit"] = limit

        if type is not None:
            parameters["type"] = type

        if name is not None:
            if fieldsValuesDict is not None:
                fieldsValuesDict["name"]=name
            else:
                fieldsValuesDict={}
                fieldsValuesDict["name"]=name

        if fieldsValuesDict is not None and isinstance(fieldsValuesDict, dict):
            print(fieldsValuesDict)
            q=""
            for key, value in fieldsValuesDict.items():
                print(key,value)
                #ejemplo: q=temperature<24;humidity==75..90;status==running
                q=q+f"{key}=={value};"
                
            
            q=q[:-1]#quita el último;
            parameters["q"] = q

        if self.printInfo:
            print("Fiware.filterByUserAndProperties.Current parameters:")
            print(parameters.items())
        
        page = 0
        entities = []
        while True:
            if self.printInfo:
                print(f"Iteración: {page + 1}")
            response = requests.get(self.urlEntities, params=parameters)
            if len(response.json()) == 0:
                break
            fa:FiwareAnswer=FiwareAnswer(answer=response,printInfo=self.printInfo)
            entities += response.json()

            if len(response.json()) <= limit:
                break
            page += 1
            parameters["offset"] = page * limit
        fa=FiwareAnswer(answer=response, printInfo=self.printInfo)
        fa.setResultingEntities(resultingEntities=entities)
        return fa


    def deleteEntityById(self,entity_id):
        """
        There is not a feature in Fiware to delete several entities at once
        It is necessary select them and remove them one by one
        """
        url = self.urlEntities + "/" + entity_id
        if self.printInfo:
            print("Fiware.deleteEntityById")
            print(f"Deleting entity {url}")
        
        self.requesResult=requests.delete(url)
        fa:FiwareAnswer=FiwareAnswer(self.requesResult,printInfo=self.printInfo)
        return fa
    
    def deleteAllEntitiesOfUser(self, username):
        if self.printInfo:
            print(f"Fiware.deleteAllEntitiesOfUser. Username: {username}")
        fa1:FiwareAnswer=self.filter(fieldsValuesDict={"username":username})
        n=len(fa1.resultingEntities)
        results:[FiwareAnswer]=[]
        for i in range(n):
            if self.printInfo:
                print(f"Deleting entity {i+1} of {n}")
            en=fa1.resultingEntities[i]
            #pay attention. Here the payload field is not
            #when you upload an entity you get the id as en["payload"]["id"]
            #but when you download an entity you simply use en["id"]
            fa:FiwareAnswer=self.deleteEntityById(en["id"])
            fa.entity=en
            results.append(fa)

    def createGeoEntity(self, etype, ename, coordinates, attributes={}):
        #coordinates=[longitude, latitude]
        
        payload={
            "id":self.createUrn(etype, ename),
            "type":etype,
            "name":{
                "type":"text",
                "value":ename
                },
            "username":{
                "type":"Text",
                "value":self.user
                },
            "location":{
                "type":"geo:json",
                "value":{
                    "type":"Point",
                    "coordinates":coordinates
                    }
                }
            }
        for key, value in attributes.items():
            payload[key]=value
        
        entity={
            "type":etype,
            "name":ename,
            "payload":payload
        }

        if self.printInfo:
            print("Fiware class. createGeoEntity")
            print(json.dumps(entity, indent=4))
        return entity
    
    def createCsvEntities(self, etype, csvData:list, csvHeader:list):
        #csvData es una lista de listas 
        #csv header is: ["PID", "LONGITUDE", "LATITUDE", "ACCURACY", "DATE"]
        #ename es PID
        
        specialFields=["PID", "LONGITUDE", "LATITUDE"]
        
        csvEntities=[]
        for record in csvData:
            attributes={}
            for index, fieldName in enumerate(csvHeader):
                if not fieldName in specialFields:
                    value=record[index]
                    if isinstance(value, float):
                        attributes[fieldName.lower()]={
                            "type": "Float",
                            "value": value
                            }
                    elif isinstance(value, int):
                        attributes[fieldName.lower()]={
                            "type": "Integer",
                            "value": value
                            }
                    else:
                        attributes[fieldName.lower()]={
                            "type": "Text",
                            "value": value
                            }   
            geoEntity=self.createGeoEntity(etype=etype, 
                                           ename=record[0], 
                                           coordinates=[record[1],record[2]],
                                           attributes=attributes)
    
            csvEntities.append(geoEntity)
            if self.printInfo:
                self.printListOfDicts(csvEntities)
        return csvEntities

