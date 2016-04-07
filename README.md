# Quora_crawler
A crawler crawling Q&amp;A of quora topics

#Install
This python script requires several packages

- selenium (2.53.1)
- phantomjs (2.0.1)

To install on Mac with pip or brew:

```
brew install selenium
brew install phantomjs
```

#Usage
To use the script, just run the python script

```
python quora_crawler.py
```

It will generate a csv file named `quora_qa.csv` with data of `Question, Answer` pairs. By default it grabs data from https://www.quora.com/topic/Ann-Arbor-MI, you can change it with any valid url:

```
url = YOUR_URL
```
