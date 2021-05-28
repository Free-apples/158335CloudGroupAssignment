import csv
import datetime
import json
import boto3

from botocore.vendored import requests

# url of a single user
link = 'http://data.ecan.govt.nz/data/133/Water/Consent%20Irrigation%20Restrictions/CSV?RecordNo=@@@@@@@&Today=@D%2F@M%2F@Y'


# user list


def lambda_handler(event, context):
    region = 'ap-southeast-2'
    dynamodb = boto3.client('dynamodb', region_name=region)

    users = ["CRC205005", "CRC192445"]

    today = datetime.datetime.now()
    now = today.strftime("%d/%m/%Y")
    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")

    for x in users:
        url = link.replace('@@@@@@@', x).replace('@D', day).replace('@M', month).replace('@Y', year)
        session = requests.Session()
        raw_data = session.get(url)

        decoded_content = raw_data.content.decode('utf-8')

        reader = csv.reader(decoded_content.splitlines(), delimiter=',')

        next(reader)
        next(reader)
        for row in reader:
            irr_id = x
            date = now
            today_flow = row[9]
            tomo_flow = row[11]
            trig_level = row[16]
            today_alloc = row[17]
            tomo_alloc = row[19]

        add_to_db = dynamodb.put_item(
            TableName='WaterRestriction',
            Item={
                'consentNo': {'S': irr_id},
                'Date': {'S': date},
                'TodaysFlow': {'S': today_flow},
                'TomorrowsFlow': {'S': tomo_flow},
                'TodaysAllocation': {'S': today_alloc},
                'TomorrowsAllocation': {'S': tomo_alloc}})

