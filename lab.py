# coding=utf-8
from pythaiseg import WordSegmentation

sentence = u'ทดสอบ ตัดคำ ภาษาไทย'
ws = WordSegmentation()
sentences = ws.segment(sentence)
for sequences in sentences:
    for sequence in sequences:
        print('|'.join(sequence))
