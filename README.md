# App de Nutrición con IA

Aplicación web desarrollada con Flask que genera planes nutricionales personalizados utilizando IA (Groq), en función de los datos del usuario como edad, peso, altura, nivel de actividad y objetivo físico.

---

## Funcionalidades

* Formulario para introducir datos del usuario
* Validación de datos en backend
* Cálculo de necesidades calóricas (Mifflin-St Jeor)
* Distribución de macronutrientes según objetivo
* Generación de plan nutricional personalizado con IA
* Respuesta estructurada en formato JSON
* Arquitectura modular (routes, services, utils)

---

## Estructura del proyecto

```
app/
├── __init__.py
├── routes.py
├── services/
│   └── servicio_nutricion.py
├── utils/
│   ├── calculos.py
│   └── formulario.py
├── templates/
│   └── index.html
run.py
.env
```

---

## Tecnologías utilizadas

* Python
* Flask
* Groq API (LLM)
* HTML / Jinja2
* dotenv

---

## Lógica del sistema

1. El usuario introduce sus datos en el formulario.
2. Se validan los datos en backend.
3. Se calculan:

   * Calorías diarias
   * Macronutrientes
4. Se construye un prompt estructurado.
5. Se envía a la API de Groq.
6. Se recibe una respuesta en JSON.
7. Se devuelve al frontend para mostrar el plan.

---

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**

```bash
venv\Scripts\activate
```

(Si falla por políticas de ejecución, usar:)

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 5. Configurar variables de entorno

Crea un archivo `.env`:

```
GROQ_API_KEY=tu_api_key_aqui
```

---

## Ejecutar la aplicación

```bash
python run.py
```

Abrir en navegador:

```
http://127.0.0.1:5000
```

---

## Testing del endpoint

Puedes probar el endpoint `/nutricion` con herramientas como:

* Insomnia
* Postman

### Ejemplo de request:

**POST** `/nutricion`

Body (form-data):

```
edad=30
peso=70
altura=175
sexo=hombre
nivel_actividad=activo
objetivo=musculo
```

---

## Mejoras futuras

* Guardado de planes en base de datos (SQLite)
* Generación de PDF descargable
* Sistema de usuarios / login
* Dashboard de progreso
* Más personalización de objetivos

---

## Autor

Pablo Fernández

---

## Licencia

Este proyecto es de uso educativo y personal.
