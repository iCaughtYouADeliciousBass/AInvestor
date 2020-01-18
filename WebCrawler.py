import requests
import lxml.html as lh
import pandas as pd


URL = "https://www.gurufocus.com/stock_list.php?m_country[]=USA&n=21000"
page = requests.get(URL)

doc = lh.fromstring((page.content))

tr_elements = doc.xpath('//tr')
