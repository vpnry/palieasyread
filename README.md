## Info
A quick and simple Python script to split Roman pali words into smaller syllables which are easier to be read.

> Bodhirukkhabodhigharaāsanagharasammuñjaniaṭṭadāruaṭṭavaccakuṭidvārakoṭṭhakapānīyakuṭipānīyamāḷakadantakaṭṭhamāḷakesupi

> [Bo dhi ruk kha bo dhi gha ra ā sa na gha ra sam muñ ja ni aṭ ṭa dā ru aṭ ṭa vac ca ku ṭi dvā ra koṭ ṭha ka pā nī ya ku ṭi pā nī ya mā ḷa ka dan ta kaṭ ṭha mā ḷa ke su pi]

> (Vinayasaṅgaha-aṭṭhakathā)

It splits correctly most of the words, but NOT all. Some words may need your postprocessing edit (manually find & replace!).

NOT recommended for beginers who have no idea how to pronounce a pali word. For example `gārayhā`, this script will split it: `gārayhā => gā ra yhā`.


## Installation


### Method 1


```
python3 -m pip install git+https://github.com/vpnry/palieasyread.git#egg=palieasyread

```

### Method 2:
Download [this repository](https://github.com/vpnry/palieasyread/archive/refs/heads/master.zip) unzip and run `python3 setup.py install` or import the `palieasyread` manually.


## Usage

### Syntax

```python
easy_read(text, word_div=' / ', show_origin=True, syl_div=' ')
```

### Examples:

```python

from palieasyread import easy_read

text = '''
Manopubbaṅgamā dhammā, manoseṭṭhā manomayā;

Manasā ce paduṭṭhena, bhāsati vā karoti vā;

Tato naṃ dukkhamanveti, cakkaṃva vahato padaṃ.
'''

```

#### Example 1

Using default settings:

```python

print(easy_read(text))

```

Output example 1

```
[Ma no pub baṅ ga mā] [dham mā,] [ma no seṭ ṭhā] [ma no ma yā;]

Manasā ce paduṭṭhena, bhāsati vā karoti vā;
[Ma na sā] [ce] [pa duṭ ṭhe na,] [bhā sa ti] [vā] [ka ro ti] [vā;]

Tato naṃ dukkhamanveti, cakkaṃva vahato padaṃ.
[Ta to] [naṃ] [duk kha man ve ti,] [cak kaṃ va] [va ha to] [pa daṃ.]
```

#### Example 2
Changing word divider and NOT showing the orginal text

```python

print(easy_read(text, word_div=' * ', show_origin=False))

```

Output example 2

```
Ma no pub baṅ ga mā * dham mā, * ma no seṭ ṭhā * ma no ma yā;


Ma na sā * ce * pa duṭ ṭhe na, * bhā sa ti * vā * ka ro ti * vā;


Ta to * naṃ * duk kha man ve ti, * cak kaṃ va * va ha to * pa daṃ.
```

#### Example 3
Changing word divider, syllable divider, and NOT showing the orginal text 

```python
print(easy_read(text, word_div=' / ', show_origin=False, syl_div='.'))

```

Output example 3

```
Ma.no.pub.baṅ.ga.mā / dham.mā, / ma.no.seṭ.ṭhā / ma.no.ma.yā;


Ma.na.sā / ce / pa.duṭ.ṭhe.na, / bhā.sa.ti / vā / ka.ro.ti / vā;


Ta.to / naṃ / duk.kha.man.ve.ti, / cak.kaṃ.va / va.ha.to / pa.daṃ.
```