import base64
import hashlib
import hmac
import urllib

from flask import Flask, render_template, request, redirect, make_response, jsonify, url_for, session
from flask_awscognito import AWSCognitoAuthentication
from flask_cognito_auth import CognitoAuthManager, callback_handler, logout_handler, login_handler
from flask_jwt_extended import set_access_cookies, JWTManager, verify_jwt_in_request, get_jwt_identity, jwt_required, \
    create_access_token
from flask_table import Table, Col, DatetimeCol
from boto3.dynamodb.conditions import Key, Attr
import boto3
import datetime
from flask_bootstrap import Bootstrap
import logging
import jwt
import requests
import json
from datetime import date
from opencage.geocoder import OpenCageGeocode
from PIL import Image
import PIL
from warrant import Cognito


from werkzeug.security import generate_password_hash, check_password_hash

application = Flask(__name__)

application.secret_key = "my super secret keydfhsredhsdthsdtfghwtdjhnsaerz"

application.config['COGNITO_REGION'] = "ap-southeast-2"
application.config['COGNITO_USER_POOL_ID'] = "ap-southeast-2_gpZvNaDq0"
application.config['COGNITO_CLIENT_ID'] = "4i2jg0hkgvb7363ch4570borea"
application.config['COGNITO_CLIENT_SECRET'] = "1qgjvggt8oclpm21v0qbni7j1lm8usrscm2arltgoddearql9832"
application.config['COGNITO_DOMAIN'] = "https://irrigationplanner.auth.ap-southeast-2.amazoncognito.com"
# application.config["ERROR_REDIRECT_URI"] = "page500"        # Optional
# application.config["COGNITO_STATE"] = "mysupersecrethash"   # Optional

application.config['COGNITO_REDIRECT_URI'] = "https://irrigationplanner.com/cognito/callback"  # Specify this url in Callback URLs section of Appllication client settings of User Pool within AWS Cognito Sevice. Post login application will redirect to this URL

application.config['COGNITO_SIGNOUT_URI'] = "https://irrigationplanner.com/" # Specify this url in Sign out URLs section of Appllication client settings of User Pool within AWS Cognito Sevice. Post logout application will redirect to this URL

cognito = CognitoAuthManager(application)
# cognito = CognitoManager(app)
# cognito.init(app)

application.config["JWT_SECRET_KEY"] = "sadlfhbkjadsbfkjasdblfabsnelifhawsli"  # Change this!
jwt = JWTManager(application)


bootstrap = Bootstrap(application)
dynamodb_client = boto3.client('dynamodb', region_name="ap-southeast-2")
today = date.today()

#
# application.add_url_rule('/', 'index', (lambda: root()))
# application.add_url_rule('/farmView', 'farmView', (lambda: farmView()))

# Use @login_handler decorator on cognito login route
@application.route('/cognito/login', methods=['GET'])
@login_handler
def cognitologin():
    pass

# Use @callback_handler decorator on your cognito callback route
@application.route('/cognito/callback', methods=['GET'])
@callback_handler
def callback():
    print("Do the stuff before post successfull login to AWS Cognito Service")

    for key in list(session.keys()):
        print(f"Value for {key} is {session[key]}")
    response = redirect(url_for("farmView"))
    return response

# @application.route('/home', methods=['GET'])
# def home():
#     current_user = session["username"]
#     email = session["email"]
#     return jsonify(logged_in_as=current_user, email=email), 200

# Use @logout_handler decorator on your cognito logout route
@application.route('/cognito/logout', methods=['GET'])
@logout_handler
def cognitologout():
    pass


@application.route('/', methods=['GET', 'POST'])
def root():
    error = None

    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        return render_template('farmView.html')


@application.route('/.well-known/acme-challenge/IsflFAyZVa5XpaRJi2GDdvCa2P18GAtuQ83EHlNlbRw')
def cert():
    response = make_response("IsflFAyZVa5XpaRJi2GDdvCa2P18GAtuQ83EHlNlbRw.cLbPFSWwWpdX2PnKW_0o_AI1NHOa_Tu2pT-py9s1x1A", 200)
    response.mimetype = "text/plain"
    return response




@application.route('/test')
def test():
    region = 'ap-southeast-2'
    #dynamodb = boto3.client('dynamodb', region_name=region)
    dynamodbResource = boto3.resource('dynamodb', region_name=region)

    restrictionTable = dynamodbResource.Table('WaterRestriction')
    restrictions = restrictionTable.scan()
    restrictionItems = restrictions["Items"]
    users = []
    for i in range(len(restrictionItems)):
        tempConsentNo = restrictionItems[i]["consentNo"]
        users.append(tempConsentNo)
    usersTable = dynamodbResource.Table("users")
    usersEmail = usersTable.scan()
    userItems = usersEmail["Items"]
    consentNoDict = {}
    emailList = []
    for i in range(len(restrictionItems)):
        consentNo = restrictionItems[i]["consentNo"]
        allocation = restrictionItems[i]["TodaysAllocation"]
        consentNoDict[consentNo] = allocation
    for i in range(len(userItems)):
        email = userItems[i]["Email address"]
        consentNo = userItems[i]["Consent number"]
        allocation = consentNoDict[consentNo]
        emailList.append([email, allocation])





    print("test")
    response = make_response("IsflFAyZVa5XpaRJi2GDdvCa2P18GAtuQ83EHlNlbRw.cLbPFSWwWpdX2PnKW_0o_AI1NHOa_Tu2pT-py9s1x1A", 200)
    response.mimetype = "text/plain"
    return response



@application.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        #Deal with tables
        loginInfo = request.form
        email = loginInfo["email"]
        consentNo = loginInfo["consentNumber"]
        address = loginInfo["address"]
        password = loginInfo["password"]
        fieldAmount = int(loginInfo["fields"])
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        usersTable = dynamodb.Table("users")
        usersTable.put_item(Item={'Email address': email,
                                  'Consent number' : consentNo,
                                  'Address': address})
        restrictionTable = dynamodb.Table("WaterRestriction")
        restrictionTable.put_item(Item={"consentNo": consentNo})
        fieldTable = dynamodb.Table("moistureLevels")
        for i in range(1, fieldAmount):
            fieldTable.put_item(Item={"fieldNo": i, "consentNo" : consentNo})

        email = request.form.get('email')
        password = request.form.get('password')
        consentNumber = request.form.get('consentNumber')
        address = request.form.get('address')
        print(email)
        client = boto3.client('cognito-idp')
        CLIENT_ID = '4i2jg0hkgvb7363ch4570borea'
        CLIENT_SECRET = '1qgjvggt8oclpm21v0qbni7j1lm8usrscm2arltgoddearql9832'
        msg = email + CLIENT_ID
        dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                       msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()

        response = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=d2,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
        )

    return render_template('signup.html')

        #Create user in cognito
        # client = boto3.client('cognito-idp')
        # response = client.admin_create_user(UserPoolId="ap-southeast-2_gpZvNaDq0", Username=email,
        #                                     UserAttributes=[{
        #                                         'Email' : email
        #                                     }],
        #                                     ValidationData=[{
        #                                         'Email': email
        #                                     }],
        #                                     TemporaryPassword='password',
        #                                     ForceAliasCreation=True,
        #                                     MessageAction='RESEND',
        #                                     DesiredDeliveryMediums=[
        #                                          'EMAIL',
        #                                     ])
        #
        # # resp = client.sign_up(
        #     ClientId='4i2jg0hkgvb7363ch4570borea',
        #     Email=email
        # )

        # except client.exceptions.UsernameExistsException as e:
        #     return {"error": False,
        #             "success": True,
        #             "message": "This username already exists",
        #             "data": None}
        # except client.exceptions.InvalidPasswordException as e:
        #
        #     return {"error": False,
        #             "success": True,
        #             "message": "Password should have Caps,\
        #                           Special chars, Numbers",
        #             "data": None}
        # except client.exceptions.UserLambdaValidationException as e:
        #     return {"error": False,
        #             "success": True,
        #             "message": "Email already exists",
        #             "data": None}
        #
        # except Exception as e:
        #     return {"error": False,
        #             "success": True,
        #             "message": str(e),
        #             "data": None}
        #
        # return {"error": False,
        #         "success": True,
        #         "message": "Please confirm your signup, \
        #                         check Email for validation code",
        #         "data": None}
        #return make_response(response)
      #  return render_template("index.html")


@application.route('/farmView', methods=['GET', 'POST'])
# @jwt_required()
def farmView():
    #email = session["email"]
    email = "megan@freedman.co.nz"
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    usersTable = dynamodb.Table("users")
    userInfo = usersTable.query(KeyConditionExpression=Key("Email address").eq(email))

    userInfo1 = userInfo["Items"]
    consentNo = userInfo1[0]["Consent number"]
    moistureLevelsTable = dynamodb.Table('moistureLevels')
    waterRestrictionTable = dynamodb.Table('WaterRestriction')
    tableItems = []
    restrictionItems = []

    weatherKey = "bef127b111b0b2658b68e27029de01d1"
    geocoderKey = "8bcc85953c2c454ea51476d0fdc1e876"
    geocoder = OpenCageGeocode(geocoderKey)
    address = "Auckland"
    results = geocoder.geocode(address)
    city = "Christchurch"
    lat = results[0]["annotations"]["DMS"]["lat"]
    lng = results[0]["annotations"]["DMS"]["lng"]
    lat = lat.split(" ")[0].strip("°")
    lng = lng.split(" ")[0].strip("°")
    weather1 = requests.get(
        "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lng+"&exclude=minutely,hourly&units=metric&appid=" + weatherKey)
    weather2 = weather1.text
    jsonWeather = json.loads(weather2)
    date = today.strftime("%B %d, %Y")
    currentWeather = jsonWeather["current"]
    rain = currentWeather["weather"]
    rain = rain[0]["description"]
    currentTemperature = int(currentWeather["temp"])
    clouds = currentWeather["clouds"]
    todayIconCode = currentWeather["weather"][0]["icon"]
    todayIcon = "http://openweathermap.org/img/wn/"+todayIconCode +".png"
    todayMinTemp = int(jsonWeather["daily"][1]["temp"]["min"])
    todayMaxTemp = int(jsonWeather["daily"][1]["temp"]["max"])
    tomorrowWeather = jsonWeather["daily"][1]
    tomorrowMinTemp = int(tomorrowWeather["temp"]["min"])
    tomorrowMaxTemp = int(tomorrowWeather["temp"]["max"])
    tomorrowRain = tomorrowWeather["weather"][0]["description"]
    tomorrowIconCode = tomorrowWeather["weather"][0]["icon"]
    tomorrowIcon = 'http://openweathermap.org/img/wn/'+tomorrowIconCode +'.png'
    if clouds > 50:
        cloud = "Cloudy"
    elif clouds <= 50 and clouds > 10:
        cloud = "Partially cloudy"
    else:
        cloud = "Clear Skys"

    for i in range(20):
        moistureData = moistureLevelsTable.query(
            KeyConditionExpression=Key('fieldNo').eq(i) & Key("consentNo").eq(consentNo))
        for data in moistureData["Items"]:
            fieldNo = data["fieldNo"]
            device_data = data["device_data"]
            fieldMoist = device_data["fieldMoist"]
            fieldMoist = fieldMoist["BOOL"]
            tableItems.append(Item(consentNo, fieldNo, fieldMoist))
    moistureLevelsTable = ItemTable(tableItems, classes=["table"])
    waterRestrictionsData = waterRestrictionTable.scan()
    for i in waterRestrictionsData["Items"]:
        restrictionItems.append(i)
    for key in restrictionItems:
        if consentNo == key["consentNo"]:
            restriction = key["TodaysAllocation"]

            return render_template("farmView.html", table=moistureLevelsTable, restriction=restriction,
                                    rain=rain,  date=date, currentTemperature=currentTemperature,
                           tomorrowMinTemp=tomorrowMinTemp, tomorrowMaxTemp=tomorrowMaxTemp, tomorrowRain=tomorrowRain,
                                   cloud=cloud, todayMinTemp=todayMinTemp, todayMaxTemp=todayMaxTemp, todayIcon=todayIcon,
                                   tomorrowIcon=tomorrowIcon, city=city)
    return render_template("farmView.html", restriction="No data to show")


# Declare  table
class ItemTable(Table):
    farmId = Col("Farm Id")
    fieldId = Col("Field ID")
    fieldMoist = Col("Field Moist")

    def get_tr_attrs(self, item):
        status = item.status()
        return {'class': status}


# Get some objects
class Item(object):
    def __init__(self, farmId, fieldId, fieldMoist):
        self.farmId = farmId
        self.fieldId = fieldId
        self.fieldMoist = fieldMoist

    def status(self):
        if self.fieldMoist == False:
            return "table-danger"
        else:
            return "table-success"


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.secret_key = "abc"
    application.config['SESSION_TYPE'] = 'filesystem'
    application.debug = True
    application.run()
