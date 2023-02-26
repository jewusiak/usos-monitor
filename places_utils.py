#
#  Copyright (c) 2023 Grzegorz Jewusiak - jewusiak.pl
#
import datetime
import json
import os

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

import config


def get_available_places(driver: webdriver):
    avails = []
    for subject in config.courses:
        driver.get(
            f"https://{config.usos_domain}/kontroler.php?_action=dla_stud/rejestracja/brdg2/grupyPrzedmiotu&rej_kod={config.registration_id}&prz_kod={subject}&cdyd_kod={config.semester}&odczyt=1")
        subject_name = driver.find_element(By.XPATH, f"//span[contains(text(), '{subject}')]").text
        rows = driver.find_elements(By.XPATH, "//tr[position()>2 and not(contains(@style,'font-weight: bold;'))]")
        for row in rows:
            cells = row.find_elements(By.XPATH, ".//td")
            avails.append(
                {'subject_id': subject, 'subject_name': subject_name, 'internal_id': subject + '/' + cells[0].text,
                 'group': cells[0].text, 'max': int(cells[3].text),
                 'registered': int(cells[1].text), 'teacher': cells[4].text, 'time': cells[6].text})
    return avails


def save_available_places(places):
    to_save = json.dumps({'time': datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), 'places': places})
    with open('places.usos', 'w') as f:
        f.write(to_save)


def read_old_places():
    if not os.path.isfile('places.usos'):
        return []

    with open('places.usos', 'r') as f:
        data = f.read()

    return json.loads(data)['places']


def process_places(old, new):
    for new_group in new:
        exists = False
        for old_group in old:
            if old_group['internal_id'] == new_group['internal_id']:
                exists = True
                new_group['diff'] = new_group['max'] - new_group['registered'] - (
                        old_group['max'] - old_group['registered'])  # diff > 0 new empty places
                break
        new_group['status'] = 'old' if exists else 'new'
