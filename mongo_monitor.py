import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from pymongo import MongoClient
client = MongoClient()
db=client.ods
collection=db.workzoneSensor
k=0
try:
    for i in collection.find():
        k+=1
    print(datetime.now())
    print("success")
except:
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Timeli Alert<ctrereactor@iastate.edu>"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    recipients=["sknick@iastate.edu","aditya3@iastate.edu","aravindk@iastate.edu"]

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "MongoDB down"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("You are receving this mail as there is an issue with MongoDB used by Timeli application. Please take necessary action."
                )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Alert!!</h1>
      <p>You are receving this mail as there is an issue with MongoDB used by Timeli application. Please take necessary action.</p>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses':recipients
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
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
