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

def InvoicesLod_pdf(request, pk):
    invoice = Invoice.objects.get(id_inv = pk)
    customer = Customer.objects.get(id_cut=invoice.customers_id)
    descrip = []
    loadInv = InvoicesHasLoad.objects.filter(invoices_id=invoice.id_inv)
    for l in loadInv:
        load = Load.objects.get(id_lod=l.loads_id)
        descrip.append(load)
    business = Busines.objects.get(id_bus=invoice.business_id)
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    #Header
    p.setFillColor('#B40404')
    p.roundRect(0, 720, 694, 10, 5, fill=1)

    if invoice.business.logo:
        p.drawImage('static/media/' + str(invoice.business.logo), 250, 735, width=100, height=100)

    p.setFont('Helvetica', 28)
    p.setFillColor('#000')
    p.drawCentredString(70, 785, "INVOICE")

    p.setFillColor('#34495E')
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, 760, 'No. ' + invoice.prefix + "-" + str(invoice.serial))

    p.setFont('Helvetica', 10)
    p.drawImage('static/img/icon/address-o.png', 50, 700, width=10, height=10)
    p.drawString(65, 700, business.address)
    p.drawImage('static/img/icon/phone-o.png', 50, 680, width=10, height=10)
    p.drawString(65, 680, business.phone)
    if business.fax:
        p.drawImage('static/img/icon/fax-o.png', 50, 660, width=10, height=10)
        p.drawString(65, 660, business.fax)
    if business.email:
        p.drawImage('static/img/icon/Email-o.png', 50, 640, width=10, height=10)
        p.drawString(65, 640, business.email)

    p.setFont('Helvetica',11)
    p.setFillColorRGB(0,0,0)
    p.drawString(410, 700, 'Week Star Date: '+str(invoice.start_date))
    p.drawString(410, 680, 'Week End Date: ' + str(invoice.end_date))


    #Customer
    '''if customer.company_name:
        p.setFillColor('#34495E')
        p.setFont('Helvetica-Bold', 14)
        p.drawString(75, 620, customer.company_name)
        p.drawString(50, 620, 'To:')
    if customer.fullname:
        p.setFont('Helvetica-Bold', 12)
        p.drawString(75, 600, customer.fullname)
    if customer.address:
        p.setFont('Helvetica', 12)
        p.drawString(75, 580, customer.address)
    if customer.phone:
        p.setFont('Helvetica', 12)
        p.drawString(75, 560, customer.phone)'''

    # Footer
    p.setFillColor('#B40404')
    p.roundRect(0, 30, 694, 10, 5, fill=1)
    p.setFont('Helvetica', 9)
    p.setFillColorRGB(0, 0, 0)
    if request.user.first_name:
        user_print = request.user.first_name + " " + request.user.last_name
    else:
        user_print = request.user.username
    p.drawString(30, 20, 'Date of printing ' + time.strftime("%m/%d/%y %H:%M:%S") + ' by %s' % user_print)
    p.setFillColor('#34495E')
    p.setFont('Helvetica', 10)
    if invoice.business.messager:
        p.drawString(200, 60, str(invoice.business.messager))

    #Boby
    p.setFillColor('#58D3F7')
    p.roundRect(445, 145, 120, 20, 0, fill=1)
    p.setFillColor('#FAFAFA')
    p.roundRect(445, 65,120, 80, 0, fill=1)
    p.setFillColor('#A9F5A9')
    p.roundRect(445, 44, 120, 22, 0, fill=1)
    p.setFillColor('#020000')
    p.setFont('Helvetica', 11)
    p.drawString(450, 150, "Subtotal: $" + str(invoice.subtotal))
    if invoice.comission_fee:
        comission_fee = invoice.comission_fee
    else:
        comission_fee = 0
    p.setFont('Helvetica', 11)
    p.drawString(450, 130, "7% FEE: $" + str(comission_fee))
    if invoice.wire_fee:
        wire_fee = invoice.wire_fee
    else:
        wire_fee = 0
    p.setFont('Helvetica', 11)
    p.drawString(450, 110, "WIRE FEE: $" + str(wire_fee))
    if invoice.ach_fee:
        ach_fee = invoice.ach_fee
    else:
        ach_fee = 0
    p.setFont('Helvetica', 11)
    p.drawString(450, 90, "ACH FEE: $" + str(ach_fee))
    if invoice.discount:
        discount = invoice.discount
    else:
        discount = 0
    p.setFont('Helvetica', 11)
    p.drawString(450, 70, "Others FEE: $" + str(discount))
    p.setFont('Helvetica-Bold', 12)
    p.drawString(450, 50, "Total: $" + str(invoice.total))

    styles = getSampleStyleSheet()
    stylesBH = styles["Heading3"]
    stylesBH.alignment = TA_CENTER
    stylesBH.fontSize = 10
    stylesBH.fill = '#34495E'
    broker = Paragraph('''Customer Name''', stylesBH)
    driver = Paragraph('''Driver''', stylesBH)
    pickupdate = Paragraph('''Pick Up Date''',stylesBH)
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
    for l in descrip:
        driver = DriversLogt.objects.get(id_dr=l.driver_id)
        colum1 = Paragraph(l.broker, stylesBD)
        colum2 = Paragraph(driver.name, stylesBD)
        colum3 = Paragraph(str(l.pickup_date), stylesBD)
        colum4 = Paragraph(l.pickup_from, stylesBD)
        colum5 = Paragraph(l.deliver, stylesBD)
        colum6 = Paragraph(l.number, stylesBD)
        colum7 = Paragraph(str(l.value), stylesBD)
        this_descrip = [colum1, colum2 , colum3 , colum4 , colum5 , colum6 , colum7]
        data.append(this_descrip)
        high = high - 36

    width, height = A4
    table = Table(data, colWidths=[3 * cm, 3 * cm, 2 * cm, 3 * cm, 3 * cm, 2 * cm, 2 * cm])
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