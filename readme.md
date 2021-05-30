###### SET UP SOIL MONITOR
Instructions to set up the soil monitor were followed from here : https://www.instructables.com/Soil-Moisture-Sensor-Raspberry-Pi/ Instructables Circuits (2021).

###### DEPLOY APPLICATION
Instructions adapted from: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html 

1. git clone  https://github.com/Free-apples/158335CloudGroupAssignment 
2. eb init -p python-3.8 irrigation-tracker-application --region ap-southeast-2 
3. eb create irrigation-tracker-env 
4. Go to console, IAM console.  
5. Select roles on left navigation panel.  
6. Select ec2 
7. Select attach policies 
8. Select AmazonDynamoDBFullAcess

###### SETTING UP DYNAMODB TABLES
1.Instructions adapted from : https://docs.aws.amazon.com/iot/latest/developerguide/iot-ddb-rule.html 
2.Create user table tables:  
3.Set Table name: “users” 
4.Set Primary key, partition key, to "Email address" and choose string.  
5.Choose create 
6.Create water restriction table 
7.Set Table name: “WaterRestriction” 
8.Set Primary key, partition key, to "consentNo" and choose string.  
9.Choose create
10.Create Moisture levels table 
11.Set Table name: “moistureLevels”
12.Set Primary key, partition key, to "fieldNo and choose number.
13.Check add sort key 
14.Choose to add sort key: set to "consentNo” and choose number
15.Choose create

###### SET UP SES AND SNS

1. Go to AWS lambda console page, click create function
2. Choose Author from scratch,
3. Input the basic information, function name, runtime, in this case for send SMS function, I choose python3.6.
4. Click to open the permission part, choose create a new role with basic lambda permissions or use an existing role if you already have one.
5. Click the create function button.
6. In the function create page, we will use code source and test part.
7. In code source page, click the Lambda funciton.py file, then write the code in the right part of the editor.
8. When finished, click the deploy button to deploy the code for test.
9. Setup the IAM permission. For example: I used lambda to call the SNS and SES service, so I need setup the IAM permission to allow lambda to access the SNS or SES Api, such as send email or send SMS functions.
 10.Test the lambda function. click the test tab, insert the test data of your phone number or email address then run the test, if it success, you should receive a message or an email.

###### ACCESS DATA FROM ECAN
Create New role on IAM with DynamoDB and Lambda access.
Create a DynamoDB table with created role. Set primary key for user as irri_id.
Create a Lambda function, set run time as Python 3.8
Use code
Deploy the code, then test

###### SET UP COGNITO

Create user pool:
1. Instructions from: https://docs.aws.amazon.com/cognito/latest/developerguide/getting-started-with-cognito-user-pools.html 
2.Create user pool in Amazon Cognito console 
3. Choose required attributes(email) and custom attributes(consent num, city) 
4. Click on manage user pools and choose create app client 
5. Choose app name and tick generate client secret option 
6. Configure awscli: 
7. Instructions from: https://docs.aws.amazon.com/cli/index.html 
8. Create IAM user and acquire aws access and secret user ids 
9. Open command prompt and install latest version of awscli 
10. Run awscli
11. Enter with personal access and secret key 
12. $ aws configure AWS Access Key ID [None]:"key"
13 AWS Secret Access Key [None]: "secret key" 
14. Default region name [None]: ap-southeast-2
15. Default output format [None]: json

###### Create Login and Register pages:

1.Create python virtual environment and run basic flask application using this tutorial: https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3 
2. Make sign in and register @approute functions using Warrant Cognito API to register and authenticate users: https://github.com/capless/warrant#readme 