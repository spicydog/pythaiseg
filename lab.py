# coding=utf-8
#
from pythaiseg import WordSegmentation

sentence = u'ตัดคำงงงงภาษาไทย'
ws = WordSegmentation()
sentences = ws.segment(sentence)

for sentences in sentences:
    for sequence in sentences:
        print('|'.join([node.term for node in sequence]))
    print('#' * 16)
