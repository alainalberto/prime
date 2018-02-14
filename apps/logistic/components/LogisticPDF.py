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
    p.setFillColor('#2471A3')
    p.roundRect(0, 750, 694, 120, 20, fill=1)
    p.drawImage('static/img/logoFCI.png', 250, 760, width=150, height=70)

    p.setFont('Helvetica', 28)
    p.setFillColor('#E5E7E9')
    p.drawCentredString(70, 785, "LOAD")

    p.setFillColor('#34495E')
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, 730, 'No. '+str(load.number))

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
   # p.drawString(30, 20, 'Date of printing '+time.strftime("%m/%d/%y %H:%M:%S")+' by %s' % request.user.first_name)

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
    quantity = Paragraph('''Quantity''', stylesBH)
    description = Paragraph('''Description''', stylesBH)
    value = Paragraph('''Unit Price''',stylesBH)
    tax = Paragraph('''Tax %''', stylesBH)
    subtotal = Paragraph('''Subtotal''', stylesBH)
    data = []
    data.append([quantity, description, value, tax, subtotal])

    stylesBD = styles["BodyText"]
    stylesBD.alignment = TA_CENTER
    stylesBD.fontSize = 7
    high = 510
   # for item in descrip:
   #     this_descrip = [item.quantity, item.description, item.value, item.tax, item.subtotal]
  #      data.append(this_descrip)
   #     high = high - 18

    width, height = A4
    table = Table(data, colWidths=[2 * cm, 8 * cm, 4 * cm, 2 * cm])
    table.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
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