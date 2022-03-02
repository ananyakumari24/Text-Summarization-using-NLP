#importing libraries
from os import error
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from flask import Flask
from flask import request, render_template, flash

app = Flask(__name__)

@app.route("/")
def index():
    text = request.args.get("text", "")
    # if text=="":
    #     flash("Please enter text", 'error')
    #     return render_template('text.html')
    if text:
        summary = summarizer(text)
    else:
        summary = ""
    return( render_template('home.html', text=text, summary=summary))
    #    + "Summary: "
    #     + summary
    #     )    

# #input text to be summarized
# text = input("enter text to summarize:")

@app.route("/<string:text>")
def summarizer(text):
    #tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # a frequency table to keep the score of each word
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word]+=1
        else:
            freqTable[word] = 1

    # a dictionary to keep the score of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Finding average and treating it as a threshold value
    average = int(sumValues/len(sentenceValue))

    # Storing sentences into our summary
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence]>(1.2*average)):
            summary += " " + sentence 
    return summary

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


