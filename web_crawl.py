from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup

#값들을 넣어줄 TopChamp 생성
TopChamp=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

#url은 ASCII 코드값만 사용하므로 quote 함수로 인코딩 해주어야함
Myname=parse.quote(input("소환사명을 입력해주세요! : "))

#동일하게 적용되는 url부분
urlbase="https://www.op.gg/summoner/champions/userName="

#기존의 url과 입력받은 값을 합하여 완전한 url생성
url=urlbase+Myname

#url을 웹문서 형태로 html에 저장
html=urlopen(url)

#html을 BeautifulSoup 객체로 저장
#BeautifulSoup는 웹문서를 파싱해줌 (json 파싱)
bs=BeautifulSoup(html,"html.parser")

#0번째 열 -> 챔피언에 대한 주소 (상대하기 쉬운 챔피언, 카운터 챔피언 확인용)
#1번째 열 -> 챔피언 이름
for champ in bs.select("tr.Row.TopRanker td.ChampionImage.Cell a"):
    TopChamp[0].append("https://www.op.gg"+champ.get("href"))
    TopChamp[1].append(champ.text.strip())

#2번째 열 -> 승리
#3번째 열 -> 패배
#4번째 열 -> 승률
for game in bs.select("tr.Row.TopRanker div.WinRatioGraph"):
    if game.text.strip().find("W")==-1:
        TopChamp[2].append(0)
        TopChamp[3].append(game.text.strip().split("\n\n")[0].replace("L",""))
        TopChamp[4].append(game.text.strip().split("\n\n")[1])
    elif game.text.strip().find("L")==-1:
        TopChamp[2].append(game.text.strip().split("\n\n")[0].replace("W",""))
        TopChamp[3].append(0)
        TopChamp[4].append(game.text.strip().split("\n\n")[1])
    else:
        TopChamp[2].append(game.text.strip().split("\n\n")[0].replace("W",""))
        TopChamp[3].append(game.text.strip().split("\n\n")[1].replace("L",""))
        TopChamp[4].append(game.text.strip().split("\n\n\n")[1])

#5번째 열 -> 킬
#6번째 열 -> 데스
#7번째 열 -> 어시스트
for grade in bs.select("tr.Row.TopRanker div.KDA"):
    TopChamp[5].append(grade.text.strip().split(" /\n\t\t\t\t\t\t")[0])
    TopChamp[6].append(grade.text.strip().split(" /\n\t\t\t\t\t\t")[1])
    TopChamp[7].append(grade.text.strip().split(" /\n\t\t\t\t\t\t")[2])

#8번째 열 -> KDA
for kda in bs.select("tr.Row.TopRanker td.KDA.Cell"):
    TopChamp[8].append(kda.get("data-value"))

#나머지 열에 대한 정보는 모두 한 클래스에 속해 있으므로 객체를 생성
remainder=[]
for remain in bs.select("tr.Row.TopRanker td.Value.Cell"):
    remainder.append(remain.text.strip())

#9번째 열 -> 평균 획득 골드
#10번째 열 -> 평균 CS
#11번째 열 -> 최대 킬
#12번째 열 -> 최대 데스
#13번째 열 -> 평균 가한 피해량
#14번째 열 -> 평균 받은 피해량
#15번째 열 -> 더블킬
#16번째 열 -> 트리플킬
#17번째 열 -> 쿼드라킬
#18번째 열 -> 펜타킬
for index in range(0,int((len(remainder))/10)):
    TopChamp[9].append(remainder[index*10])
    TopChamp[10].append(remainder[index*10+1])
    TopChamp[11].append(remainder[index*10+2])
    TopChamp[12].append(remainder[index*10+3])
    TopChamp[13].append(remainder[index*10+4])
    TopChamp[14].append(remainder[index*10+5])
    TopChamp[15].append(remainder[index*10+6])
    TopChamp[16].append(remainder[index*10+7])
    TopChamp[17].append(remainder[index*10+8])
    TopChamp[18].append(remainder[index*10+9])

import numpy as np
import pandas as pd

colnames=["Champurl","Champ","Win","Lose","Winrate","Kill","Death","Assist",
          "Kda","Gold","CS","Maxkill","Maxdeath","Adi","Adr","2k","3k","4k","5k"]

DF=pd.DataFrame({
    "ChampUrl":TopChamp[0],
    "Champ":TopChamp[1],
    "Win":TopChamp[2],
    "Lose":TopChamp[3],
    "WinRate":TopChamp[4],
    "Kill":TopChamp[5],
    "Death":TopChamp[6],
    "Assist":TopChamp[7],
    "Kda":TopChamp[8],
    "Gold":TopChamp[9],
    "CS":TopChamp[10],
    "MaxKill":TopChamp[11],
    "MaxDeath":TopChamp[12],
    "ADI":TopChamp[13],
    "ADR":TopChamp[14],
    "2K":TopChamp[15],
    "3K":TopChamp[16],
    "4K":TopChamp[17],
    "5K":TopChamp[18]
    })

DF.to_csv("test.csv")
