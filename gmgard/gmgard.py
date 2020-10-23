import time
import os
import json

from nonebot import on_command, CommandSession
from hoshino import Service

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


sv = Service('gmgard')

    
def get_login_info():
    print('get_login_info')
    with open(r"hoshino\modules\gmgard\gmgard.json", "r", encoding='utf-8') as f:
        checkin_info = json.load(f)
    i = 0
    cookie_list = []
    user_list = []
    url = checkin_info['URL_GMGARD']
    for user_name in checkin_info['USER'].keys():
        i += 1
        user_list.append(user_name)
        cookie_list.append(checkin_info['USER'][user_name])
    return user_list, cookie_list, url


def login(browser, cookie, url):
    print('login')
    browser.get(url)
    browser.add_cookie(cookie)
    browser.get(url)
    assert '紳士の庭' in browser.title
    return browser
    
    
def do_checkin(browser):
    print('do_checkin')
    process_msg = ''
    try:
        browser.find_element_by_id('checkin').click()
    except NoSuchElementException:
        process_msg = f"未发现签到按钮，推测已签到。"
    try:
        time.sleep(1)
        checkin_retry_times = 0
        while True:
            checkin_result = browser.find_element_by_id('checkw').text
            if checkin_result == '点此签到' and checkin_retry_times < 2:
                browser.refresh()
                checkin_retry_times += 1
            elif checkin_result != '点此签到':
                process_msg += checkin_result
                break
            elif checkin_retry_times >= 2:
                process_msg += f"未成功签到请手动确认!" 
                break
    except NoSuchElementException:
        process_msg += f"签到异常，手动确认！"
    return process_msg, browser


@sv.scheduled_job('cron', hour='00', minute='05')
async def gmgard_auto_checkin():
    browser = webdriver.Chrome()
    login_info = get_login_info()
    user_list = login_info[0]
    cookie_list = login_info[1]
    url = login_info[2]
    for i in range(0,len(user_list)):
        user_cookie = cookie_list[i]
        login(browser, user_cookie, url)
        do_checkin(browser)[0]
    browser.quit()


@sv.on_command('gmgard_checkin', aliases=('g签到'), only_to_me=False)
async def gmgard_checkin(session: CommandSession):
    await session.send(f"gmgard开始执行签到...")
    browser = webdriver.Chrome()
    login_info = get_login_info()
    user_list = login_info[0]
    cookie_list = login_info[1]
    url = login_info[2]
    print(user_list, url)
    msg = ''
    for i in range(0,len(user_list)):
        user_cookie = cookie_list[i]
        msg += f"用户：{user_list[i]}，"
        login(browser, user_cookie, url)
        msg += f"{do_checkin(browser)[0]}\n"
    await session.send(msg)
        
    browser.quit()


@sv.on_command('gmgard_checkin_status', aliases=('g签到状态'), only_to_me=False)
async def gmgard_checkin(session: CommandSession):
    await session.send(f"正在获取所有用户的签到情况请稍等。。。")
    browser = webdriver.Chrome()
    login_info = get_login_info()
    user_list = login_info[0]
    cookie_list = login_info[1]
    url = login_info[2]
    msg = ''
    for i in range(0,len(user_list)):
        user_cookie = cookie_list[i]
        msg += f"用户：{user_list[i]}，"
        login(browser, user_cookie, url)
        try:
            checkin_result = browser.find_element_by_id('checkw').text
            if checkin_result == '点此签到':
                msg += f"未签到\n"
            elif '连续' in checkin_result:
                msg += f"{checkin_result}\n "
            else:
                msg += f"获取状态异常，请手动查看！\n"
        except NoSuchElementException:
            msg += f"获取状态异常，请手动查看！\n"
    await session.send(msg)
        
    browser.quit()
