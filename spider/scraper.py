import scrapy
import sys
from opencc import OpenCC


class BrickSetSpider(scrapy.Spider):
	name = "brickset_spider"
	domain = "https://www.uukanshu.com"
	book_name = ''

	# Simplified Chinese to Traditional Chiese
	converter = OpenCC('s2t')

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
		print('scrapy runspider scraper.py -a starturl=https://www.uukanshu.com/b/125477/ -a output=萬族之劫.txt')
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
		content = response.css('#contentbox::text').getall()
		# replace &nbsp in content
		filter_content = [st.replace('\xa0', '') for st in content]
		# save to article dict
		self.articles.append({
			'idx': article_index,
			'title': title,
			'content': filter_content
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
			file.write(self.converter.convert(article['title'][0]))
			file.write('\n')

			for line in article['content']:
				# write content
				file.write(self.converter.convert(line.strip(' \t\n\r')))
				file.write('\n')
				file.write('\n')

		file.close();



