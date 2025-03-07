def determinar_sectores(lista_sectores):
    sectores_presentes = {sector.split('_')[0] for sector in lista_sectores}  # Extraer los prefijos
    if sectores_presentes == {"syg"}:
        return "Pertenece solo a SYG"
    elif sectores_presentes == {"mgm"}:
        return "Pertenece solo a MGM"
    elif sectores_presentes == {"syg", "mgm"}:
        return "Pertenece a ambos sectores"
    else:
        return "Sectores desconocidos"

# Ejemplos de uso:
encargado_1 = ['syg_ingenieria', 'mgm_ingenieria', 'syg_laboratorio', 'mgm_laboratorio']
encargado_2 = ['mgm_ingenieria', 'mgm_laboratorio']
encargado_3 = ['syg_laboratorio', 'syg_ingenieria']

print(determinar_sectores(encargado_1))  # Salida: Pertenece a ambos sectores
print(determinar_sectores(encargado_2))  # Salida: Pertenece solo a MGM
print(determinar_sectores(encargado_3))  # Salida: Pertenece solo a SYG