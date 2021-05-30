#python3.6

import logging
import boto3

# Initialize logger and set log level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS client for Ireland region
session = boto3.Session(
    region_name="ap-southeast-2"
)
sns_client = session.client('sns')


def lambda_handler(event, context):

    # Send message
    response = sns_client.publish(
        PhoneNumber=event["phone_number"],
        Message=event["sms_message"],
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'SENDERID'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Promotional'
            }
        }
    )

    logger.info(response)
    return 'OK'

#test********************************************
# phone_number is the farmers phone number it must like: +641111111111
# 
#{
#  "phone_number": "+641111111111",
#  "sms_message": "this a test for ..."
#}


# readme ******************************************
# user need to grant permissions to the function,then it can send sms message using aws sns.
# please add the below json to the IAM roles of the lambda funciton.
# {
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Effect": "Allow",
#            "Action": "sns:Publish",
#            "Resource": "*"
#        }
#    ]
#}