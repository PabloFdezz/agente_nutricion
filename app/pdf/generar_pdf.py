from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf(plan_json, nombre_archivo="plan.pdf"):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, f"Plan nutricional - Calorías: {plan_json['calorias']} kcal")

    y = 730
    for comida, valor in plan_json["menu_diario"].items():
        c.drawString(50, y, f"{comida.capitalize()}: {valor}")
        y -= 20

    c.save()
    return nombre_archivo