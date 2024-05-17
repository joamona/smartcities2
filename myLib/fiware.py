import requests, folium, json
from myLib import fiwareSettings

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