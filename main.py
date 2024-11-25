from flask import Blueprint, render_template, url_for, request,send_from_directory ,jsonify, redirect
import reportlab
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import letter
import io
from PyPDF2 import PdfReader, PdfWriter
import os

main=Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('estado.html')

@main.route('/formato')
def formato():
    return render_template('auto_formato.html')

@main.route('/cultivo')
def cultivo():
    return render_template('cultivo.html')

@main.route('/enfermedades')
def enfermedades():
    return render_template('enfermedades.html')

@main.route('/plagas')
def plagas():
    return render_template('plagas.html')

@main.route('/malezas')
def malezas():
    return render_template('malezas.html')

@main.route('/estado')
def estado():
    return render_template('estado.html')

@main.route('/formato/herbicida')
def herbicida():
    return render_template('herbicida.html')

@main.route('/formato/herbicida/formulario', methods=['GET', 'POST'])
def formulario_herb():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha1 = fecha_hoy = datetime.today().date()
        fecha2 = request.form['date_activity']
        producto = request.form['Producto']
        costo = request.form['costo']
        just = request.form['Justificacion']
        dosis = request.form['dosis']
        area = request.form.get('area')
        if area == 'Lote':
            area=3060
        elif area=='Cultivo':
            area=2700
        cant_prod=float(dosis)*float(area)/10000
        def add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, positions):
            # Leer el archivo PDF original
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()

            # Crear un lienzo en memoria para agregar el texto
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Escribir cada texto en su posición
            for key, value in text_data.items():
                x, y = positions[key]
                can.drawString(x, y, f"{key} {value}")
            can.save()

            # Mover el lienzo al inicio y crear un nuevo PDF con la anotación
            packet.seek(0)
            overlay_pdf = PdfReader(packet)

            # Combinar las páginas originales con la nueva página que contiene el texto
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if page_num == 0:  # Solo agregar anotaciones en la primera página
                    page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)
            blank_packet = io.BytesIO()
            can = canvas.Canvas(blank_packet, pagesize=letter)
            tiempo_cal = request.form['tiempo_cal']
            area_cal = request.form['area_cal']
            caudal = request.form['caudal']
            dosis = request.form['dosis']
            area = request.form.get('area')
            if area == 'Lote':
                area=3060
            elif area=='Cultivo':
                area=2700

            cant_prod=float(dosis)*float(area)/10000
            tiempo_ap=(float(tiempo_cal)*float(area))/float(area_cal)
            lit_mezcla=float(caudal)*float(tiempo_ap)/1000
            num_bombas=float(lit_mezcla)/25
            Cant_bomb=(float(cant_prod)/float(num_bombas))*1000
            Cant_agua=float(lit_mezcla)*10000/float(area)

            can.setFont("Helvetica", 14)
            can.drawString(100, 750, f"Dosis recomendada del producto: {dosis}L")
            can.drawString(100, 730, f"Area: {area}m2")
            can.drawString(100, 700, "Cantidad de producto:")
            can.drawString(280, 680, f"{dosis}L * {area}m2 / 10000m2 = {round(cant_prod,2)}L")
            can.drawString(100, 650, "Tiempo de aplicación:")
            can.drawString(280, 630, f"({tiempo_cal}s * {area}m2) / {area_cal}m2 = {round(tiempo_ap,2)}s")
            can.drawString(100, 600, "Litros de mezcla total:")
            can.drawString(280, 580, f"({caudal}(ml/s) * {round(tiempo_ap,2)}s)/1000 = {round(lit_mezcla,2)}L")
            can.drawString(100, 550, "Número de bombas:")
            can.drawString(280, 530, f"({round(lit_mezcla,2)}L / 25) = {round(num_bombas,2)}")
            can.drawString(100, 500, "Cantidad de producto por bomba:")
            can.drawString(280, 480, f"{round(cant_prod,2)}L / {round(num_bombas,2)} * 1000 = {round(Cant_bomb,2)} L")
            can.drawString(100, 450, "Cantidad de Agua utilizada:")
            can.drawString(280, 430, f"({round(lit_mezcla,2)}L * 10000m2) / {area}m2 = {round(Cant_agua,2)}L")

            can.showPage()  # Añadir una página vacía
            can.save()
            blank_packet.seek(0)

            # Leer la página en blanco y agregarla al PDF
            blank_pdf = PdfReader(blank_packet)
            writer.add_page(blank_pdf.pages[0])  # Añadir la página en blanco

            # Guardar el nuevo archivo PDF con el texto añadido y la página en blanco
            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)
        text_data = {
        fecha1: "",
        fecha2: "",
        "Puerro": "",
        nombre: "",
        producto : "",
        cant_prod : "",
        just : "",
        costo : "",
        }
        positions = {
        fecha1: (175, 745),
        fecha2: (443, 745),
        "Puerro": (150, 730),
        nombre: (450, 730),
        producto  : (165, 553),
        cant_prod : (255, 553),
        just: (344, 553),
        costo : (435, 553),
        }

        # Rutas de archivo
        input_pdf_path = "FORMATO SOLICITUDES.pdf"
        output_pdf_path = "venv_web_ciclo/static/formulario_rellenado.pdf"

        # Ejecutar la función
        add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, positions)
        print(f"PDF con anotaciones y página en blanco guardado en {output_pdf_path}")
            # Después de procesar los datos, redirigir a otra página o mostrar un mensaje
        return redirect(url_for('main.leido'))

@main.route('/formato/fungicida')
def fungicida():
    return render_template('fungicida.html')


@main.route('/formato/fungicida/formulario', methods=['GET', 'POST'])
def formulario_fung():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha1 = fecha_hoy = datetime.today().date()
        fecha2 = request.form['date_activity']
        producto = request.form['Producto']
        costo = request.form['costo']
        just = request.form['Justificacion']
        dosis = request.form['dosis']
        area = request.form.get('area')
        if area == 'Lote':
            area=3060
        elif area=='Cultivo':
            area=2700
        cant_prod=float(dosis)*float(area)/10000
        def add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, positions):
            # Leer el archivo PDF original
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()

            # Crear un lienzo en memoria para agregar el texto
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Escribir cada texto en su posición
            for key, value in text_data.items():
                x, y = positions[key]
                can.drawString(x, y, f"{key} {value}")
            can.save()

            # Mover el lienzo al inicio y crear un nuevo PDF con la anotación
            packet.seek(0)
            overlay_pdf = PdfReader(packet)

            # Combinar las páginas originales con la nueva página que contiene el texto
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if page_num == 0:  # Solo agregar anotaciones en la primera página
                    page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)
            blank_packet = io.BytesIO()
            can = canvas.Canvas(blank_packet, pagesize=letter)
            tiempo_cal = request.form['tiempo_cal']
            area_cal = request.form['area_cal']
            caudal = request.form['caudal']
            dosis = request.form['dosis']
            area = request.form.get('area')
            if area == 'Lote':
                area=3060
            elif area=='Cultivo':
                area=2700

            cant_prod=float(dosis)*float(area)/10000
            tiempo_ap=(float(tiempo_cal)*float(area))/float(area_cal)
            lit_mezcla=float(caudal)*float(tiempo_ap)/1000
            num_bombas=float(lit_mezcla)/25
            Cant_bomb=(float(cant_prod)/float(num_bombas))*1000
            Cant_agua=float(lit_mezcla)*10000/float(area)

            can.setFont("Helvetica", 14)
            can.drawString(100, 750, f"Dosis recomendada del producto: {dosis}L")
            can.drawString(100, 730, f"Area: {area}m2")
            can.drawString(100, 700, "Cantidad de producto:")
            can.drawString(280, 680, f"{dosis}L * {area}m2 / 10000m2 = {round(cant_prod,2)}L")
            can.drawString(100, 650, "Tiempo de aplicación:")
            can.drawString(280, 630, f"({tiempo_cal}s * {area}m2) / {area_cal}m2 = {round(tiempo_ap,2)}s")
            can.drawString(100, 600, "Litros de mezcla total:")
            can.drawString(280, 580, f"({caudal}(ml/s) * {round(tiempo_ap,2)}s)/1000 = {round(lit_mezcla,2)}L")
            can.drawString(100, 550, "Número de bombas:")
            can.drawString(280, 530, f"({round(lit_mezcla,2)}L / 25) = {round(num_bombas,2)}")
            can.drawString(100, 500, "Cantidad de producto por bomba:")
            can.drawString(280, 480, f"{round(cant_prod,2)}L / {round(num_bombas,2)} * 1000 = {round(Cant_bomb,2)} L")
            can.drawString(100, 450, "Cantidad de Agua utilizada:")
            can.drawString(280, 430, f"({round(lit_mezcla,2)}L * 10000m2) / {area}m2 = {round(Cant_agua,2)}L")

            can.showPage()  # Añadir una página vacía
            can.save()
            blank_packet.seek(0)

            # Leer la página en blanco y agregarla al PDF
            blank_pdf = PdfReader(blank_packet)
            writer.add_page(blank_pdf.pages[0])  # Añadir la página en blanco

            # Guardar el nuevo archivo PDF con el texto añadido y la página en blanco
            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)
        text_data = {
        fecha1: "",
        fecha2: "",
        "Puerro": "",
        nombre: "",
        producto : "",
        cant_prod : "",
        just : "",
        costo : "",
        }
        positions = {
        fecha1: (175, 745),
        fecha2: (443, 745),
        "Puerro": (150, 730),
        nombre: (450, 730),
        producto  : (165, 593),
        cant_prod : (255, 593),
        just: (344, 593),
        costo : (435, 593),
        }

        # Rutas de archivo
        input_pdf_path = "FORMATO SOLICITUDES.pdf"
        output_pdf_path = "venv_web_ciclo/static/formulario_rellenado.pdf"

        # Ejecutar la función
        add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, positions)
        print(f"PDF con anotaciones y página en blanco guardado en {output_pdf_path}")
            # Después de procesar los datos, redirigir a otra página o mostrar un mensaje
        return redirect(url_for('main.leido'))

@main.route('/leido')
def leido():
    # Definir la ruta del archivo PDF
    pdf_path = os.path.join('venv_web_ciclo/static/formulario_rellenado.pdf')

    # Verificar si el archivo existe
    if os.path.exists(pdf_path):
        # Enviar el PDF como respuesta para visualizarlo y permitir la descarga
        return render_template('leido.html', pdf_url=url_for('static', filename='formulario_rellenado.pdf'))
    else:
        return "El archivo PDF no se encuentra disponible.", 404



@main.route('/formato/insecticida')
def insecticida():
    return render_template('insecticida.html')

@main.route('/formato/insecticida/formulario', methods=['GET', 'POST'])
def formulario_ins():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha1 = fecha_hoy = datetime.today().date()
        fecha2 = request.form['date_activity']
        producto = request.form['Producto']
        costo = request.form['costo']
        just = request.form['Justificacion']
        dosis = request.form['dosis']
        area = request.form.get('area')
        if area == 'Lote':
            area=3060
        elif area=='Cultivo':
            area=2700
        cant_prod=float(dosis)*float(area)/10000
        def add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, positions):
            # Leer el archivo PDF original
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()

            # Crear un lienzo en memoria para agregar el texto
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Escribir cada texto en su posición
            for key, value in text_data.items():
                x, y = positions[key]
                can.drawString(x, y, f"{key} {value}")
            can.save()

            # Mover el lienzo al inicio y crear un nuevo PDF con la anotación
            packet.seek(0)
            overlay_pdf = PdfReader(packet)

            # Combinar las páginas originales con la nueva página que contiene el texto
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                if page_num == 0:  # Solo agregar anotaciones en la primera página
                    page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)
            blank_packet = io.BytesIO()
            can = canvas.Canvas(blank_packet, pagesize=letter)
            tiempo_cal = request.form['tiempo_cal']
            area_cal = request.form['area_cal']
            caudal = request.form['caudal']
            dosis = request.form['dosis']
            area = request.form.get('area')
            if area == 'Lote':
                area=3060
            elif area=='Cultivo':
                area=2700

            cant_prod=float(dosis)*float(area)/10000
            tiempo_ap=(float(tiempo_cal)*float(area))/float(area_cal)
            lit_mezcla=float(caudal)*float(tiempo_ap)/1000
            num_bombas=float(lit_mezcla)/25
            Cant_bomb=(float(cant_prod)/float(num_bombas))*1000
            Cant_agua=float(lit_mezcla)*10000/float(area)

            can.setFont("Helvetica", 14)
            can.drawString(100, 750, f"Dosis recomendada del producto: {dosis}L")
            can.drawString(100, 730, f"Area: {area}m2")
            can.drawString(100, 700, "Cantidad de producto:")
            can.drawString(280, 680, f"{dosis}L * {area}m2 / 10000m2 = {round(cant_prod,2)}L")
            can.drawString(100, 650, "Tiempo de aplicación:")
            can.drawString(280, 630, f"({tiempo_cal}s * {area}m2) / {area_cal}m2 = {round(tiempo_ap,2)}s")
            can.drawString(100, 600, "Litros de mezcla total:")
            can.drawString(280, 580, f"({caudal}(ml/s) * {round(tiempo_ap,2)}s)/1000 = {round(lit_mezcla,2)}L")
            can.drawString(100, 550, "Número de bombas:")
            can.drawString(280, 530, f"({round(lit_mezcla,2)}L / 25) = {round(num_bombas,2)}")
            can.drawString(100, 500, "Cantidad de producto por bomba:")
            can.drawString(280, 480, f"{round(cant_prod,2)}L / {round(num_bombas,2)} * 1000 = {round(Cant_bomb,2)} L")
            can.drawString(100, 450, "Cantidad de Agua utilizada:")
            can.drawString(280, 430, f"({round(lit_mezcla,2)}L * 10000m2) / {area}m2 = {round(Cant_agua,2)}L")

            can.showPage()  # Añadir una página vacía
            can.save()
            blank_packet.seek(0)

            # Leer la página en blanco y agregarla al PDF
            blank_pdf = PdfReader(blank_packet)
            writer.add_page(blank_pdf.pages[0])  # Añadir la página en blanco

            # Guardar el nuevo archivo PDF con el texto añadido y la página en blanco
            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)
        text_data = {
        fecha1: "",
        fecha2: "",
        "Puerro": "",
        nombre: "",
        producto : "",
        cant_prod : "",
        just : "",
        costo : "",
        }
        positions = {
        fecha1: (175, 745),
        fecha2: (443, 745),
        "Puerro": (150, 730),
        nombre: (450, 730),
        producto  : (165, 516),
        cant_prod : (255, 516),
        just: (344, 516),
        costo : (435, 516),
        }

        # Rutas de archivo
        input_pdf_path = "FORMATO SOLICITUDES.pdf"
        output_pdf_path = "venv_web_ciclo/static/formulario_rellenado.pdf"

        # Ejecutar la función
        add_text_to_pdf(input_pdf_path, output_pdf_path, text_data, positions)
        print(f"PDF con anotaciones y página en blanco guardado en {output_pdf_path}")
            # Después de procesar los datos, redirigir a otra página o mostrar un mensaje
        return redirect(url_for('main.leido'))