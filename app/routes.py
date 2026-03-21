from flask import Blueprint, request, jsonify, render_template
from app.utils.formulario import formulario
from app.utils.calculos import calcular_calorias, calcular_macros
from app.services.servicio_nutricion import generar_prompt
from groq import Groq
import os, json, logging, re

bp = Blueprint("main", __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

niveles_actividad = [
    ('sedentario', 'Sedentario (Poco o ningún ejercicio)'),
    ('poco_activo', 'Poco Activo (1-3 días/semana)'),
    ('activo', 'Activo (3-5 días/semana)'),
    ('muy_activo', 'Muy Activo (6-7 días/semana)'),
    ('super_activo', 'Super Activo (Atleta profesional/2x entrenamientos)')
]

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", niveles_actividad=niveles_actividad)

@bp.route("/nutricion", methods=["POST"])
def nutricion():
    # 1️⃣ Validar formulario
    datos, error = formulario(request.form, niveles_actividad)
    if error:
        return jsonify({"success": False, "error": error})

    # 2️⃣ Calcular calorías y macros
    calorias = calcular_calorias(
        datos["edad"], datos["peso"], datos["altura"], datos["sexo"], datos["nivel_actividad"]
    )
    macros = calcular_macros(calorias, datos["objetivo"])

    # 3️⃣ Generar prompt usando la función del servicio
    prompt = generar_prompt(datos, calorias, macros)

    # 4️⃣ Llamar a Groq y manejar errores
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Eres un nutricionista profesional. Responde en español, recomendaciones seguras, prácticas y realistas. No inventes datos médicos."},
                {"role": "user", "content": prompt}
            ],
            model="qwen/qwen3-32b",
            temperature=0.7,
            max_tokens=1200
        )
        respuesta_texto = completion.choices[0].message.content

        # 5️⃣ Limpiar respuesta antes de parsear
        respuesta = completion.choices[0].message.content

        # Extraer JSON con regex (por si hay texto extra)
        match = re.search(r"\{.*\}", respuesta, re.DOTALL)

        if not match:
            logging.error("No se encontró JSON en la respuesta del modelo")
            return jsonify({
                "success": False,
                "error": "No se recibió JSON válido del modelo"
            })

        json_str = match.group(0)

        # 6️⃣ Parseo con fallback 
        try:
            plan = json.loads(json_str)
        except json.JSONDecodeError:
            logging.error("JSON inválido recibido del modelo")
            return jsonify({
                "success": False,
                "error": "Error procesando la respuesta del modelo"
            })

        return jsonify({"success": True, "plan": plan})

    except Exception as e:
        logging.error(f"Error en Groq: {str(e)}")
        return jsonify({"success": False, "error": "Error generando el plan"})