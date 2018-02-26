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
from apps.logistic.models import DispatchLoadHasLoad, Load, CustomerHasLoad

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

def InvoicesLog(request, pk, start, end):
    invoice = DispatchLoad.objects.get(id_inv=pk)
    customer = Customer.objects.get(id_cut=invoice.customers_id)
    descrip = []
    loadInv = DispatchLoadHasLoad.objects.filter(invoices=invoice)
    for l in loadInv:
        load = CustomerHasLoad.objects.get(loads=l.loads)
        descrip.append(load)
    file = File.objects.filter(folders=customer.folders, name='LOGO', category='Misselenious')
    logo = 'img/logos/trucklogo.jpg'
    if file:
        logo = str(File.objects.get(folders=customer.folders, name='LOGO', category='Misselenious').url)
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Header
    p.setFillColor('#2471A3')
    p.roundRect(0, 750, 694, 120, 20, fill=1)
    p.drawImage('static/media/' + logo, 440, 760, width=150, height=70)

    p.setFont('Helvetica', 16)
    p.setFillColor('#E5E7E9')
    p.drawCentredString(300, 785, customer.company_name)


    p.setFont('Helvetica', 28)
    p.setFillColor('#E5E7E9')
    p.drawCentredString(70, 785, "INVOICE")

    p.setFillColor('#34495E')
    p.setFont('Helvetica-Bold', 12)
    p.drawString(410, 720, 'No: ' + invoice.prefix + "-" + str(invoice.serial))

    p.setFont('Helvetica', 10)
    p.drawImage('static/img/icon/address-o.png', 50, 700, width=10, height=10)
    p.drawString(65, 700, customer.address)
    p.drawImage('static/img/icon/phone-o.png', 50, 680, width=10, height=10)
    p.drawString(65, 680, customer.phone)


    p.setFont('Helvetica', 11)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(410, 700, 'Week Star Date: ' + str(invoice.start_date))
    p.drawString(410, 680, 'Week End Date: ' + str(invoice.end_date))

    #Footer
    p.setFillColor('#2471A3')
    p.roundRect(0, 0, 694, 50, 0, fill=1)
    p.setFont('Helvetica', 9)
    p.setFillColorRGB(0, 0, 0)
    p.line(0, 50, 800, 50)
    p.drawString(30, 20, 'Date of printing '+time.strftime("%m/%d/%y %H:%M:%S"))
    p.setFillColor('#34495E')
    p.setFont('Helvetica', 10)
    p.drawString(200, 60, 'THANK YOU FOR YOUR BUSSINESS!')

    # Boby

    p.setFillColor('#020000')
    p.setFont('Helvetica', 11)
    p.drawString(450, 150, "Subtotal: $" + str(invoice.subtotal))
    p.setFont('Helvetica', 11)
    p.drawString(450, 130, "7% FEE: $" + str(invoice.comission_fee))
    p.setFont('Helvetica', 11)
    p.drawString(450, 110, "WIRE FEE: $" + str(invoice.wire_fee))
    p.setFont('Helvetica', 11)
    p.drawString(450, 90, "ACH FEE: $" + str(invoice.ach_fee))
    p.setFont('Helvetica', 11)
    p.drawString(450, 70, "Others FEE: $" + str(invoice.discount))
    p.setFont('Helvetica-Bold', 12)
    p.drawString(450, 50, "Total: $" + str(invoice.total))

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
    for l in descrip:
        colum1 = Paragraph(l.loads.broker, stylesBD)
        colum2 = Paragraph(l.driver.name, stylesBD)
        colum3 = Paragraph(str(l.loads.pickup_date), stylesBD)
        colum4 = Paragraph(l.loads.pickup_from, stylesBD)
        colum5 = Paragraph(l.loads.deliver, stylesBD)
        colum6 = Paragraph(l.loads.number, stylesBD)
        colum7 = Paragraph(str(l.loads.value), stylesBD)
        this_descrip = [colum1, colum2, colum3, colum4, colum5, colum6, colum7]
        data.append(this_descrip)
        high = high - 18

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