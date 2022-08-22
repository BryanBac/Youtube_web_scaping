from selenium import webdriver
from bs4 import BeautifulSoup


links = [
    "https://www.youtube.com/watch?v=P-bBKa8Bb_Q"
]


def obtner():
    print("me faltan los likes")
    driver = webdriver.Chrome("chromedriver_win32\\chromedriver.exe")
    driver.get(links[0])
    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, 'lxml')
    duración = soup.findAll("span", class_="ytp-time-duration")
    print(duración[0].text)
    pruebas = soup.findAll("div", class_="top-level-buttons style-scope ytd-menu-renderer")
    for prueba in pruebas:
        print(prueba, "-")
        #  UN NO FUNCIONA
