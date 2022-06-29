# -*- coding: utf-8 -*-
# Split Roman pali words into syllables
# It splits correctly for most of the words, but not all.
# Update: https://github.com/vpnry/palieasyread


# -------- modify these 3 values to your choice
import sys
import os
import string
import re
from collections import OrderedDict
my_word_divider = ' _ '
my_syllable_divider = ' '
my_show_origin = True
# below is the app logic
# do not modify if you don't know python


args = sys.argv


vowel_str = 'a,ā,i,ī,u,ū,e,o'
vowels = vowel_str.split(',')
vowels += vowel_str.upper().split(',')
# asp_consonants = 'ch,jh,kh,gh,th,ṭh,dh,ḍh,bh,ph'.split(',')

escape_xh = OrderedDict([
    ('kh', '1'),
    ('gh', '2'),
    ('ch', '3'),
    ('jh', '4'),
    ('th', '5'),
    ('ṭh', '6'),
    ('dh', '7'),
    ('ḍh', '8'),
    ('ph', '9'),
    ('bh', '0'),

    ('vh', '$'),
    # pariyogāḷhadhammo => pa ri yo gā ḷha dham mo
    ('ḷh', '¢'),
    # gārayhā => gā ra yhā
    ('yh', '£'),
    ('br', '€'),
    ('by', '¥')])


final_manual_fix = OrderedDict([
    ('K@h', 'Kh'),
    ('G@h', 'Gh'),
    ('C@h', 'Ch'),
    ('J@h', 'Jh'),
    ('T@h', 'Th'),
    ('Ṭ@h', 'Ṭh'),
    ('D@h', 'Dh'),
    ('Ḍ@h', 'Ḍh'),
    ('P@h', 'Ph'),
    ('B@h', 'Bh'),

    ('V@h', 'Vh'),
    ('Ḷ@h', 'Ḷh'),
    ('Y@h', 'Yh'),
    ('B@r', 'Br'),
    ('B@y', 'By'),

    # Manually replace
    ('D@v', 'Dv'),

    # khadv
    ('d@v', '@dv'),
    ('t@v', '@tv'),
    ('s@v', '@sv'),
    ('t@r', '@tr')
])

not_allow_divs = [v for k, v in escape_xh.items()]
not_allow_divs.append('@')

rex_nonWord = re.compile(r'\W+')


def add_div_consonant(word):
    word_ = word.strip('@1234567890' + string.punctuation + string.whitespace)
    if not word_:
        return word

    # like kkh =>k-kh etc
    three = re.compile(
        r'([^aāiīuūeo])(ch|jh|kh|gh|th|ṭh|dh|ḍh|bh|ph)',
        re.IGNORECASE)
    three_con = re.findall(three, word)
    if three_con:
        for tup in three_con:
            w = tup[0] + tup[1]
            rw = tup[0] + '@' + tup[1]
            word = word.replace(w, rw)

    for k, v in escape_xh.items():
        word = word.replace(k, str(v))

    # like nn =>n-n etc
    two = re.compile(
        r'([^.aāiīuūeo1234567890@])([^.aāiīuūeo1234567890@])',
        re.IGNORECASE)

    two_con = re.findall(two, word)
    if two_con:
        for tup in two_con:
            w = tup[0] + tup[1]
            rw = tup[0] + '@' + tup[1]
            word = word.replace(w, rw)

    # restore escaped ?h
    for k, v in escape_xh.items():
        word = word.replace(str(v), k)

    return word


def manual_fix_chunk(word):
    rex = re.compile(r'@([^aāiīuūeo])@', re.IGNORECASE)

    # @t@ => t@
    word = re.sub(rex, r'\1@', word)

    # fix misc PTT html
    word = word.replace('@,', ',')
    word = word.replace('@.', '.')
    word = word.replace('@;', ';')
    word = word.replace('@ṃ', 'ṃ')
    word = word.replace('@ṁ', 'ṁ')
    word = word.replace('‘@‘', '‘‘')
    word = word.replace('’@’', '’’')
    word = word.replace('‘@', '‘')

    for k, v in final_manual_fix.items():
        word = word.replace(k, str(v))
    return word.strip('@')


def split_syl_word(word):
    if len(word) <= 2:
        return word
    word = add_div_consonant(word)
    chunk = ''
    chars = [char for char in word]
    lenChar = len(chars)
    for i in range(lenChar):
        if re.match(rex_nonWord, chars[i]):
            chunk += chars[i]
            continue
        if chars[i] == '@':
            chunk += chars[i]
            continue
        if chars[i] not in vowels:
            chunk += chars[i]

        # consider a valid syllable after meeting a vowel
        # it works for most of the words.
        else:
            chunk += chars[i] + '@'
    chunk = chunk.strip('@')
    return manual_fix_chunk(chunk)


def check_div_collision(word_div, syl_div):
    divs = word_div.strip() + syl_div.strip()
    for i in not_allow_divs:
        if i in divs:
            return True
    return False


def easy_read(text, word_div=' _ ', show_origin=True, syl_div=' '):

    error_div = check_div_collision(word_div, syl_div)
    if error_div:
        print(
            'Error: word_div or syl_div must not contain these chars\n',
            not_allow_divs)
        print('Please use other dividers.')
        return ''

    res = ''
    lines = text.strip().splitlines()
    for line in lines:
        line_chunk = ''
        if not line:
            res += '\n'
            continue
        words = line.strip().split(' ')
        for word in words:
            syls = split_syl_word(word)
            if syls.strip():
                line_chunk += syls + word_div
        line_chunk = line_chunk.strip(' ' + word_div)
        if word_div == '] [':
            line_chunk = f'[{line_chunk}]'
        if show_origin:
            res += f'{line}\n{line_chunk}\n'
        else:
            res += f'\n{line_chunk}\n'

    if syl_div != '@':
        res = res.replace('@', syl_div)

    # fix misc double word_div
    di = word_div.strip()
    double_word_div = f' {di}  {di} '
    one_word_div = f' {di} '

    res = res.replace(double_word_div, one_word_div)
    return res.strip()


# ------- Command line -------

def easy_read_text(*wordss):
    text = ""
    for word in wordss:
        text += word + " "
    text = text.strip()
    return easy_read(text,
                     word_div=my_word_divider,
                     show_origin=my_show_origin,
                     syl_div=my_syllable_divider)


def easy_read_file(fn):
    text = ''
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()

    res = easy_read(text,
                    word_div=my_word_divider,
                    show_origin=my_show_origin,
                    syl_div=my_syllable_divider)
    savefn = fn + '_done.txt'
    with open(savefn, 'w', encoding='utf-8') as fo:
        fo.write(res)
    print('Done! Check:', savefn)


def printHelp():
    name = args[0]
    print('')
    print(
        "1. To split a short pali text, run:\n  python3 " +
        name +
        " <text>")
    print(
        "2. To split a pali plain text file, run:\n  python3 " +
        name +
        " yourPaliFile.txt")
    print('')


if __name__ == '__main__':
    if len(args) > 0:
        try:
            if not os.path.isfile(args[1]):
                try:
                    tdone = easy_read_text(*args[1:])
                    print(tdone)
                except Exception as e:
                    print("Errors occured! " + str(e))
                    printHelp()
            else:
                try:
                    print('Processing file:', args[1])
                    easy_read_file(args[1])
                except Exception as e:
                    print("Errors occured! " + str(e))
                    printHelp()

        except IndexError:
            printHelp()
