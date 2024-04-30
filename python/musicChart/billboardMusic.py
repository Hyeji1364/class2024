import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

res = req.get("https://www.billboard.com/charts/hot-100/", headers=head)


# print(res.text)
# print(res.status_code)  #406

soup = bs(res.text, "lxml")

# 데이터 선택
ranking = soup.select(".o-chart-results-list-row-container > .o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light  lrv-u-padding-l-1@mobile-max >.c-label  a-font-primary-bold-l u-font-size-32@tablet u-letter-spacing-0080@tablet")
title = soup.select(".lrv-u-width-100p > .c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
artist = soup.select(".lrv-u-width-100p > .c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")


# print(len(ranking))
# print(len(title))
# print(len(artist))

# 데이터 저장
rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a in artist]

#데이터 프레임 생성
chart_df = pd.DataFrame ({
    'Rank': rankingList,
    'Title' : titleList,
    'Artist': artistList
})

# JSON 파일로 저장
chart_df.to_json("billboradChart.json", force_ascii=False, orient="records")