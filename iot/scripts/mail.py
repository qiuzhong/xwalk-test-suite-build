#!/usr/bin/env python3

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart

import config


def mail_results(json_file):
    '''
    Read the .json file and mail the results to the administrator.
    '''
    with open(json_file) as fp:
        update_info = json.load(fp)
    
    msg = MIMEMultipart()
    msg['Subject'] = config.OSTRO_RELEASE_NOTIFICATION
    msg['From'] = config.FROM_ADDR
    msg['To'] = config.TO_ADDR
    msg['Cc'] = config.CC_ADDR

    content = '''<html>
                <head>
                </head>
                <body>
                <h1>New Ostro image released!</h1>
                <h2>Last Build Number: {last}</h2>
                <h2>This Build Number: {this}</h2>
                </body>
                </html>'''.format(last = update_info.get('last_build_number'),
                                this = update_info.get('this_build_number'))
    msgtext = MIMEText(content,'html','utf-8')
    msg.attach(msgtext)

    server = smtplib.SMTP(config.SMTP_SERVER)
    server.set_debuglevel(1)
    server.sendmail(config.FROM_ADDR, config.TO_ADDR, msg.as_string().encode('utf-8'))
    server.quit()


if __name__ == '__main__':
    json_file = 'ostro_build_number.json'
    mail_results(json_file)