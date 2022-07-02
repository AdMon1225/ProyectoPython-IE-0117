def createBoard(rows, columns):
    tablero = []
    for i in range(rows):
        fila = []
        for n in range(columns):
            fila.append(0)
        tablero.append(fila)
    return tablero

def createAnts(numberAnts,rows,columns):
    hormigas = []
    if numberAnts == 1:
        hormiga = []
        hormiga.append(int(rows/2))
        hormiga.append(int(columns/2))
        hormiga.append(0)
        hormigas.append(hormiga)
        return hormigas

def conseguir_giro(hormiga,tablero,reglas):
    fila = hormiga[0]
    columna = hormiga[1]
    estado = tablero[fila][columna]
    if estado>=len(reglas):
        estado=0
        letra = reglas[estado]
        return letra
    else:
        letra = reglas[estado]
        return letra 
    
def girar(hormiga,direccionGiro):
    if direccionGiro=="L":
        if hormiga[2]==0:
            hormiga[2]=3
        else:
            hormiga[2]-=1
    elif direccionGiro=="R":
        if hormiga[2]==3:
            hormiga[2]=0
        else:
            hormiga[2]+=1
    elif direccionGiro=="U":
        if hormiga[2]==0 or hormiga[2]==1:
            hormiga[2]+=2
        else:
            hormiga[2]-=2
     
def pintar(hormiga,tablero,reglas):
     fila = hormiga[0]
     columna = hormiga[1]
     estado = tablero[fila][columna]
     if estado == len(reglas)-1:
         tablero[fila][columna]=0  
     else:
         tablero[fila][columna]+=1
 
def avanzar(hormiga,tablero):
    if hormiga[2]==0:
        hormiga[1]+=1
        fila = hormiga[0]
        if hormiga[1]>=len(tablero[fila]):
            hormiga[1]=0
    elif hormiga[2]==3:
        hormiga[0]-=1
        if hormiga[0]<0:
            hormiga[0]=len(tablero[0])-1
    elif hormiga[2]==2:
        hormiga[1]-=1
        fila = hormiga[0]
        if hormiga[1]<0:
            hormiga[1]=len(tablero[fila])-1  
    elif hormiga[2]==1:
        hormiga[0]+=1
        if hormiga[0]>=len(tablero[0]):
            hormiga[0]=0
    print(hormiga)

def takeStep(board,ants,antRules):
    for i in ants:
        print(conseguir_giro(i,board,antRules))
        girar(i,conseguir_giro(i,board,antRules))
        pintar(i,board,antRules)
        avanzar(i,board)
