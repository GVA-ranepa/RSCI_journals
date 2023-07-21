import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#import os
#import pandas as pd
#import time
#from bs4 import BeautifulSoup

# Запускаем драйвер, открываем веб-страницу Журналы
browser = webdriver.Firefox()
browser.get('https://elibrary.ru/titles.asp')

# находим выпадающий список "Сведения о включении в РИНЦ". Выбираем пункт "индекисруется в РИНЦ"
select = Select(browser.find_element("name","risc"))
select.select_by_value('0')

# на странице две кнопки класса butred - "вход" и "Поиск", нажимаем на вторую
buttonArray = browser.find_elements("css selector", ".butred")
# for but in buttonArray:
#     print(but)
buttonArray[1].click()

# на странице выдачи поиска находим количество страниц результатов поиска

lastPage = browser.find_element(By.LINK_TEXT, "В конец")
lastUrl = lastPage.get_attribute('href')
# print(lastUrl)

lastPage.click()

# извлекаем из href номер последней страницы
m = re.search(r'\d{1,4}', lastUrl)
if m:
    totalPages = int(m[0])
#print(totalPages)

# открываем файл на запись, кодировка utf-8 для обработки названий на молдавском, армянском, французском ит.п. языках
with open("res_rsci.txt", "w", encoding="utf-8") as file:
    # перебираем страницы результатов поиска
    for i in range(totalPages-1, totalPages+1):
        # на странице выдачи поиска находим таблицу результатов по id
        resTable = browser.find_element(By.XPATH, "//*[@id='restab']")
        num_rows = len (browser.find_elements(By.XPATH, "//*[@id='restab']/tbody/tr"))
        # print("There are " + repr(num_rows) + " rows in table")
        beforeXPath = "//*[@id='restab']/tbody/tr["
        aftertd_XPath_1 = "]/td[1]"
        aftertd_XPath_2 = "]/td[3]/a"

        for curRow in range(4, num_rows+1):
            curStr = ""
            FinalXPath1 = beforeXPath + str(curRow) + aftertd_XPath_1
            FinalXPath2 = beforeXPath + str(curRow) + aftertd_XPath_2
            # номер журнала в списке результатов
            cell_text1 = browser.find_element(By.XPATH, FinalXPath1).text
            cell_text1 = cell_text1.rstrip(cell_text1[-1])
            # название журнала
            cell_text2 = browser.find_element(By.XPATH, FinalXPath2).text

            curStr = cell_text1 + ';' + cell_text2
            file.write(curStr + '\n')
            # print(curStr)
        # находим и нажимаем ссылку на следующую страницу (если она существует)
        try: 
            nextPage = browser.find_element(By.XPATH, "//*[@id='pages']/table/tbody/tr/td[13]/a")
            i += 1
            nextPage.click()
        except: 
            break

# закрываем браузер
browser.quit()