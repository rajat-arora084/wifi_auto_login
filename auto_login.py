import keyring
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
import os
from configparser import ConfigParser

WIFI = "home_wifi"
WIFI_NAME = "D2-102"


def is_connected_to_home_wifi():

    is_connected = False
    if WIFI_NAME in  subprocess.check_output("netsh wlan show interfaces").decode('utf-8'):
        is_connected = True
    
    return is_connected

def connect_to_wifi():
    
    # # connect to the given wifi network
    os.system(f'''cmd /c "netsh wlan connect name={WIFI_NAME}"''')
    
    # print("If you're not yet connected, try connecting to a previously connected SSID again!")

def get_wifi_credentials():
    wifi_credentials = { 'username' : "", 'password': ""}
    try:
        creds = keyring.get_credential(WIFI, None)
        wifi_credentials['username'] = creds.username
        wifi_credentials['password'] = creds.password
    except:
        raise Exception('Error ocurred while reading credentials from Windows credentials manager')
    return wifi_credentials

def get_config_data():
    config_data = {'login_url_path': '', 'chrome_exe_path': ''}
    try:
        configure = ConfigParser()
        configure.read(r'C:\Users\rajata\Desktop\auto-login\config.ini')
        config_data['login_url_path'] = configure.get('installation', 'login_url')
        config_data['chrome_exe_path'] = configure.get('installation', 'chrome_exe_path')

    except:
        raise Exception('Error while reading configuration')
    return config_data


def login_to_service_provider(credentials, config):
    try:
        chrome_driver = webdriver.Chrome(executable_path=config.get('chrome_exe_path'))    
        chrome_driver.get(config.get('login_url_path'))
        time.sleep(10)
        chrome_driver.find_element_by_name("username").send_keys(credentials.get('username'))
        chrome_driver.find_element_by_name("password").send_keys(credentials.get('password'))
        time.sleep(5)
        all_input_elements = chrome_driver.find_elements_by_tag_name("input")
        all_input_elements[5].click() #hard coded.
    except:
        raise Exception('Error ocurred while logging in the user.')

def main():
    try:
        credentials = get_wifi_credentials() or {}
        is_connected = is_connected_to_home_wifi()
        config = get_config_data()
        print(credentials, is_connected, config)
        connect_to_wifi()
        login_to_service_provider(credentials, config)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    main()
