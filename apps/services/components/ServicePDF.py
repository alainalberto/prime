from io import BytesIO
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Paragraph, Table, TableStyle
from apps.services.models import *

def PendingListPDF(request):
    permit = Permit.objects.all()
    insurance = Insurance.objects.filter(state='Pending')
    equipment = Equipment.objects.filter(state='Pending')
    ifta = Ifta.objects.filter(state='Pending')
    contract = Contract.objects.filter(state='Pending')
    audit = Audit.objects.filter(state='Pending')
    driver = Driver.objects.filter(state='Pending')
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Header
    p.setFillColor('#2471A3')
    p.roundRect(0, 790, 694, 60, 10, fill=1)
    p.drawImage('static/img/logoFCI.png', 520, 795, width=70, height=45)

    p.setFont('Helvetica', 14)
    p.setFillColor('#BDBDBD')
    p.drawCentredString(200, 810, "List of pending services")

    #Footer
    p.setFont('Helvetica', 9)
    p.setFillColorRGB(0, 0, 0)
    p.line(0, 50, 800, 50)
    p.drawString(30, 20, 'Date of printing '+time.strftime("%m/%d/%y %H:%M:%S")+' by %s' % request.user.first_name)

    #Boby

    styles = getSampleStyleSheet()
    stylesBH = styles["Heading3"]
    stylesBH.alignment = TA_CENTER
    stylesBH.fontSize = 10
    stylesBH.fill = '#34495E'
    customer = Paragraph('''Customer''', stylesBH)
    service = Paragraph('''Service''', stylesBH)
    description = Paragraph('''Description''', stylesBH)
    update = Paragraph(''' Last Up Date''', stylesBH)
    user = Paragraph('''Up Date User''',stylesBH)
    data = []
    data.append([customer, service,description, update, user])

    stylesBD = styles["BodyText"]
    stylesBD.alignment = TA_CENTER
    stylesBD.fontSize = 8
    high = 730
    for pr in permit:
     this_permit = [Paragraph(str(pr.customers),stylesBD), Paragraph('Permit',stylesBD), Paragraph(str(pr.name),stylesBD), Paragraph(str(pr.update),stylesBD), Paragraph(str(pr.users),stylesBD)]
     data.append(this_permit)
     high = high - 25
    for i in insurance:
     this_insurance = [Paragraph(str(i.customers),stylesBD), Paragraph('Insurance',stylesBD), Paragraph(str(i.sale_type),stylesBD), Paragraph(str(i.update),stylesBD), Paragraph(str(i.users),stylesBD)]
     data.append(this_insurance)
     high = high - 25
    for e in equipment:
     this_equipment = [Paragraph(str(e.customers),stylesBD), Paragraph('Equipment',stylesBD), Paragraph('Serial Number: '+str(e.serial),stylesBD), Paragraph(str(e.update),stylesBD), Paragraph(str(e.users),stylesBD)]
     data.append(this_equipment)
     high = high - 25
    for it in ifta:
     this_ifta = [Paragraph(str(it.customers),stylesBD), Paragraph('IFTA',stylesBD), Paragraph('Type: '+str(it.type),stylesBD), Paragraph(str(it.update),stylesBD), Paragraph(str(it.users),stylesBD)]
     data.append(this_ifta)
     high = high - 25
    for c in contract:
     this_contrac = [Paragraph(str(c.customers),stylesBD), Paragraph('Contract',stylesBD), Paragraph('Serial: '+str(c.serial),stylesBD), Paragraph(str(c.update),stylesBD), Paragraph(str(c.users),stylesBD)]
     data.append(this_contrac)
     high = high - 25
    for a in audit:
     this_audit = [Paragraph(str(a.customers),stylesBD), Paragraph('Audit',stylesBD), Paragraph('Type: '+str(a.type),stylesBD), Paragraph(str(a.update),stylesBD), Paragraph(str(a.users),stylesBD)]
     data.append(this_audit)
     high = high - 25
    for d in driver:
     this_driver = [Paragraph(str(d.customers),stylesBD), Paragraph('Driver',stylesBD), Paragraph('Name: '+str(d.name),stylesBD), Paragraph(str(d.update),stylesBD), Paragraph(str(d.users),stylesBD)]
     data.append(this_driver)
     high = high - 25
    width, height = A4
    table = Table(data, colWidths=[4 * cm, 2 * cm, 7 * cm, 2.5 * cm, 3.5 * cm])
    #table.setStyle(TableStyle([
    #    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    #    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 20, high)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response