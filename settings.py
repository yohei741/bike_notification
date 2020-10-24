# https://qiita.com/harukikaneko/items/b004048f8d1eca44cba9

import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

# 「settings.py」の相対パスを取得し、joinで「.env」ファイルを指定します。
# dotenv_pathに格納された.envファイルのパスを元に、load_dotenvでファイルの中身を読み取ります
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ID = os.environ.get("ID")
PASS = os.environ.get("PASS")
LINE_TOKEN = os.environ.get("LINE_TOKEN")
