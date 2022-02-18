import heapq
import tkinter
from bs4 import BeautifulSoup
import googlesearch,requests,re
import nltk
from tkinter import *
root=Tk()
root.title("Query Bot")
def code():
    para=[]
    output=[]
    a = googlesearch.search(entry.get())
    for b in a[1:4]:
            try:
                r = requests.get(b)
                data = r.text
                soup = BeautifulSoup(data, features='lxml')
                for link in soup.find_all('p'):
                    g = link.get_text()
                    token = nltk.tokenize.sent_tokenize(g)
                    para.append(token)
            except requests.exceptions.MissingSchema as pe:
                print()
    def r(para):
        for s in para:
            if type(s) == list:
                r(s)
            else:
                output.append(s)
    r(para)
    # print(output)
    # text summarizatoin
    # using list comprehension
    stri = ' '.join(map(str, output))
    text = stri.lower()
    clean = re.sub('[^a-zA-Z]', ' ', text)
    clean2 = re.sub('\s+', ' ', clean)
    sentence_list = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(clean2):
        if word not in stopwords:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / maximum_frequency
    sentence_scores = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence):
            if word in word_frequencies and len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]
    summary = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    sentence = ''.join(summary)
    pr = re.sub('\n+', ' ', sentence)
    abc = nltk.sent_tokenize(pr)
    qus = entry.get()
    text_are.insert(tkinter.INSERT, qus)
    text_are.insert(tkinter.INSERT,"\n")
    text_area.insert(tkinter.INSERT,abc)
    text_area.insert(tkinter.INSERT,"\n")
    text_area.insert(tkinter.INSERT,"\n")
    text_area.insert(tkinter.INSERT,"\n")
    entry.delete(0,END)
def clear():
    text_area.delete(1.0,END)
entry=Entry(root,width=50,text='enter your queries ')
entry.pack(pady=10)
btn=Button(root,width=20,text='search',command=code)
btn.pack(pady=15)
btn2=Button(root,width=20,text='clear',command=clear)
btn2.pack()
text_are=Text(root, width=85,height=90)
text_are.pack(pady=20, side=LEFT)
text_area=Text(root ,width=80 ,height=90)
text_area.pack(pady=20, side=RIGHT)
root.mainloop()