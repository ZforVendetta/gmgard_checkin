import time
import os
import json

from nonebot import on_command, CommandSession
from hoshino import Service

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

sv = Service('gmgard')


@sv.on_command('gmgard_checkin', aliases=('g签到'), only_to_me=False)
async def gmgard_checkin(session: CommandSession):
    await session.send(f"gmgard开始执行签到...")
    with open(r"hoshino\modules\gmgard\gmgard.json", "r", encoding='utf-8') as f:
        checkin_info = json.load(f)
    i = 0
    get_user_name = ''
    user_cookie = {}
    user_list = []
    for user_name in checkin_info['USER'].keys():
        i += 1
        user_list.append(user_name)
        get_user_name += str(i) +':'+ user_name +';\n'
    for user_name in user_list:
        user_cookie = checkin_info['USER'][user_name]
        msg = f"用户：{user_name}，"
        #开始登录
        browser = webdriver.Chrome()
        browser.get(checkin_info['URL_GMGARD'])
        browser.add_cookie(user_cookie)
        browser.get(checkin_info['URL_GMGARD'])
        assert '紳士の庭' in browser.title
        
        try:
            browser.find_element_by_id('checkin').click()
        except NoSuchElementException:
            msg += f"未发现签到按钮，推测已签到。"
        try:
            time.sleep(1)
            checkin_retry_times = 0
            while True:
                checkin_result = browser.find_element_by_id('checkw').text
                if checkin_result == '点此签到' and checkin_retry_times < 2:
                    browser.refresh()
                    checkin_retry_times += 1
                elif checkin_result != '点此签到':
                    msg += checkin_result
                    break
                elif checkin_retry_times >= 2:
                    msg += f"未成功签到请手动确认!" 
                    break
        except NoSuchElementException:
            msg += f"签到异常，手动确认！"
        await session.send(msg)
        browser.quit()
