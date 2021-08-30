import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()

NEW_CODE_WAIT_TIME = 3 * 3600

driver = webdriver.Firefox()


def create_log():
    with open('bot.log', 'w') as log:
        log.write('YYYY-MM-DD HH:MM:SS')


def get_last_code_time():
    with open('bot.log', 'r') as log:
        contents = log.readlines()
    last_line = contents[len(contents) - 1]
    if last_line != 'YYYY-MM-DD HH:MM:SS':
        timestamp = last_line[:19]
        last_time = datetime(int(timestamp[:4]), int(timestamp[5:7]), int(timestamp[8:10]), int(timestamp[11:13]), int(timestamp[14:16]), int(timestamp[17:19]))
        delta = datetime.now() - last_time
    else:
        delta = timedelta(seconds=NEW_CODE_WAIT_TIME + 1)
    return delta


def log(message):
    now = str(datetime.now())[:19]
    with open('bot.log', 'a+') as log:
        log.write('\n')
        log.write(f'{now}: {message}')


def login_se_account():
    se_id = os.getenv('SE_ID')
    se_psw = os.getenv('SE_PSW')
    driver.find_element_by_id('sqexid').send_keys(se_id)
    driver.find_element_by_id('password').send_keys(se_psw + Keys.ENTER)


def login_reddit_account():
    re_id = os.getenv('R_ID')
    re_psw = os.getenv('R_PSW')
    driver.find_element_by_id('loginUsername').send_keys(re_id)
    driver.find_element_by_id('loginPassword').send_keys(re_psw + Keys.ENTER)


def nav_to_invite_code():
    driver.get('https://secure.square-enix.com/account/app/svc/mogstation')
    login_se_account()
    WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id('to_service_contract_button2'))
    driver.find_element_by_id('to_service_contract_button2').click()
    driver.find_element_by_id('friend_invitation_banner_button').click()


def get_invite_code():
    invitation_code = driver.find_element_by_class_name('invitation_code').text
    log(f'Invitation Code: {invitation_code}')
    return invitation_code


def get_post(invitation_code):
    with open('post.txt', 'r', encoding='utf-8') as file:
        title = file.readline().strip()
        message = file.readlines()
    title = title.replace('<CODE>', invitation_code)
    del message[0]
    message = ''.join(message).replace('<CODE>', invitation_code)
    return title, message


def format_reddit_msg(message):
    r_message = [line + '\n' for line in message.split('\n') if line.strip() != '']
    return r_message


def nav_to_ffxiv_forum():
    driver.get('https://forum.square-enix.com/ffxiv/threads/272808-Official-Recruit-a-Friend-Code-Thread/')
    driver.find_element_by_id('header_login').click()
    login_se_account()
    WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id('global_normal_search_text'))
    driver.back()
    driver.back()
    driver.back()
    driver.find_element_by_class_name('rescomment_btn').click()


def create_ffxiv_forum_post(message):
    WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id('vB_Editor_001_textarea'))
    driver.find_element_by_id('vB_Editor_001_textarea').send_keys(message)


def post_to_ffxiv_forum():
    driver.find_element_by_id('vB_Editor_001_save').click()
    log(f'FFXIV forum post: {driver.current_url}')


def nav_to_reddit():
    driver.get('https://www.reddit.com/r/ffxivraf/submit')
    login_reddit_account()


def create_reddit_post(title, message):
    WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_tag_name('textarea'))
    driver.find_element_by_tag_name('textarea').send_keys(title)
    driver.find_element_by_css_selector('.public-DraftEditor-content').send_keys(message)


def post_to_reddit():
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[4]/div[3]/div[2]/div/div[1]/button').click()
    time.sleep(3)
    log(f'Reddit post: {driver.current_url}')


def dismiss_popup():
    time.sleep(10)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def main():
    if not os.path.isfile('bot.log'):
        create_log()
    
    last_code_seconds = int(get_last_code_time().total_seconds())
    if last_code_seconds > NEW_CODE_WAIT_TIME:
        nav_to_invite_code()
        invitation_code = get_invite_code()

        post = get_post(invitation_code)
        title = post[0]
        message = post[1]
        r_message = format_reddit_msg(message)

        nav_to_ffxiv_forum()
        create_ffxiv_forum_post(message)
        post_to_ffxiv_forum()

        nav_to_reddit()
        dismiss_popup()
        create_reddit_post(title, r_message)
        post_to_reddit()
    else:
        new_code_time = timedelta(seconds=NEW_CODE_WAIT_TIME - last_code_seconds)
        print(f'A new code should be available in {new_code_time}.')


if __name__ == '__main__':
    main()
