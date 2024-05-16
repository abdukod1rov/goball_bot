# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACb1ecf7674c1dbb8be705816793016334"
auth_token = "c0b0ca01d312de9bbb0e52d1dd46528d"
verify_sid = "VA30f97712189a55a58d09ba58ac58c6b1"
verified_number = "+998908211633"

client = Client(account_sid, auth_token)


def send_message():
    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(verification.status)

    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
    print(verification_check.status)


def send_sms(message):
    message = client.messages.create(from_='+13372849423', to='+998908211633', body=message)
    print(message.sid)

send_sms('Iltimos kodni kiriting!')
