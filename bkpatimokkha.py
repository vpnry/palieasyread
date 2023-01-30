# -*- coding: utf-8 -*-

'''Split syllable in Bhikkhupātimokkhapāḷi

Generate Bhikkhupatimokkhapali_syllable_recitation.epub with pandoc

Last updated: 30 Jan 2023
'''

import os
import re
from bs4 import BeautifulSoup
from palieasyread import easy_read

from javascript import require  # pip3 install javascript
PSC = require('@pnfo/pali-converter')  # npm install -g @pnfo/pali-converter
# convertMixed = PSC.convertMixed #  https://github.com/pnfo/pali-converter
convert = PSC.convert
print(convert('mettā', 'my', 'ro'))


sylDIV = ' '
wordDIV = ' _ '
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
    save_html_file = fin.strip('_')
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

    note = f'''<div style="border: grey solid 1px">
<ul>
Note:
<br>
<li>The Roman pāḷi text is from this VRI version https://www.tipitaka.org/romn/cscd/{save_html_file.replace('.html', '.xml')}</li>

<li>Pāḷi script converter https://github.com/pnfo/pali-converter</li>

<li>Pāḷi syllable splitting lines are generated using this script https://github.com/vpnry/palieasyread</li>

<li>This file and a recitation audio can be downloaded from: https://github.com/vpnry/patimokkha_recitation</li>

<li>The syllable spliting lines may not be 100% perfect, but it can be helpful for beginners to follow along the recitation audio by the Sayadaw. When you are pretty familiar with the pronunciation and rhythm, it is better to use the normal writing words directly.</li>
<li>This Dhamma material is for free distribution only.</li>
</ul>
</div>
<br><br>
'''
    res += note
    for line in html_body.splitlines():
        if line.strip().startswith('<a name="'):
            line = line.replace('<a ', '<h2 ').replace('</a>', '</h2>')
        if not line:
            res += line
            continue
        pali_ro_text = html_to_text(line)

        pali_mm_text = convert(pali_ro_text, 'my', 'ro')

        if not pali_ro_text.strip():
            res += line
            continue
        class_name = get_pclass(line)

        easy = easy_read(
            pali_ro_text,
            syl_div=sylDIV,
            word_div=wordDIV,
            show_origin=False)
        if is_colorify:
            easy = colorify(easy, syl_div=sylDIV, word_div=wordDIV)
            bline = f'<p class="{class_name}">{pali_mm_text.replace(".", "။")}</p>\n{line}\n<p class="{class_name}">{easy}</p>\n'
        else:
            bline = f'<p class="{class_name}">{pali_mm_text.replace(".", "။")}</p>\n{line}\n<p class="{class_name}">{easy}</p>\n'
        res += bline + '\n'

    # misc replace
    res = res.replace(
        '<title>Tīkā > Vinayapiṭaka (ṭīkā) > Dvemātikāpāḷi > Bhikkhupātimokkhapāḷi</title>',
        '<title>Dvemātikāpāḷi - Bhikkhupātimokkhapāḷi</title>')
    res = res.replace('="../pta/textAndMenu.css"', '="textAndMenu.css"')

    with open('textAndMenu.css', 'r', encoding='utf-8') as fi:
        css = fi.read()

    css = f'<style>\n{css}\n</style>'
    res = res.replace('</head>', f'{css}\n</head>')

    # print(toc_rex)
    for k, v in toc_rex:
        res = res.replace(f'{k}"></h2>',
                          f'{k}">{v}</h2>')

    with open(save_html_file, 'w', encoding='utf-8') as fh:
        fh.write(res)
        print('Wrote', save_html_file)

    # epub gen
    epub = 'Bhikkhupatimokkhapali_syllable_recitation.epub'

    cmdepub = f'pandoc -f html -t epub -c textAndMenu.css -o {epub} {save_html_file}'
    e = os.system(cmdepub)
    if e == 0:
        print('Generating EPUB: Done')


if __name__ == '__main__':
    fin = 'vin04t.nrf0.html_'
    main(fin)
