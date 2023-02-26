#
#  Copyright (c) 2023 Grzegorz Jewusiak - jewusiak.pl
#
import json
import os
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import credentials


def read_session_data():
    if not os.path.isfile('session.usos'):
        return None

    with open('session.usos', 'r') as f:
        session_cookie = f.readline()
    return json.loads(session_cookie)


def save_session_id(driver: webdriver):
    cookies = driver.get_cookies()
    for item in cookies:
        if item['name'] == 'PHPSESSID':
            with open('session.usos', 'w') as f:
                f.write(json.dumps(item))
            return


def login_to_usosweb_ui(driver: webdriver):
    driver.delete_all_cookies()
    driver.get(
        "https://cas.usos.pw.edu.pl/cas/login?service=https%3A%2F%2Fusosweb.usos.pw.edu.pl%2Fkontroler.php%3F_action%3Ddla_stud%2Frejestracja%2Fbrdg2%2FwyborPrzedmiotu%26rej_kod%3D6430-WFS-2023L%26callback%3Dg_ed300d68")

    username_input = driver.find_element(By.ID, 'username')
    username_input.clear()
    username_input.send_keys(credentials.usos_login)

    password_input = driver.find_element(By.ID, 'password')
    password_input.clear()
    password_input.send_keys(credentials.usos_password)

    driver.find_element(By.NAME, 'submit').click()


def do_auth(driver):
    session_cookie = read_session_data()
    driver.get("https://usosweb.usos.pw.edu.pl/kontroler.php?_action=news/default")

    if not session_cookie == None:
        print('próba odtworzenia sesji...')
        driver.delete_all_cookies()
        driver.add_cookie(session_cookie)
    driver.get("https://usosweb.usos.pw.edu.pl/kontroler.php?_action=news/default")

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for session alert.')

        alert = driver.switch_to.alert
        alert.dismiss()
        print("alert canceled")
    except TimeoutException:
        print("no alert")

    if driver.find_element(By.XPATH, '//menu-top-item[3]').get_attribute('greyed') == 'true':
        print('brak sesji - logowanie...')
        login_to_usosweb_ui(driver)
        save_session_id(driver)
        print('nowa sesja - zalogowano')
    else:
        print('odtworzono sesję - zalogowano')
