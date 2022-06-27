# -*- coding: utf-8 -*-

import os
import re
from bs4 import BeautifulSoup
from palieasyread import easy_read


sylDIV = ' '
wordDIV = '] ['
colorClass = ['b', 'r', 'o', 'g'] * 100
is_colorify = False


def html_to_text(html):
    m = BeautifulSoup(html, 'lxml')
    return m.get_text()


def get_pclass(html):
    m = BeautifulSoup(html, 'lxml')
    if m.p:
        return ' '.join(m.p['class'])
    else:
        return ''


def colorify(sentence, syl_div, word_div):
    words = sentence.split(word_div)
    res = ''
    for word in words:
        if not word:
            continue
        w = ''
        syls = word.split(syl_div)
        for i in range(len(syls)):
            w += f'<span class="{colorClass[i]}">{syls[i]}</span>' + syl_div
        res += w + word_div
    res = f'<b>{res}</b>'
    return res


def main(fin):
    with open(fin, 'r', encoding='utf-8') as fh:
        html = fh.read()

    temp1 = html.split(r'<!-- start of head TOC -->')
    temp2 = temp1[1].split(r'<!-- end of head TOC -->')

    html_head = temp1[0]
    html_toc = temp2[0]
    html_body = temp2[1]

    rex = re.compile(r'#(.*?)">(.*?)</a>', re.I)
    toc_rex = re.findall(rex, html_toc)

    res = html_head
    for line in html_body.splitlines():
        if line.strip().startswith('<a name="'):
            line = line.replace('<a ', '<h2 ').replace('</a>', '</h2>')
        if not line:
            res += line
            continue
        pali_text = html_to_text(line)
        if not pali_text.strip():
            res += line
            continue
        class_name = get_pclass(line)

        easy = easy_read(
            pali_text,
            syl_div=sylDIV,
            word_div=wordDIV,
            show_origin=False)
        if is_colorify:
            easy = colorify(easy, syl_div=sylDIV, word_div=wordDIV)
            bline = f'<p class="{class_name}">{easy}</p>\n'
        else:
            bline = f'{line}\n<p class="{class_name}">{easy}</p>\n'
        res += bline + '\n'

    # misc replace
    res = res.replace(
        '<title>Tīkā > Vinayapiṭaka (ṭīkā) > Dvemātikāpāḷi > Bhikkhupātimokkhapāḷi</title>',
        '<title>Dvemātikāpāḷi - Bhikkhupātimokkhapāḷi</title>')
    res = res.replace('="../pta/textAndMenu.css"', '="textAndMenu.css"')

    # print(toc_rex)
    for k, v in toc_rex:
        res = res.replace(f'{k}"></h2>',
                          f'{k}">{v}</h2>')
    save_html_file = fin.strip('_')
    with open(save_html_file, 'w', encoding='utf-8') as fh:
        fh.write(res)
        print('Wrote', save_html_file)

    # epub gen
    epub = 'Bhikkhupatimokkhapali-easyRead.epub'

    cmdepub = f'pandoc -f html -t epub -c textAndMenu.css -o {epub} {save_html_file}'
    e = os.system(cmdepub)
    if e == 0:
        print('Generating EPUB Done')


if __name__ == '__main__':
    fin = 'vin04t.nrf0.html_'
    main(fin)
