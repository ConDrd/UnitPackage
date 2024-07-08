def check_dimension(unit):
    try:
        separacion = unit.split("^")
        unidad = separacion[0]
        potencia = float(separacion[1])
    except IndexError:
        unidad = unit
        potencia = 1.0
    return unidad, potencia

def separar_unidades(unidad: str):
    unidades_dict = {"multiplicando": [], "dividiendo": []}
    if "/" in unidad:
        numerador, denominador = unidad.split("/")
        multiplicaciones = numerador.split("*")
        if "(" in denominador and ")" in denominador:
            paren_1 = denominador.find("(") + 1
            paren_2 = denominador.find(")")
            divisiones = denominador[paren_1:paren_2].split("*")
            parte_derecha = denominador[paren_2+2:].split("*")
            multiplicaciones.extend(parte_derecha)
        else:
            parte_derecha = denominador.split("*")
            divisiones = [parte_derecha[0]]
            multiplicaciones.extend(parte_derecha[1:])
    else:
        multiplicaciones = unidad.split("*")
        divisiones = []

    unidades_dict["multiplicando"] = multiplicaciones
    unidades_dict["dividiendo"] = divisiones
    
    return unidades_dict

def armar_unidades(unidades: dict):
    multiplicados = unidades["multiplicando"]
    dividiendo = unidades["dividiendo"]
    
    text = "*".join(multiplicados)
    
    if dividiendo:
        if len(dividiendo) > 1:
            text += "/(" + "*".join(dividiendo) + ")"
        else:
            text += "/" + dividiendo[0]
    
    return text

def eliminar_unidades(unidades: dict):
    multiplicados = unidades["multiplicando"]
    dividiendo = unidades["dividiendo"]

    lista_multiplicados = list(map(check_dimension, multiplicados))
    lista_dividiendo = list(map(check_dimension, dividiendo))

    # Inicializar los diccionarios
    multiplicandos = {}
    dividiendos = {}
    
    # Procesar la lista de multiplicados
    for unidad, exponente in lista_multiplicados:
        multiplicandos[unidad] = multiplicandos.get(unidad, 0) + exponente
    
    # Procesar la lista de dividiendo
    for unidad, exponente in lista_dividiendo:
        dividiendos[unidad] = dividiendos.get(unidad, 0) + exponente

    nuevos_multiplicados = []
    nuevos_dividiendo = []
    
    for unidad, exponente in multiplicandos.items():
        if unidad in dividiendos:
            dif_exponente = exponente - dividiendos[unidad]
            if dif_exponente > 0:
                nuevos_multiplicados.append(f"{unidad}^{dif_exponente}" if dif_exponente != 1 else unidad)
            elif dif_exponente < 0:
                nuevos_dividiendo.append(f"{unidad}^{-dif_exponente}" if dif_exponente != -1 else unidad)
            del dividiendos[unidad]
        else:
            nuevos_multiplicados.append(f"{unidad}^{exponente}" if exponente != 1 else unidad)
    
    for unidad, exponente in dividiendos.items():
        nuevos_dividiendo.append(f"{unidad}^{exponente}" if exponente != 1 else unidad)
    
    if nuevos_multiplicados == [""]:
        nuevos_multiplicados = ["1"]
    
    for i, elementos in enumerate(nuevos_multiplicados):
        if "^0" in elementos:
            nuevos_multiplicados.pop(i)
            
    for i, elementos in enumerate(nuevos_dividiendo):
        if "^0" in elementos:
            nuevos_dividiendo.pop(i)
                
    return {
        "multiplicando": [elemento for elemento in nuevos_multiplicados if elemento],
        "dividiendo": [elemento for elemento in nuevos_dividiendo if elemento]
    }

# Ejemplo de uso
# unidad = "m^0*m/(s*h^0)" 
# resultado = separar_unidades(unidad)
# resultado = eliminar_unidades(resultado)
# print(resultado)
# print(armar_unidades(resultado)) 