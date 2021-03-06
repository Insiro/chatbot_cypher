from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
from bs4 import BeautifulSoup

defualtList = ['랭킹', '전적검색', '오싸']


def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': defualtList
    })


status = 0
season = 13
charactor = {'로라스': 'loras', '휴톤': 'huton', '루이스': 'louis', '타라': 'tara', '트리비아': 'trivia', '카인': 'cain',
             '레나': 'rena', '드렉슬러': 'drexler', '도일': 'doyle', '토마스': 'thomas', '나이오비': 'niobe', '시바포': 'shiva',
             '시바': 'shiva', '시바 포': 'shiva', '웨슬리': 'wesley', '스텔라': 'stella', '엘리셔': 'alicia', '클레어': 'clare',
             '다이무스': 'deimus', '이글': 'eagle', '미를렌': 'marlene', '샬럿': 'charlotte', '윌라드': 'willard', '레이튼': 'lleyton',
             '미쉘': 'michelle', '린': 'rin', '빅터': 'viktor', '카를로스': 'carlos', '호타루': 'hotaru', '트릭시': 'trixie',
             '히카로드': 'ricardo', '까미유': 'camille', '자네트': 'jannette', '피터': 'peter', '아이작': 'issac', '레베카': 'rebecca',
             '엘리': 'ellie', '마틴': 'martin', '브로스': 'bruce', '미아': 'mia', '드니스': 'denise', '제레온': 'gereon', '루시': 'lucy',
             '티엔': 'tian', '하랑': 'harang', 'J': 'j', 'j': 'j', '제이': 'j', '벨져': 'belzer', '리첼': 'richel', '리사': 'risa',
             '릭': 'rick', '제키엘': 'jekiel', '탄야': 'tanya', '캐럴': 'carol', '라이샌더': 'lysander', '루드빅': 'ludwig',
             '멜빈': 'melvin', '디아나': 'diana', '클리브': 'clive', '헬레나': 'helena', '에바': 'eva', '론': 'ron', '레오노르': 'leonor',
             '시드니': 'sidney'
             }


def btnRespone(respone, botton):
    return JsonResponse({
        'message': {'text': respone},
        'keyboard': {
            'type': 'buttons',
            'buttons': botton
        }
    })


def textRespone(respone):
    return JsonResponse({
        'message': {
            'text': respone
        },
        'keyboard': {
            'type': 'text'
        }
    })


def mainSelect(data):
    global status
    if data == '랭킹':
        status = '랭킹'
        return btnRespone('어떤 랭킹을 조회하시겠습니까', ['통합', '투신', '캐릭터'])
    elif data == '전적검색':
        status = '전적'
        return textRespone('닉네임을 공백 없이 입력하시오')
    elif data == '오싸':
        link = 'http://cyphers.nexon.com/cyphers/article/today2/1'
        req = requests.get(link)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        strs = ''
        tags = '#container > div.content > div.content_board > div.comm_today > div > ul > li'
        i = 0
        for tag in soup.select(tags):
            if i == 4:
                break
            strs += str(tag.text) + '\n'
            i += 1
        contents = strs
        return btnRespone(contents, defualtList)


def rankSelect(data):
    global status
    if data == '투신':
        status = 0
        contents = parseFight()
        return btnRespone(contents, defualtList)
    elif data == '통합':
        status = 0
        contents = parseRank()
        return btnRespone(contents, defualtList)
    elif data == '캐릭터':
        status = '캐릭랭킹'
        return textRespone('캐릭터의 이름을 입력하시오')


def charRank(data):
    global status
    if data in charactor.keys():
        status = 0
    else:
        return textRespone('존재하지 않는 이름입니다.\n올바른 캐릭터명을 입력하시오')
    link = 'http://cyphers.nexon.com/cyphers/article/ranking/charac/13/' + charactor.get(data) + '/win/day/1'
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    tags = '#rankCharacForm > div.rank_board.mar_b10 > table > tbody > tr > td'
    i = 0
    j = 0
    str2 = ''
    for tag in soup.select(tags):
        if i == 0:
            i += 1
            if j != 0:
                str2 += '\n'
            str2 += str(j + 1)
        elif i == 1:
            str2 += ' ' + tag.text[:7] + ' '
            i += 1
        elif i == 4:
            i = 0
            j += 1
            str2 += ''.join(tag.text[4:].split(' '))
        else:
            i += 1
            continue
    print(str2)
    contents = str2
    return btnRespone(contents, defualtList)


def parseHistory(data):
    link = 'http://cyphers.nexon.com/cyphers/game/log/search/1/' + data
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    con = '이름이 잘못되었습니다'
    tag_WL = "#container > div.content > div.record > div.record_new > table > thead > tr > th > span > img"
    tag_C = "#container > div.content > div.record > div.record_new > table > tbody > tr > td > p"
    strs = []
    strs = []
    for tag in soup.select(tag_WL):
        strs.append(str(tag)[10:12])
    j = 0
    i = -1
    for tag2 in soup.select(tag_C):
        if (j % 2 == 0):
            j += 1
            continue
        stsr = tag2.text.split()
        strs[i] += " " + "%-4s" % stsr[1] + "\t" + stsr[3][0:2]
        j += 1
        i += 1
    if j != 0:
        con = "\n".join(strs)
    return con


def parseFight():
    link = 'http://cyphers.nexon.com/cyphers/article/ranking/gof/f/1'
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    tags = '#container > div.content > div.content_board > div.rank_board.clan_rank.mar_b10 > table > tbody > tr > td'
    i = 0
    j = 0
    str2 = ''
    for tag in soup.select(tags):
        if i == 0:
            i += 1
            if j != 0:
                str2 += '\n'
            str2 += str(j + 1)
        elif i == 1:
            str2 += ' ' + tag.text
            i += 1
        elif i == 2:
            str2 += ' ' + tag.text + ' '
            i += 1
        elif i == 4:
            i = 0
            j += 1
            str2 += ''.join(tag.text[4:].split(' '))
        else:
            i += 1
            continue
    return str2


def parseRank():
    link = 'http://cyphers.nexon.com/cyphers/article/ranking/total/13/1'
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    str1 = ''
    str2 = ''
    j = 1
    i = 0
    for tag in soup.select('#rankTotalForm > div.rank_board.total_rank.mar_b10 > table > tbody > tr > td'):
        if j == 51:
            break
        i += 1
        if i == 2:
            str1 = str(j) + ' ' + tag.text[0:6]
        elif i == 3:
            str1 = str1 + ' ' + tag.text
        elif i == 4:
            str1 = str1 + ' ' + tag.text
        elif i == 5:
            i = 0
            j += 1
            if j != 51:
                str1 += '\n'
            str2 += str1
    print(str2)
    return str2


@csrf_exempt
def answer(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']
    global status
    if status == 0:
        return mainSelect(datacontent)
    elif status == '랭킹':
        return rankSelect(datacontent)
    elif status == '캐릭랭킹':
        return charRank(datacontent)
    elif status == '전적':
        status = 0
        contents = parseHistory(datacontent)
        return btnRespone(contents, defualtList)
