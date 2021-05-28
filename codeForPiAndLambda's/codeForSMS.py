import json
import boto3


def lambda_handler(event, context):
      region = 'ap-southeast-2'
      dynamodb = boto3.client('dynamodb',region_name = region)
      dynamodbResource = boto3.resource('dynamodb', region_name= region)

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
      mobileList = []
      for i in range(len(restrictionItems)):
        consentNo = restrictionItems[i]["consentNo"]
        allocation = restrictionItems[i]["TodaysAllocation"]
        consentNoDict[consentNo] = allocation
      for i in range(len(userItems)):
        mobile = userItems[i]["mobile"]
        consentNo = userItems[i]["Consent number"]
        allocation = consentNoDict[consentNo]
        mobileList.append([mobile, allocation])
    allocation = "42 %"
#for user in mobileList:
    sns = boto3.client('sns')
    sns.publish(
        PhoneNumber='+61405291505',
        Message="Todays allocation is:" + allocation)
