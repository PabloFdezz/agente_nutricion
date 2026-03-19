def calcular_calorias(edad, peso, altura, sexo, nivel):
    if sexo == "hombre":
        tmb = 10*peso + 6.25*altura - 5*edad + 5
    else:
        tmb = 10*peso + 6.25*altura - 5*edad - 161

    factores = {
        "sedentario": 1.2,
        "poco_activo": 1.375,
        "activo": 1.55,
        "muy_activo": 1.725,
        "super_activo": 1.9
    }

    return round(tmb * factores.get(nivel, 1.2))

def calcular_macros(calorias, objetivo):
    if objetivo == "musculo":
        proteinas = 0.3
        grasas = 0.25
        carbos = 0.45
    elif objetivo == "definicion":
        proteinas = 0.35
        grasas = 0.25
        carbos = 0.40
    else:  # mantenimiento
        proteinas = 0.3
        grasas = 0.3
        carbos = 0.4

    return {"proteinas": proteinas, "grasas": grasas, "carbohidratos": carbos}