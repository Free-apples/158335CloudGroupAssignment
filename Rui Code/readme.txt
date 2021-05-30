1. go to aws lambda console page, click create function
2. choose Author from scratch,
3. input the basic information, function name,runtime, in this case for sendsms function, I choose python3.6.
4. click to open the permisson part, choose create a new role with basic lambda permissions or use an existing role if you already have one.
5. click the create function buttion.
6. in the funciton create page, we will use code cource and test part.
7. in code source page, click the lambda_funciton.py file, then write the code in the right part of the editor.
8. when finished, click the deploy button to deploy the code for test.
9. setup the IAM permission.for example: I used lambda to call the sns and ses service, so I need setup the IAM permission to allow lambda to access the the sns or ses api,such as send_email or send_sms functions. 

10.test the lambda function. click the test tab, insert the test data of your phone number or email address then run the test, if it success, you should recieve a message or a email.

**important
1.for send email function, you need choose the correct region,otherwise, it does not work.
2. for send email function,aws ses service need verified the reciever's email, if the email did not veridied, it can not be sent.
3. for send sms function, the farmer's phone number format must look like : +641111111111，just this kind of formart can be sent.
