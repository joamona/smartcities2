from myLib.fiware import Fiware

upv=Fiware()

upv=Fiware(url='Http://OtroServidor.com',user='perico')

print("False")
upv=Fiware(printInfo=False)
print("Terminado")
