from io import BytesIO
import time
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Paragraph, Table, TableStyle
from apps.logistic.models import *

def LoadPDF(request, pk):
    load = Load.objects.get(id_lod=pk)
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Header
    p.setFillColor('#B40404')
    p.roundRect(0, 720, 694, 10, 5, fill=1)


    p.setFont('Helvetica', 28)
    p.setFillColor('#000')
    p.drawCentredString(70, 785, "LOAD")

    p.setFillColor('#34495E')
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, 760, 'No. ' + str(load.number))

    p.setFont('Helvetica',12)
    p.setFillColorRGB(0,0,0)
    p.drawString(450, 700, 'Pic Up Date: '+str(load.pickup_date))
    p.line(450, 697, 562, 697)

    p.setFont('Helvetica', 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(450, 680, 'Deliver Date: ' + str(load.deliver_date))
    p.line(450, 697, 562, 697)

    #Customer
    # if customer.company_name:
    p.setFillColor('#34495E')
    p.setFont('Helvetica-Bold', 14)
     #   p.drawString(50, 650, customer.company_name)
    #if customer.fullname:
    p.setFont('Helvetica-Bold', 12)
     #   p.drawString(50, 630, customer.fullname)
    #if customer.address:
    p.setFont('Helvetica', 12)
    #    p.drawString(50, 610, customer.address)
   # if customer.phone:
    p.setFont('Helvetica', 12)
     #   p.drawString(50, 590, customer.phone)


    #Footer
    p.setFont('Helvetica', 9)
    p.setFillColorRGB(0, 0, 0)
    p.line(0, 50, 800, 50)
    p.drawString(30, 20, 'Date of printing '+time.strftime("%m/%d/%y %H:%M:%S")+' by %s' % request.user.first_name)

    #Boby

    p.setFont('Helvetica-Bold', 14)
    #p.drawString(450, 590, "Total: $"+ str(invoice.total))
    p.setFont('Helvetica', 12)
   # p.drawString(450, 570, "Discount: $" + str(invoice.discount))
    p.setFont('Helvetica', 12)
   # p.drawString(450, 550, "Subtotal: $" + str(invoice.subtotal))

    styles = getSampleStyleSheet()
    stylesBH = styles["Heading3"]
    stylesBH.alignment = TA_CENTER
    stylesBH.fontSize = 10
    stylesBH.fill = '#34495E'
    broker = Paragraph('''Customer Name''', stylesBH)
    driver = Paragraph('''Driver''', stylesBH)
    pickupdate = Paragraph('''Pick Up Date''', stylesBH)
    pickupfrom = Paragraph('''Pick Up From''', stylesBH)
    deliver = Paragraph('''Deliver To''', stylesBH)
    loadno = Paragraph('''Load No.''', stylesBH)
    value = Paragraph('''Agreed Amount''', stylesBH)
    data = []
    data.append([broker, driver, pickupdate, pickupfrom, deliver, loadno, value])

    stylesBD = styles["BodyText"]
    stylesBD.alignment = TA_CENTER
    stylesBD.fontSize = 7
    high = 600
    driver = DriversLogt.objects.get(id_dr=load.driver_id)
    colum1 = Paragraph(load.broker, stylesBD)
    colum2 = Paragraph(driver.name, stylesBD)
    colum3 = Paragraph(str(load.pickup_date), stylesBD)
    colum4 = Paragraph(load.pickup_from, stylesBD)
    colum5 = Paragraph(load.deliver, stylesBD)
    colum6 = Paragraph(load.number, stylesBD)
    colum7 = Paragraph(str(load.value), stylesBD)
    this_descrip = [colum1, colum2, colum3, colum4, colum5, colum6, colum7]
    data.append(this_descrip)
    high = high - 36

    width, height = A4
    table = Table(data, colWidths=[3 * cm, 3 * cm, 2 * cm, 3 * cm, 3 * cm, 2 * cm, 2 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, high)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response