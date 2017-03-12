'''
# ЗДЕСЬ СОЗДАЕМ СПИСОК IDF

texts = []
norm_texts = []

for i in range(0, 2951):
    raw_text = open("sport/text_"+str(i)+".txt", 'r', encoding='utf-8')
    raw_text.readline()
    raw_text.readline()
    raw_text.readline()
    texts.append(raw_text.read())

print('normaa')
for text in texts:
    norm_texts.append(normalize(split_word(text)))

dic = word_freq(texts)
print(len(dic))

dic_idf = {}

n=0
for word in dic.keys():
    print(n)
    dic_idf[word] = idf(word, norm_texts)
    n += 1

t = ''
for i in sorted(dic_idf):
    t += i + ' ' + str(dic_idf[i]) + "\n"

open('idfs.txt', 'w', encoding='utf-8').write(t)
'''