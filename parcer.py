from selenium import webdriver
from selenium.webdriver.common.by import By
from currency_converter import CurrencyConverter
from datetime import date, datetime
import csv
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QWidget, QTextEdit

Form, Window = uic.loadUiType("urlputparcer.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
errorWindow = QMessageBox()

converter = CurrencyConverter()
now = datetime.now()

def pushed():
    path_to_chromedriver = 'D:\work\buff163-parcer\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)

    url = form.textEdition.toPlainText()
    browser.get(url)

    itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

    steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
    steamPriceStrRemoveLastOne = steamPriceStr[:-1]
    steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
    steamPrice = float(steamPriceStrRemoved)

    itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
    itemPriceStrRemoved = itemPriceStr[2:]
    itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)

    finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)

    # print('Steam price - $', steamPrice)
    # print('Item price - $', itemPrice)
    # print('Income -', finalPercentage, '%')

    steamPricePrepared = str(steamPrice).replace(".", ",")
    itemPricePrepared = str(itemPrice).replace(".", ",")
    finalPercentagePrepared = str(finalPercentage).replace(".", ",")

    # browser.close()

    # dateTime = now.strftime('%d.%m.%Y %H.%M.%S')
    with open(r'oxis.csv', 'a') as file:
        file.write(itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + url + '\n')

form.put.clicked.connect(pushed)

app.exec()