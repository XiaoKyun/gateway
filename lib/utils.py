from . import twilio

# Twilio REST API version
API_VERSION = '2010-04-01'

# Twilio AccountSid and AuthToken
ACCOUNT_SID = 'Twillio account sid'
ACCOUNT_TOKEN = 'Twillio account token'

# Outgoing Caller ID previously validated with Twilio
CALLER_ID = '+1234567890';

# Create a Twilio REST account object using your Twilio account ID and token
account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

def make_call(to, url, from_ = CALLER_ID):
    """
    Make the outgoing call
    """
    return account.request(
        '/{0}/Accounts/{1}/Calls'.format(API_VERSION, ACCOUNT_SID), 
        'POST', { 'From' : CALLER_ID, 'To' : to, 'Url' : url })

def extract_phone_number(address):
    """
    Small function extracting phone number 
    from emails like call+123456@example.net
    returns the number found or None otherwize
    """
    local = address.split("@")[0]
    if '+' not in local:
        return None
    else:
        return '+{0}'.format(local.split('+')[1])
