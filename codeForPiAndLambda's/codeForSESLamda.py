import boto3
from botocore.exceptions import ClientError
import csv
import datetime
import json


def lambda_handler(event, context):
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

    for user in emailList:

        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        SENDER = "meganjanetfreedman@gmail.com"

        # Replace recipient@example.com with a "To" address. If your account
        # is still in the sandbox, this address must be verified.
        RECIPIENT = user[0]

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        # CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        AWS_REGION = "ap-southeast-2"

        # The subject line for the email.
        SUBJECT = "Amazon SES Test (SDK for Python)"

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                     "Your water allocation is: " + user[1]

                     )

        # The HTML body of the email.
        BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])