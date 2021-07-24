import random

#La duración del juego está determinada por el tamaño del tablero(4x4, 8x8, 12x12)
CORTO = 4
MEDIO = 8
LARGO = 12

#Teclas para las opciones
NUEVA_PARTIDA = 1
CONFIGURACION = 2
PUNTUACIONES = 3
SALIR = 4


#Funciones de interfaz
def mostrar_menu_principal() -> None:
    '''
    Muestra al usuario las opciones posibles a elegir
    '''
    
    print("Menu de opciones:")
    print(" 1- Nueva partida\n 2- Cambiar opciones\n 3- Puntuaciones\n 4- Salir\n")

def mostrar_puntuaciones(ganadores : list) -> None:
    '''
    Muestra en pantalla las ultimas 4 partidas ordenadas por quien ganó más
    indicando nombre, victorias y cantidad de partidas respectivamente
    PRE: ganadores debe ser una lista de 4 elementos y cada uno debe contener
    3 elementos los cuales indican el nombre las veces que gano y las veces
    que jugaron los ultimos 4 ganadores
    POST: la lista se mostrara ordenada por las veces en que gano cada jugador
    '''
    print(sorted(ganadores, key=lambda veces_gano: veces_gano[1]))

def mostrar_menu_config(prob_comodines : dict, duracion : int) -> None:
    '''
    PRE: prob_comodines debe contener claves con los nombres de los comodines
    y valores con sus probabilidades
    POST: Muestra en pantalla los parametros actuales del juego
    '''
    print("\nParámetros actuales del juego\n")    
    print(f"Probabilidad de comodines: {prob_comodines}\n")
    print(f"Tamaño tablero : {duracion}\n (Indica la cantidad de filas y columnas)")

#Funciones de juego
def hay_ganador(juego) -> tuple:
    '''
    Recibe el estado de juego actual y devuelve una tupla con un booleano
    que indica si el juego esta terminado o no como primero elemento y su
    nombre como segundo elemento
    
    PRE: juego debe ser un iterable de 2 elementos con 2 diccionarios que contengan
    los datos de los jugadores. Los diccionaros deben incluir las claves "Tablero",
    "Fichas encontradas" y "Nombre". Estos deben tener como valor una matriz, una lista
    y un string respectivamente
    POST: la tupla tendra como elemento True, ganador["Nombre"] si hay un ganador
    o False, "" si no lo hay
    '''
    jugador1, jugador2 = juego
    nombre_ganador = ""
    fichas_totales = (len(jugador1["Tablero"])**2) //2
    
    if fichas_totales == len(jugador1["Fichas encontradas"]):
        nombre_ganador = jugador1["Nombre"]

    elif fichas_totales == len(jugador2["Fichas encontradas"]):    
        nombre_ganador = jugador2["Nombre"]

    return bool(nombre_ganador), nombre_ganador

def agregar_ganador(ultimo_ganador : str, ganadores : list) -> None:
    '''
    PRE: ultimo_ganador debe ser una cadena con el nombre del ganador
    del ultimo juego y ganadores una lista de listas con 3 elementos
    donde cada uno indica el nombre, las veces que jugo y cuantas veces
    gano respectivamente
    POST: Agrega a la lista ganadores la lista [ultimo_ganador, 1, 1] si 
    ultimo_ganador no se encontraba en ella, sino se le suma una victoria y 
    una partida jugada
    '''

    for i in range(len(ganadores)):
        if ganadores[i][0] == ultimo_ganador:
            ganadores[i][1] += 1
            ganadores[i][2] += 1
     
    if len(ganadores) == 4:
        ganadores.pop(-1)

    ganadores.append([ultimo_ganador, 1, 1])
    
def crear_tablero(dimensiones : int) -> list:
    '''
    PRE: dimensiones debe ser un entero que indique las dimensiones del tablero
    POST: Devuelve el tablero en forma de matriz con las fichas 
    distribuidas de manera random
    '''
    tablero = []
    fichas = [i for i in range((dimensiones**2) //2)] *2
    random.shuffle(fichas)
       
    for i in range(0, len(fichas), dimensiones):  #Step necesario en el range para que no se repitan fichas i=0,4,8,12
        tablero.append(fichas[i:i + dimensiones]) #i:i + dimensiones hace que agregue filas al tablero con dimensiones elementos

    return tablero

def crear_partida(duracion : int, jugadores : list) -> tuple:
    '''
    Inicializa el estado del juego.
    PRE: duracion debe ser un entero == CORTO MEDIO o LARGO 
    el cual indica la duracion del juego
    jugadores debe ser una lista de 2 strings con los nombres del jugador 1 y el 2
    POST: Devuelve dos diccionarios empaquetados, 
    uno para cada jugador con "Nombre", "Tablero", "Fichas encontradas" y
    "Comodines" como keys.
    '''

    return {
        "Nombre": jugadores[0],
        "Tablero": crear_tablero(duracion),
        "Comodines": {},
        "Fichas encontradas": []
        }, {
        "Nombre": jugadores[1],
        "Tablero": crear_tablero(duracion),
        "Comodines": {},
        "Fichas encontradas": []
    }

def usar_comodin(comodin : str, jugador : dict) -> None:
    '''
    PRE: Recibe una cadena con el nombre del comodin deseado 
    y los datos del jugador que lo usará
    POST: Aplica el comodin en los datos del jugador recibido
    '''
    if comodin == "Fatality":
        jugador["Tablero"] = fatality(jugador["Tablero"])
    
    elif comodin == "Toti":
        jugador["Tablero"] = toti(jugador["Tablero"])
    
    elif comodin == "Layout":
        layout(jugador["Tablero"])
    
    else:
        replay(jugador)

    print(f"Usaste tu comodín {comodin} con éxito")
    jugador["Comodines"][comodin] -= 1

def comprobar_comodines(jugador : dict) -> None:
    '''
    PRE: Recibe un diccionario con los datos del jugador y evalua si quiere 
    y puede usar un comodin. El diccionario debe contener las keys "Comodines" y
    "Tablero"
    
    POST: En caso de que pueda, el comodin es aplicado a su tablero sino printea
    que no tiene comodines disponibles
    '''
    
    if jugador["Comodines"]:
        desea_usar = input("Deseas usar un comodin?\nSi: Escribe si\nNo: ENTER\n")           
        
        if desea_usar:
            comodin_deseado = input(f"Qué comodin deseas usar?\n").capitalize()
            while comodin_deseado not in jugador["Comodines"]:
                comodin_deseado = input(f"No te quedan mas {comodin_deseado}, elige otro comodin\n")
            
            usar_comodin(comodin_deseado, jugador)
    
    else:
        print("No tenes comodines disponibles")

def dado_comodin(prob_comodines : dict) -> str:
    '''
    PRE: prob_comodines será un diccionario con el nombre de los comodines
    como claves y enteros referentes a sus probabilidades como valores.
    POST: Devuelve una cadena con el nombre del comodin si se obtuvo uno
    '''
    for comodin, probabilidad in prob_comodines.items():
        if random.randint(1,100) in range(1, probabilidad):
            return comodin

def posiciones_validas(coordenadas : tuple, tablero : list) -> bool:
    '''
    PRE: coordenadas es una tupla de iterables con elementos enteros y tablero una matriz 
    POST: Devuelve en booleano si las coordenadas se encuentran dentro del rango
    de la matriz
    '''
    validas = True

    for coordenada in coordenadas:
        x, y = coordenada
        
        if x < 0 or x > len(tablero[0]):
            validas = not validas
        elif y < 0 or y > len(tablero):
            validas = not validas

    return validas

def jugar_dado(jugador_actual : dict, prob_comodines : dict) -> None:
    '''
    Tira el dado y si saca comodin, da la opcion al usuario de guardarlo o jugarlo.

    PRE: Recibe un diccionario con los datos del jugador actual 
    y otro con las probabiliadades de los comodines. jugador_actual
    debe contener las claves "Comodines" y "Tablero"
    POST: En caso de querer jugarlo, el comodin es aplicado a su tablero, sino se suma a sus comodines.
    Si no saco comodin al tirar el dado la funcion imprime lo sucedido
    '''

    print("Tirando dado...")
    comodin = dado_comodin(prob_comodines)
    
    if comodin:
        print(f"Qué suerte! Sacaste el comodín {comodin}")
        desea_usarlo = input("Deseas usarlo? En caso de que no el comodín se guardará\nSi: Escribe si\nNo: ENTER\n")
        
        if comodin not in jugador_actual["Comodines"]:
            jugador_actual["Comodines"][comodin] = 1
        else:
            jugador_actual["Comodines"][comodin] += 1 
        if desea_usarlo:
            usar_comodin(comodin, jugador_actual)
    
    else:
        print("Mala suerte, no sacaste comodín")

def mostrar_tablero_oculto(tablero : list, fichas_descubiertas : list) -> None:
    '''
    PRE: tablero es una matriz perteneciente al jugador A y fichas descubiertas una lista de enteros
    con las fichas descubiertas por el jugador B
    POST: imprime una copia del tablero recibido pero mostrando "?" en las fichas que aun no
    se descubrieron
    '''
    tablero_oculto = tablero.copy() 

    for y in range(len(tablero_oculto)):    
        for x in range(len(tablero_oculto[y])):
            if tablero[y][x] not in fichas_descubiertas:
                tablero_oculto[y][x] = "?"

    print(f"Tablero del jugador contrario\n{tablero_oculto}")

def avanzar(juego : tuple, turno_jugador1 : bool) -> tuple:
    '''
    Avanza con el estado del juego pidiendo y validando posiciones al usuario
    y mostrando tableros ocultos
    PRE: juego debe ser una tupla de dos diccionarios con los datos
    de ambos jugadores y turno_jugador1 un booleano que indique
    si es el turno del jugador 1 o no
    POST: Retorna los diccionarios con los datos de los jugadores empaquetados
    en una tupla. En caso de que el jugador actual haya encontrado un par de fichas,
    se le agregara a la lista "Fichas encontradas" el entero correspondiente al par
    encontrado y se creara la clave "Replay" indicando que el proximo turno sera el suyo
    '''
    jugador1, jugador2 = juego
    
    x1, y1 = input("Introduce la fila y columna separadas por una coma\nFicha 1: ").split(",")
    x2, y2 = input("Ficha 2: ").split(",")

    coordenada1 = (int(x1), int(y1))
    coordenada2 = (int(x2), int(y2))
    
    while not posiciones_validas((coordenada1, coordenada2), jugador1["Tablero"]):
        print("Coordenadas invalidas, volve a intentar")
        x1, y1 = input("Ficha 1: ").split(",")
        x2, y2 = input("Ficha 2: ").split(",")

        coordenada1 = (int(x1), int(y1))
        coordenada2 = (int(x2), int(y2))
    
    if turno_jugador1:
        ficha1 = jugador2["Tablero"][coordenada1[1]][coordenada1[0]]
        ficha2 = jugador2["Tablero"][coordenada2[1]][coordenada2[0]]
        print(f"Ficha 1: {ficha1} - Ficha 2: {ficha2}")
        
        if ficha1 == ficha2:    #Si las fichas son pares iguales la agrego a la lista de encontradas
            jugador1["Fichas encontradas"].append(ficha1)
            jugador1["Replay"] = True

        mostrar_tablero_oculto(jugador2["Tablero"], jugador1["Fichas encontradas"])

    else:
        ficha1 = jugador1["Tablero"][coordenada1[1]][coordenada1[0]]
        ficha2 = jugador1["Tablero"][coordenada2[1]][coordenada2[0]]
        print(f"Ficha 1: {ficha1} - Ficha 2: {ficha2}")
        
        if ficha1 == ficha2:
            jugador2["Fichas encontradas"].append(ficha1)
            jugador2["Replay"] = True

        mostrar_tablero_oculto(jugador1["Tablero"], jugador2["Fichas encontradas"])

    return juego

#Comodines
def fatality(tablero : list) -> list:
    '''
    PRE: tablero es una matriz
    POST: Devuelve la matriz traspuesta
    '''
    nuevo_tablero = []

    for i in range(len(tablero)):   
        fila = []
        
        for j in range(len(tablero)): 
            fila.append(tablero[j][i])  

        nuevo_tablero.append(fila)

    return nuevo_tablero

def replay(jugador_actual : dict) -> None:
    '''
    Recibe los datos del jugador actual y agrega la clave "Replay"
    que indica que el proximo turno sera el suyo nuevamente
    '''
    jugador_actual["Replay"] = True

def layout(tablero : list) -> None:
    '''
    PRE: tablero es una matriz
    POST: Redistribuye los elementos de la matriz de manera random
    '''
    
    random.shuffle(tablero)

def toti(tablero : list) -> list:
    '''
    PRE: tablero es una matriz
    POST: Devuelve la matriz espejada horizontal o verticalmente 
    '''
    nuevo_tablero = []
    espejar_horizontal = (True, False)

    if random.choice(espejar_horizontal):
        for fila in tablero:
            nuevo_tablero.append(fila[::-1])
    
    else:
        for fila in tablero[::-1]:
            nuevo_tablero.append(fila)

    return nuevo_tablero

#Configuraciones
def config_inicial(duracion : int =CORTO) -> tuple:
    '''
    PRE: Si duracion es pasada por parametro, debera ser == CORTO, MEDIO o LARGO
    Toma CORTO como predeterminado
    POST: Devuelve empaquetados en una tupla un diccionario con las probabilidades 
    iniciales de los comodines y un entero referente a las dimensiones del tablero.
    Las claves serán Replay, Layout, Toti, Fatality, enteros que simbolizan el porcentaje 
    de probabilidad de cada comodin.
    '''

    return {"Replay": 25,
            "Layout": 25,
            "Toti": 25,
            "Fatality": 25}, duracion

def cambiar_duracion() -> int:
    '''
    POST: Pide al usuario la nueva duracion deseada y la valida hasta que ingrese
    una con el mismo valor que CORTO, MEDIO o LARGO. Devuelve un entero referente 
    a la cantidad de filas y columnas que desea el usuario
    '''
    duraciones_validas = (CORTO,MEDIO,LARGO)
    valor_deseado = int(input("De cuantas filas y columnas deseas que sean los tableros? "))
    
    while valor_deseado not in duraciones_validas: 
        print(f"Duracion inválida, debes escoger uno de estos valores: {duraciones_validas}")
        valor_deseado = int(input("Vuelve a ingresar: "))
    
    print(f"Cambio efectuado con exito! Dimension del tablero cambiada a {valor_deseado}")
    
    return valor_deseado

def cambiar_prob_comodines(config_comodines : dict) -> None:
    '''
    PRE: Debe recibir un diccionario con la configuracion actual de los comodines,
    cuyas claves sean el nombre del comodin y los valores un entero entre 1 y 100
    que indica el porcentaje de probabilidad
    POST: Valida y modifica los parametros ingresado
    '''
    comodin = input("Cual comodin deseas cambiar?").capitalize()
    valor_deseado = int(input("Por qué valor? (Indica solo el numero) "))

    if comodin not in config_comodines:
        print(f"Opcion inválida, debes escribir uno de estos parametros: {tuple(config_comodines.keys())}")   
    
    if valor_deseado < 0 or valor_deseado > 100:
        print("Valor inválido, la probabilidad debe ser entre 0 y 100%")
    
    else:
        config_comodines[comodin] = valor_deseado
        print(f"Cambio efectuado con exito! Probabilidad de {comodin} cambiada a {valor_deseado}%")

def main() -> None:
    
    opcion = 0
    prob_comodines, duracion = config_inicial()
    ganadores = []

    print("*** Bienvenido a Memotest! ***")
    
    while opcion != SALIR:
        
        mostrar_menu_principal()

        opcion = int(input("Elige una opción: "))

        if opcion not in [NUEVA_PARTIDA, CONFIGURACION, PUNTUACIONES, SALIR]:
            print("Opción inválida")
        
        if opcion == NUEVA_PARTIDA:
            turno_jugador1 = True
            terminado = False  
            juego = crear_partida(duracion, [input("Nombre jugador 1: "), input("Nombre jugador 2: ")])
            
            while not terminado:
                if turno_jugador1:
                    jugador_acutal = juego[0]
                else:
                    jugador_acutal = juego[1]
                
                print("\nTURNO: " + jugador_acutal["Nombre"])
                
                comprobar_comodines(jugador_acutal)
                jugar_dado(jugador_acutal, prob_comodines)
                juego = avanzar(juego, turno_jugador1)

                #Cambio de turno
                if "Replay" in jugador_acutal:
                    jugador_acutal.pop("Replay")
                else:
                    turno_jugador1 = not turno_jugador1

                terminado, ganador = hay_ganador(juego)

            print(f"Juego finalizado!\nGANADOR: {ganador}")
            agregar_ganador(ganador, ganadores)
        
        if opcion == CONFIGURACION:            
            mostrar_menu_config(prob_comodines, duracion)
            parametro = int(input("\nQué parametro deseas cambiar?\n1-Duracion\n2-Comodines\n"))
            
            if parametro == 1:
                duracion = cambiar_duracion()
            elif parametro == 2:
                cambiar_prob_comodines(prob_comodines)
            else:
                print("Parametro invalido, vuelve a intentar")   
        
        if opcion == PUNTUACIONES:
            print("Ganadores:\n Nombre/Victorias/Partidas")
            mostrar_puntuaciones(ganadores)
    
    print("Saliendo...")

main()