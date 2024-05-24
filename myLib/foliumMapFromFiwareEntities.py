'''
Created on 24 jul 2023

@author: joamona
'''

'''
Created on 24 jul 2023

@author: joamona
'''
import os
import json
import webbrowser

import folium
from folium.plugins import MousePosition

from myLib.fiware import Fiware
from myLib.readCsv import ReadCsv
from myLib.fiwareAnswer import FiwareAnswer

class FoliumMapFromFiwareEntities():
    upv: Fiware = None
    etype:str = None
    htmlFileName: str = None
    def __init__(self,etype):
        self.etype=etype
        self.htmlFileName=etype + '.html'
        self.upv=Fiware()
        self._createmap()
        
    def _createmap(self):
        print("Creating folium map")
        #fa:FiwareAnswer=self.upv.filterByUserAndProperties(etype=self.etype)
        fa:FiwareAnswer=self.upv.filter(type=self.etype)
        osmLayer=folium.FeatureGroup(name='osm')
        le=fa.resultingEntities
        for entity in le:
            print(f'Creating map marker for entity: {entity["id"]}')
            if 'location' not in entity.keys():
                print("No location in entity keys")
                continue
            longitude, latitude = entity['location']['value']['coordinates']
            
            #popup
            markerAttributes=f'<p><b>ID: {entity["id"]}</b></p> <p><b>Type: {entity["type"]}</b><p>'
            popup=folium.Popup(markerAttributes, max_width=500)
            #marker
            marker=folium.CircleMarker(
                location=[latitude, longitude],
                radius=10,
                fill=True,
                fill_opacity=0.4,
                popup=popup
                )
            osmLayer.add_child(child=marker)
        #create the map
        osmMap = folium.Map(location=[39.48,-0.34], zoom_start=16)
        osmMap.add_child(osmLayer)
        
        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    
        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(osmMap)
        
        #show the folium map
        osmMap.save(outfile=self.htmlFileName)
        
    def openBrowser(self):
        webbrowser.open(url=os.path.abspath(path=self.htmlFileName))#the method open needs the absolute path to the field
