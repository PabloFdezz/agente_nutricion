# app/services/servicio_nutricion.py
def generar_prompt(datos, calorias, macros):
    """
    Construye el prompt para Groq usando los datos validados y los cálculos.
    """
    return f"""
Genera un plan nutricional en español para:
Edad: {datos['edad']}
Peso: {datos['peso']}
Altura: {datos['altura']}
Sexo: {datos['sexo']}
Nivel de Actividad: {datos['nivel_actividad_desc']}
Objetivo: {datos['objetivo']}
Necesidades calóricas: {calorias} kcal
Macronutrientes: {macros}

Devuelve **solo un JSON válido** con la siguiente estructura:
{{
    "calorias": "...",
    "macros": "...",
    "menu": "...",
    "recomendaciones": "...",
    "snacks": ["...", "..."]
}}
"""