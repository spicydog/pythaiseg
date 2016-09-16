# coding=utf-8
from pythaiseg import WordSegmentation

sentence = u'ทดสอบตัดคำภาษาไทย'
ws = WordSegmentation()
sequences = ws.segment(sentence)
for sequence in sequences:
    print('|'.join(sequence))
