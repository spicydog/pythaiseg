# coding=utf-8

from pythaiseg import WordSegmentation

sentence = u'ทดสอบตัดคำภาษาไทย ตัดมานานมากละ ตัดไม่ได้ซะที'
ws = WordSegmentation()
sentences = ws.segment(sentence)

result = ws.maximal_matching(sentences)
print '| |'.join(['|'.join(s) for s in result]) + '|'

