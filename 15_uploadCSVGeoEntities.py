from myLib.readCsv import ReadCsv
from myLib.fiware import Fiware
fileName='c:/gescont/smartcities/upv_access_points.csv'
csv=ReadCsv(csvFileName=fileName, csvSeparator=',', csvHasHeader=True)
csv.printConfig()
csv.printData()

upv=Fiware()
le=upv.createCsvEntities(etype='door',
                      csvData=csv.csvData,
                      csvHeader=csv.csvHeader)
upv.uploadListOfEntities(le)


