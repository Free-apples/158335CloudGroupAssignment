//nodejs 12
var aws = require('aws-sdk');
var ses = new aws.SES({region: 'ap-southeast-2'});
exports.handler = (event, context, callback) => {
    sendMail(event["toaddress"],event["subject"],event["data"],event["source"]);
};

async function sendMail(toaddress,subject, txtdata,source) {
  const emailParams = {
        Destination: {
          ToAddresses: [toaddress],
        },
        Message: {
          Body: {
            Text: { Data: txtdata },
          },
          Subject: { Data: subject },
        },
        Source: source,
  };
      
  try {
        let key = await ses.sendEmail(emailParams).promise();
        console.log("MAIL SENT SUCCESSFULLY!!");      
  } catch (e) {
        console.log("FAILURE IN SENDING MAIL!!", e);
      }  
  return;
}

//important*************************
// email address must verified in aws ses : 
// https://ap-southeast-2.console.aws.amazon.com/ses/home?region=ap-southeast-2#verified-senders-email:
// the region must choose ap-southeast-2


//test ********************************
//{
//  "toaddress": "your email address",
//  "data": "Riley wanto tell you great",
//  "subject": "Riley it is a import info",
//  "source" : "your source email address"
//}



// readme ******************************************
// user need to grant permissions to the function,then it can send email using aws ses.
// please add the below json to the IAM roles of the lambda funciton.
//{
//    "Version": "2012-10-17",
//    "Statement": [
//        {
//            "Effect": "Allow",
//            "Action": [
//                "ses:SendEmail",
//                "ses:SendRawEmail"
//            ],
//            "Resource": "*"
//        }
//    ]
//}