# utils/formulario.py
def formulario(form_data, niveles_actividad):
    # Campos obligatorios
    required = ["edad", "peso", "altura", "sexo", "nivel_actividad", "objetivo"]
    if not all([form_data.get(f) for f in required]):
        return None, "Faltan campos obligatorios"

    # Edad, peso, altura
    try:
        edad = int(form_data.get("edad"))
        peso = float(form_data.get("peso"))
        altura = float(form_data.get("altura"))
    except (TypeError, ValueError):
        return None, "Datos numéricos inválidos"

    # Sexo
    sexo = form_data.get("sexo", "").lower()
    if sexo not in ["hombre", "mujer"]:
        return None, "Sexo inválido"

    # Nivel de actividad
    nivel_actividad = form_data.get("nivel_actividad", "").lower()
    nivel_dict = dict(niveles_actividad)
    nivel_actividad_desc = nivel_dict.get(nivel_actividad)
    if not nivel_actividad_desc:
        return None, "Nivel de actividad inválido"

    # Objetivo
    objetivo = form_data.get("objetivo", "").lower()
    if objetivo not in ["mantenimiento", "definicion", "musculo"]:
        return None, "Objetivo inválido"

    return {
        "edad": edad,
        "peso": peso,
        "altura": altura,
        "sexo": sexo,
        "nivel_actividad": nivel_actividad,
        "nivel_actividad_desc": nivel_actividad_desc,
        "objetivo": objetivo
    }, None