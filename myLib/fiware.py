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
        if self.printInfo:
            print("Fiware.uploadEntity")
            fa=FiwareAnswer(answer=self.requesResult,printInfo=self.
            printInfo,entity=entity)
        
        return fa