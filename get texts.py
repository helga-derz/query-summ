# -*- coding: utf-8 -*-

import parsers.interfax as interfax

pInter = interfax.Interfax()

f = pInter.get_news('02.02.2016', '02.02.2016')[0].text
print(f.encode('utf-8').decode())


'''
n = 0

for i in pInter.get_news('02.02.2016', '02.03.2016'):

    f = i.url + '\n' + i.publ_date + '\n' + i.publ_time + '\n' + i.text

    open('sport/text_' + str(n) + '.txt', 'w', encoding='utf-8').write(f)
    n += 1
'''
