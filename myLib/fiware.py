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