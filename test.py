import csv
import datetime
import json
import boto3


from botocore.vendored import requests


region = 'ap-southeast-2'
dynamodb = boto3.client('dynamodb', region_name=region)
dynamodbResource = boto3.resource('dynamodb', region_name=region)

restrictionTable = dynamodbResource.Table('WaterRestriction')
restrictions = restrictionTable.scan()
restrictionItems = restrictions["Items"]
users = []
for i in range(len(restrictionItems)):
    tempConsentNo = restrictionItems[i]["consentNo"]
    users.append(tempConsentNo)

print(users)
