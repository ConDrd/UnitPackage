import units
import dimensional


class Unit:
    def __init__(self, unit: str, value: float = 1):
        self.unit = unit
        self.value = value
        
        self.check_dimension = lambda unit: dimensional.check_dimension(unit)

    def convert_to(self, unit_converter: str, forced=False, decimals: int = 3):
        
        def reference_unit(unidad_actual, potencia_actual, unidad_deseada, basic_units):
            for lista in basic_units:
                if unidad in lista:
                    referencia = 1 * lista[unidad_actual]
                    conversion = self.value * (referencia / lista[unidad_deseada]) ** float(potencia_actual)
                    if potencia_actual != 1:
                        new_unit = f"{unidad_deseada}^{potencia_actual}"
                    else:
                        new_unit = unidad_deseada
                    
                    return conversion, new_unit
        
        def multiplicador(lista):
            multiplicatoria = 1
            for i in lista:
                multiplicatoria *= i
            return multiplicatoria
            
        # Constantes
        
        basic_units = [units.lenght, units.mass, units.time]
        
        # Procedimiento de limpieza
        unidad_deseada = dimensional.separar_unidades(unit_converter)
        unidad_actual = dimensional.separar_unidades(self.unit)
        
        unidad_deseada = dimensional.eliminar_unidades(unidad_deseada)
        unidad_actual = dimensional.eliminar_unidades(unidad_actual)
        
        mult_des = unidad_deseada["multiplicando"]
        div_des = unidad_deseada["dividiendo"]
        
        mult_act = unidad_actual["multiplicando"]
        div_act = unidad_actual["dividiendo"]
        
        valor_nuevo_mult=[]
        unidad_nuevo_mult=[]
        for actual in mult_act:
            unidad, potencia = dimensional.check_dimension(actual)
            if len(mult_des) !=0:
                for deseado in mult_des:
                    unidad_des, _ = dimensional.check_dimension(deseado)
                    try:
                        res =  reference_unit(unidad, potencia, unidad_des, basic_units)
                        if res[1] not in mult_act:
                            valor_nuevo_mult.append(res[0])
                            unidad_nuevo_mult.append(res[1])
                    except:
                        if unidad not in mult_act:
                            valor_nuevo_mult.append(1)
                            unidad_nuevo_mult.append(unidad)
            else:
                valor_nuevo_mult.append(1)
                unidad_nuevo_mult.append(unidad)
                

        valor_nuevo_div=[]
        unidad_nuevo_div=[]
        for actual in div_act:
            unidad, potencia = dimensional.check_dimension(actual)
            if len(div_des) !=0:
                for deseado in div_des:
                    unidad_des, _ = dimensional.check_dimension(deseado)
                    try:
                        res =  reference_unit(unidad, potencia, unidad_des, basic_units)
                        if res[1] not in div_act:
                            valor_nuevo_div.append(res[0])
                            unidad_nuevo_div.append(res[1])
                    except:
                        if unidad not in div_act:
                            valor_nuevo_div.append(1)
                            unidad_nuevo_div.append(unidad)
            else:
                valor_nuevo_div.append(1)
                unidad_nuevo_div.append(unidad)
                        
        # Calculando el nuevo valor
        multiplicatoria_mult = multiplicador(valor_nuevo_mult)
        multiplicatoria_div = multiplicador(valor_nuevo_div)
        
        self.value *= multiplicatoria_mult
        self.value /= multiplicatoria_div
        
        # Analisis dimensional de la respuesta
        
        dic_unidades = {"multiplicando": unidad_nuevo_mult, "dividiendo": unidad_nuevo_div}
        
        unidades_finales = dimensional.armar_unidades(dic_unidades)
        
        print(unidades_finales)
        
        return Unit(unidades_finales, self.value)
     
    def __mul__(self, other):
        # Verificar que sea multiplicacion entre numeros
        if isinstance(other, (int, float)):
            return Unit(self.unit, self.value * other)
        # Multiplicacion entre objetos Unit
        elif isinstance(other, Unit):
            # Verificar la dimensionalidad de las variables
            unidades_self = dimensional.separar_unidades(self.unit)
            unidades_other = dimensional.separar_unidades(other.unit)
            
            self_mult = unidades_self["multiplicando"]
            other_mult = unidades_other["multiplicando"]
            
            self_div = unidades_self["dividiendo"]
            other_div = unidades_other["dividiendo"]
            all_mult = self_mult + other_mult
            all_div = self_div + other_div
            
            # Eliminar todos los "1" de all_mult y all_div
            all_mult = [x for x in all_mult if x != "1"]
            all_div = [x for x in all_div if x != "1"]

            print(all_mult, all_div)
            
            dict_unidades = {"multiplicando": all_mult, "dividiendo": all_div}
            
            unidades = dimensional.eliminar_unidades(dict_unidades)
            unidades = dimensional.armar_unidades(unidades)

            if unidades == "1":
                unidades = "Adimensional"

            new_value = self.value * other.value
            
            return Unit(unidades, new_value)
            
    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return Unit(f"{self.unit}^{other}", self.value**other)
        else:
            raise TypeError("Potencia no soportada para el tipo dado.")

    def __add__(self, other):
        if isinstance(other, Unit) and self.unit == other.unit:
            return Unit(self.unit, self.value + other.value)
        else:
            raise TypeError(f"No se puede sumar '{self.unit}' con '{other.unit}'.")

    def __sub__(self, other):
        if isinstance(other, Unit) and self.unit == other.unit:
            return Unit(self.unit, self.value - other.value)
        else:
            raise TypeError(f"No se puede restar '{self.unit}' con '{other.unit}'.")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Unit(self.unit, self.value * other)
        # Verificar si es Objeto tipo Unit
        elif isinstance(other, Unit):
            # Verificar la dimensionalidad de las variables
            unidades_self = dimensional.separar_unidades(self.unit)
            unidades_other = dimensional.separar_unidades(other.unit)
            
            self_mult = unidades_self["multiplicando"]
            other_mult = unidades_other["dividiendo"]
            
            self_div = unidades_self["dividiendo"]
            other_div = unidades_other["multiplicando"]
            all_mult = self_mult + other_mult
            all_div = self_div + other_div
            
            # Eliminar todos los "1" de all_mult y all_div
            all_mult = [x for x in all_mult if x != "1"]
            all_div = [x for x in all_div if x != "1"]

            print(all_mult, all_div)
            
            dict_unidades = {"multiplicando": all_mult, "dividiendo": all_div}
            
            unidades = dimensional.eliminar_unidades(dict_unidades)
            unidades = dimensional.armar_unidades(unidades)

            if unidades == "1":
                unidades = "Adimensional"

            new_value = self.value / other.value
            
            return Unit(unidades, new_value)

        else:
            raise TypeError("Division no soportada para el tipo dado.")


# Uso de la clase
numero_1 = 10 * Unit("ft")
numero_2 = numero_1.convert_to("m")


print(numero_2, sep="\n")

