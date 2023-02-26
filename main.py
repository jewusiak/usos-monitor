#
#  Copyright (c) 2023 Grzegorz Jewusiak - jewusiak.pl
#

from selenium import webdriver

import auth
import email_sender as es
import places_utils as pu

op = webdriver.ChromeOptions()
op.add_argument('--headless')
op.add_argument('--no-sandbox')
driver = webdriver.Chrome()  # options=op)

if auth.do_auth(driver) is False:
    print('Przerwa techniczna')

available_places = pu.get_available_places(driver)

old_places = pu.read_old_places()

pu.save_available_places(available_places)

pu.process_places(old_places, available_places)

email_required = False

for x in available_places:
    if x['status'] == 'new' or x['diff'] != 0:
        es.send_email(available_places)
        email_required = True
        break
if not email_required:
    print("Nie wysłano; brak zmian.")
