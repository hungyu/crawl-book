### Purpose
	Using python scrapy to crawl articles

### install step
* install python (version > 3)
```
	you can use pyenv to control/install different version of python
```
* install scrapy
```
	pip install scrapy
```
* install simplified Chinese and Traditional Chinese convertor
```
	pip install opencc-python-reimplemented
```

### usage
```
	scrapy runspider scraper.py -a starturl=https://www.uukanshu.com/b/125477/ -a output=book.txt
```

### note
* now only support www.uukanshu.com article
