# Getting absolute path
import os
# Checking for migrations
import sys

# Request for functions
import urllib.request
#
import xml.dom.minidom as minidom
# Authorization for Google APIs
import httplib2
#
import apiclient.discovery
# Returning in Json format
from django.http import JsonResponse
# In order to return Template
from django.views.generic import TemplateView
# Log in and get a service instance of API access
from oauth2client.service_account import ServiceAccountCredentials

# Models
from app.models import Order


def is_migration():
    # Checking for migrations
    return 'makemigrations' in sys.argv or 'migrate' in sys.argv


def read_sheets():
    # Get data from credential.json
    # Path .\static\credential.json
    current_direction = os.path.dirname(os.path.abspath(__file__))
    credential_json = '{}\\static\\credential.json'.format(current_direction)
    # Google sheets id
    spreadsheet_id = '16r9rIrvH3GuZ-GFH9XlVd7mBuy8vwOS0njFraYn1dhE'

    # We log in and get a service instance of API access
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credential_json,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:D100',
        majorDimension='ROWS'
    ).execute()

    return values.get('values')


def get_usd():
    # Link for cbr.ru to get all current currencies
    web = urllib.request.urlopen('https://www.cbr.ru/scripts/XML_daily.asp')

    # Parsing cbr.ru
    dom = minidom.parseString(web.read())
    dom.normalize()

    # Looking for Valute tag
    elements = dom.getElementsByTagName("Valute")

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        if char_code == 'USD':
            return value


def getdata(request):
    # Calling method, which checks for migration
    if is_migration():
        print("First make migrations")

    # Getting values from Google Sheets
    sheet_value = read_sheets()

    # Getting current USDs currency
    usd = get_usd()


    # Saving data in database
    for values in sheet_value:
        i = 0
        for value in values:
            if value == '№':
                break
            if i == 0:
                num = value
                i += 1
            elif i == 1:
                order_num = value
                i += 1
            elif i == 2:
                price_usd = float(value)
                i += 1
            elif i == 3:
                date = value
                price_rub = price_usd * usd
                price_rub = float('{:.2f}'.format(price_rub))
                i += 1
            if i == 4:
                try:
                    # Updating data by id
                    order = Order.objects.get(id=id)
                    order.order_num = order_num
                    order.price_dollar = price_usd
                    order.price_rub = price_rub
                    order.delivery_data = date
                except:
                    # Creating new data
                    order = Order(id=num,
                                  order_num=order_num,
                                  price_dollar=price_usd,
                                  delivery_data=date,
                                  price_rub=price_rub)
                # Saving in database
                order.save()

    # Getting data from database, order by id
    result = Order.objects.order_by('id')
    # Deleting data from database
    if len(result) > len(sheet_value) - 1:
        for i in range(len(sheet_value), len(result) + 1):
            order = Order.objects.get(id=i)
            order.delete()
    # Returning in Json format
    return JsonResponse({"result": list(result.values())})


class Main(TemplateView):
    # Main page
    template_name = "app/main.html"
