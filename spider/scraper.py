import scrapy
import sys
from opencc import OpenCC
import w3lib.html


class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	domain = "https://tw.uukanshu.com"
	book_name = ''

	# Simplified Chinese to Traditional Chiese
	converter = OpenCC('s2twp')

	# Start parsing url
	start_urls = []

	# content dict
	articles = [];
	stop_len = 0;

	if len(sys.argv) < 6:
		print('sys.argv length:', len(sys.argv))
		print(sys.argv)
		print('you need to provide valid input')
		print('for example:')
		print('scrapy runspider scraper.py -a starturl=https://tw.uukanshu.com/b/114371/ -a output=世界樹遊戲.txt')
		sys.exit(1)

	start_urls.append(sys.argv[3].split('=')[1])
	book_name = sys.argv[5].split('=')[1]

	def parse(self, response):
		# get all chapter links
		urls = response.css('#chapterList li a::attr(href)').getall()

		self.stop_len = len(urls)

		# parse each chapter
		for idx, url in enumerate(urls):
			request = scrapy.Request(self.domain+url, callback=self.parse_content, cb_kwargs=dict(article_index=idx))
			yield request

	def parse_content(self, response, article_index):
		# parse title
		title = response.css('h1::text').getall()

		# parse content
		content = response.css('#contentbox').extract()
		# remove script tag
		content = w3lib.html.remove_tags_with_content(content[0], ('script', ))
		# replace other tag with split keyword
		content = w3lib.html.replace_tags(content, '<split>')
		# replace escape char \r \t \n
		content = w3lib.html.replace_escape_chars(content)
		# remove all white space
		content = content.replace(' ', '');
		# make content line by line
		content = content.split('<split>')
		# filter empty string
		content = list(filter(None, content))

		# save to article dict
		self.articles.append({
			'idx': article_index,
			'title': title,
			'content': content
		})
		self.save_to_txt()

	def save_to_txt(self):
		if len(self.articles) != self.stop_len:
			return

		# sort articles to incremental order
		sort_articles = sorted(self.articles, key=lambda k:k['idx'], reverse=True)
		# save to txt
		file = open(self.book_name, 'w')

		for article in sort_articles:
			# write title
			# if we need to conver simplified chinese to traditional chinese
			# file.write(self.converter.convert(article['title'][0]))
			file.write(article['title'][0])
			file.write('\n')
			file.write('\n')
			file.write('\n')

			for line in article['content']:
				# write content
				# if we need to conver simplified chinese to traditional chinese
				# file.write(self.converter.convert(line.strip(' \t\n\r')))
				file.write(line.strip(' \t\n\r'))
				file.write('\n')
				file.write('\n')

		file.close();



