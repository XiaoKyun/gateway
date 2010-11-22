"""
This is a demo email to voice gateway using
Twillio and Mailgun. README will help you to understand
how to setup this code.
"""

from flask import Flask, render_template, request, abort, url_for
from lib.utils import make_call, extract_phone_number
from email.utils import parseaddr
from threading import Timer
from functools import partial
from imaplib import IMAP4_SSL
from email.parser import Parser

app = Flask(__name__)

@app.route('/messages/', methods=['GET', 'POST'])
def new_message():
    """
    This callback is executed whenever 
    email arrives to call+phone@yourdomain.com
    """
    message_id = request.form['Message-Id']
    recipient = request.form['recipient']    
    number = extract_phone_number(recipient)
    if not number:
        abort(500, "Invalid recipient format: {0}".format(number))
    else:
        app.logger.debug("Call to: {0}, message id: {0}".format(number, message_id))
        call_to(number, message_id)
        return 'Thanks'


@app.route('/read_message/<message_id>', methods=['GET', 'POST'])
def read_message(message_id):
    """
    Once Twillio establishes the call you get
    this callback executed. Here we retrieve 
    the message from the mailbox and generate 
    twiml saying it's contents
    """
    app.logger.debug("Request to read message by id {0}".format(message_id))
    message = get_message(message_id)

    subject = message.get('subject', '')
    body = message.get_payload()
    from_ = message.get('From')

    if message:
        return render_template('read_message.xml', from_ = from_, body = body, subject = subject)
    else:
        return render_template('error.xml')


def get_message(message_id):
    """
    Here we loging via IMAP to our storage mailbox
    and retrieving the message by id
    """
    mailbox = IMAP4_SSL('mailgun.net')
    mailbox.login('storage@example.com', 'password123')
    mailbox.select()
    typ, data = mailbox.search(None, '(HEADER "Message-Id" "{0}")'.format(message_id))
    for num in data[0].split():
        typ, data = mailbox.fetch(num, '(RFC822)')
        return Parser().parsestr(data[0][1], headersonly = False)
    return None

def call_to(number, message_id):
    """
    Just a helper function to initiate call via Twillio
    """
    try:
        make_call(number, url_for('read_message', message_id = message_id, _external = True))
    except Exception, e:
        app.logger.exception("Failed to initiate a call {0}: {1}".format(number, e.read()))


if __name__ == '__main__':
    """
    These lines allow you to launch test server
    listenning on the port 5432 in debug mode,
    just type in console:
    > python gateway.py
    Read more at Flask website
    """
    app.run(host='0.0.0.0', port=5432, debug = True)

