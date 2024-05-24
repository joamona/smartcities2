from myLib.readCsv import ReadCsv

fileName='c:/gescont/smartcities/upv_access_points.csv'
csv=ReadCsv(csvFileName=fileName, csvSeparator=',', csvHasHeader=True)
csv.printConfig()
csv.printData()