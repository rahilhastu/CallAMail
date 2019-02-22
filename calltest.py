from twilio.rest import Client
import json

# Your Account Sid and Auth Token from twilio.com/console
def call():

    with open('twilioCred.json','r') as cred:
        data = json.load(cred)
        tw = data['twilio']
        sid = tw['account_sid']
        token = tw['account_token']
        # print (sid+" "+token)

    account_sid = sid
    auth_token = token
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                    url='http://demo.twilio.com/docs/voice.xml',
                    to='+919469491919',
                    from_='+919469491919'
                )

    print(call.sid)

def main():
    call()