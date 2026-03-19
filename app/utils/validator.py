def validar_formulario(request, niveles_actividad):
    edad_raw = request.form.get("edad")
    peso_raw = request.form.get("peso")
    altura_raw = request.form.get("altura")

    # ✅ Campos obligatorios
    if not all([edad_raw, peso_raw, altura_raw]):
        return None, "Faltan campos obligatorios"

    # ✅ Conversión
    try:
        edad = int(edad_raw)
        peso = float(peso_raw)
        altura = float(altura_raw)
    except (TypeError, ValueError):
        return None, "Edad, peso y altura deben ser números válidos"

    # ✅ Valores positivos
    if edad <= 0 or peso <= 0 or altura <= 0:
        return None, "Los valores deben ser mayores que cero"

    # ✅ Sexo
    sexo = request.form.get("sexo").lower()
    if sexo not in ["hombre", "mujer"]:
        return None, "Sexo inválido"

    # ✅ Nivel actividad
    nivel_actividad = request.form.get("nivel_actividad")
    nivel_dict = dict(niveles_actividad)

    if nivel_actividad not in nivel_dict:
        return None, "Nivel de actividad inválido"
    

    # ✅ Objetivo
    objetivos_validos = ["mantenimiento", "definicion", "musculo"]

    objetivo = request.form.get("objetivo").lower()
    if objetivo not in objetivos_validos:
        return None, "Objetivo inválido"

    # ✅ Textos
    comidas_favoritas = request.form.get("comidas_favoritas", "").strip()
    restricciones = request.form.get("restricciones", "Ninguna").strip()

    if len(comidas_favoritas) > 300:
        return None, "Comidas favoritas demasiado largas"

    if len(restricciones) > 300:
        return None, "Restricciones demasiado largas"

    return {
        "edad": edad,
        "peso": peso,
        "altura": altura,
        "sexo": sexo,
        "nivel_actividad": nivel_actividad,
        "nivel_actividad_desc": nivel_dict[nivel_actividad],
        "objetivo": objetivo,
        "comidas_favoritas": comidas_favoritas,
        "restricciones": restricciones
    }, None