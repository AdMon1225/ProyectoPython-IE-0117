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
