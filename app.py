from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Cargar variables de entorno (incluye la API KEY de Groq)
load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Lista de niveles de actividad
niveles_actividad = [
    ('sedentario', 'Sedentario (Poco o ningún ejercicio)'),
    ('poco_activo', 'Poco Activo (1-3 días/semana)'),
    ('activo', 'Activo (3-5 días/semana)'),
    ('muy_activo', 'Muy Activo (6-7 días/semana)'),
    ('super_activo', 'Super Activo (Atleta profesional/2x entrenamientos)')
]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", niveles_actividad=niveles_actividad)

def validar_formulario(request):
    try:
        edad = int(request.form.get("edad"))
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
    except (TypeError, ValueError):
        return None, "Edad, peso y altura deben ser números válidos"

    if edad <= 0 or peso <= 0 or altura <= 0:
        return None, "Edad, peso y altura deben ser mayores que cero"

    sexo = request.form.get("sexo")
    if sexo not in ["hombre", "mujer"]:
        return None, "Sexo inválido"

    nivel_actividad = request.form.get("nivel_actividad")
    nivel_dict = dict(niveles_actividad)

    if nivel_actividad not in nivel_dict:
        return None, "Nivel de actividad inválido"

    comidas_favoritas = request.form.get("comidas_favoritas", "").strip()
    if len(comidas_favoritas) > 300:
        return None, "Comidas favoritas demasiado largas"

    restricciones = request.form.get("restricciones", "Ninguna").strip()
    if len(restricciones) > 300:
        return None, "Restricciones demasiado largas"

    return {
        "edad": edad,
        "peso": peso,
        "altura": altura,
        "sexo": sexo,
        "nivel_actividad": nivel_actividad,
        "nivel_actividad_desc": nivel_dict[nivel_actividad],
        "comidas_favoritas": comidas_favoritas,
        "restricciones": restricciones
    }, None


def calcular_calorias(edad, peso, altura, sexo, nivel):
    if sexo == "hombre":
        tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

    factores = {
        "sedentario": 1.2,
        "poco_activo": 1.375,
        "activo": 1.55,
        "muy_activo": 1.725,
        "super_activo": 1.9
    }

    return round(tmb * factores.get(nivel, 1.2))


def calcular_macros(calorias):
    proteinas = round((calorias * 0.25) / 4)
    grasas = round((calorias * 0.25) / 9)
    carbohidratos = round((calorias * 0.5) / 4)

    return proteinas, grasas, carbohidratos


@app.route("/nutricion", methods=["POST"])
def nutricion():

    datos, error = validar_formulario(request)

    calorias = calcular_calorias(
    datos["edad"],
    datos["peso"],
    datos["altura"],
    datos["sexo"],
    datos["nivel_actividad"]
    )

    proteinas, grasas, carbs = calcular_macros(calorias)

    if error:
        return jsonify({
            "success": False,
            "error": error
        })

    prompt = f"""
    Genera directamente un plan nutricional en español para la siguiente persona:

    Edad: {datos['edad']} años
    Peso: {datos['peso']} kg
    Altura: {datos['altura']} cm
    Sexo: {datos['sexo']}
    Nivel de Actividad: {datos['nivel_actividad_desc']}
    Comidas Favoritas: {datos['comidas_favoritas']}
    Restricciones Dietéticas/Alergias: {datos['restricciones']}

    Necesidades calóricas estimadas (calculadas previamente): {calorias} kcal

    Distribución base de macronutrientes:
    - Proteínas: {proteinas} g
    - Grasas: {grasas} g
    - Carbohidratos: {carbs} g

    IMPORTANTE:
    - Usa estas calorías y macronutrientes como base (no los recalcules).
    - No muestres razonamiento interno.
    """

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Eres un nutricionista profesional..."},
                {"role": "user", "content": prompt}
            ],
            model="qwen/qwen3-32b",
            temperature=0.7,
            max_tokens=1200,
        )

        respuesta = completion.choices[0].message.content

        return jsonify({
            "success": True,
            "plan": respuesta
        })

    except Exception as e:
        logging.error(f"Error en Groq: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Error generando el plan nutricional"
        })

if __name__ == "__main__":
    app.run(debug=True)
