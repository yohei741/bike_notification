import json
import sys
import urllib.parse
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import os

# # ローカルで動かすときのみ、アクティブにする
# import settings
# ID = settings.ID
# PASS = settings.PASS
# LINE_TOKEN = settings.LINE_TOKEN

# ログイン画面を立ち上げ
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get("https://www.e-license.jp/el25/?abc=LAtcyKgwukI%2BbrGQYS%2B1OA%3D%3D&senisakiCd=5")

# ログイン情報を入力
elem_username = browser.find_element_by_id("m01a_b_studentId")
elem_username.send_keys(os.environ.get("ID",ID))
elem_pw = browser.find_element_by_name("b.password")
elem_pw.send_keys(os.environ.get("PASS",PASS))

# ログインボタンを押下
elem_login_btn = browser.find_element_by_id("m01a_login")
elem_login_btn.click()

# 技能予約ページへ遷移（１週目）
elem_serve_page = browser.find_element_by_link_text("技能予約")
elem_serve_page.click()

# １週目のページ情報を取得
elems_text = browser.page_source

# 2週目ページへ遷移
elem_next_page = browser.find_element_by_link_text("次週")
elem_next_page.click()

# 2週目のページ情報を取得
elems_text += browser.page_source

# 最終予約時点のindexを取得
# 予約がない場合は、「-1」を返す（find関数のルール）
idx_last = max(elems_text.rfind("JX") , elems_text.rfind("XJ"))

# 最終予約以降の情報に絞り込み
if idx_last!=-1:
    elems_text = elems_text[idx_last:]


# LINE通知を行うスニペット
LINE_TOKEN=os.environ.get("LINE_TOKEN",LINE_TOKEN)
LINE_NOTIFY_URL="https://notify-api.line.me/api/notify"

def send_line_push():
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    payload = {"message": "技能予約に空きが出ました！"}
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)

# もし空き「OX or XO」があれば、LINE通知する
if elems_text.count("OX")!=0 or elems_text.count("XO")!=0:
    send_line_push()
