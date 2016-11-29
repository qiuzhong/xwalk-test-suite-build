#!/usr/bin/env python3

import json
import config

import requests
import mail


def get_latest_ostro_build_number(latest_image_url):
    '''
    Get the latest ostro image build number from latest_image_url.
    '''
    conn = requests.get(latest_image_url)
    # print(conn.status_code)
    version = conn.content
    # print(str(version))

    try:
        number = int(version.decode('utf-8').strip().split('-')[-1])
    except Exception as e:
        print(e)
        return 0

    return number
    

def check_ostro_build_number():
    '''
    Check the Ostro image build number and write the results to OSTRO_CONFIG_FILE. 
    '''
    configuration = None
    with open(config.OSTRO_CONFIG_FILE) as fp:
        configuration = json.load(fp, encoding = "utf-8")

    last_build_number = configuration.get('last_build_number')
    this_build_number = configuration.get('this_build_number')

    number = get_latest_ostro_build_number(config.OSTRO_LATEST_IMAGE_URL)

    update = False
    if number and (number > last_build_number):
        print("New release!")
        update = True
        this_build_number = number
    else:
        print("No new release.")

    data = {}
    data['last_build_number'] = last_build_number
    data['this_build_number'] = this_build_number

    if update:
        with open(config.OSTRO_CONFIG_FILE, "w") as fp:
            json.dump(data, fp, encoding='utf-8', indent = 4)
        
        mail.mail_results(config.OSTRO_CONFIG_FILE)



if __name__ == '__main__':
    check_ostro_build_number()