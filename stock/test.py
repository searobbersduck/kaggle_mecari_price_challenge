# import requests
#
# stock_code = '000513'
# year = 2017
# qr = 3
#
# url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%s" \
#       % (stock_code, year, qr)
#
# content = requests.get(url=url)
#
# print('hello world')
#
#
#

import requests
from lxml import html
import pandas as pd
import numpy as np

years = [i for i in range(2006, 2017)]
qrs = [i for i in range(1,5)]

stock_code = '000513'

info = []

columns = []

def extract_columns(row):
      res = row.xpath('td//text()')
      columns = []
      for r in res:
            r = r.strip()
            if len(r) > 0:
                  columns.append(r)
      return columns

for year in years:
      for qr in qrs:
            url = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%s" \
                  % (stock_code, year, qr)
            req = requests.get(url=url)
            # with open('x.html', 'wb') as f:
            #       f.write(content.content)
            tree = html.fromstring(req.content.decode('gbk'))
            rows = tree.xpath('//div[@class="tagmain"]/table[@id="FundHoldSharesTable"]/tr')
            try:
                  col_names = rows[0]
                  columns = extract_columns(col_names)
            except:
                  continue
            rows = rows[1:]

            for row in rows:

                  # info.append(np.array(row.xpath('td//text()')))
                  tmp_list = []
                  # info.append(row.xpath('td//text()'))
                  res = row.xpath('td//text()')
                  for r in res:
                        r = r.strip()
                        if len(r) > 0:
                              tmp_list.append(r)
                  info.append(tmp_list)

print(len(info))

arr = np.array(info)

df = pd.DataFrame(arr, columns=columns)

df = df

df.to_csv('x.csv')

