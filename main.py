#
#  Copyright (c) 2023 Grzegorz Jewusiak - jewusiak.pl
#

import auth
from selenium import webdriver
from selenium.webdriver.common.by import By
import places_utils as pu
import email_sender as es


op = webdriver.ChromeOptions()
op.add_argument('--headless')
op.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=op)

auth.do_auth(driver)

courses = ['6430-00000-000-0025', '6430-00000-000-0007']

available_places = pu.get_available_places(driver, courses)

old_places = pu.read_old_places()

pu.save_available_places(available_places)

pu.process_places(old_places, available_places)

email_required=False

for x in available_places:
    if x['status']=='new' or x['diff']!=0:
        es.send_email(available_places)
        email_required=True
        break
if not email_required:
    print("Nie wysłano; brak zmian.")