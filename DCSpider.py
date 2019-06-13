#####################################################
#
#		WebScarping Data Camp Course Details
#
#####################################################


#
# Import scrapy library
import scrapy
from scrapy.crawler import CrawlerProcess


#
# DC Spider class
class DCSpider( scrapy.Spider ):


	# variable name 
	name = "dcspider"


	# start_requests method: to define which websites to scrape 
	def start_requests( self ):

		# list of webpages to scrape
		urls = [ "https://www.datacamp.com/courses/all" ]
		# follow the links to the next parser		
		for url in urls:
			yield scrapy.Request( url = url, callback = self.parse_course_links )


	# parse_front method: to parse the front page		
	def parse_front( self, response ):

		# narrow down on the course block elements
		course_blocks = response.css( 'div.course-block' )
		# direct to the course links
		course_links = course_blocks.xpath( './a/@href' )
		# extract the links 
		links_to_follow = course_links.extract()
		# follow the links to the next parser
		for link in links_to_follow:
			yield response.follow( url = link, callback = self.parse_pages )


	# parse_pages method: to parse the pages 
	def parse_pages( self, response ):

		# direct to the course title text
		course_title = response.xpath( '//h1[contains(@class, "title")]/text()' )
		# extract and clean the course title text
		course_title_text = course_title.extract_first().strip()
		# direct to chapter titles text
		chapter_titles = response.css( 'h4.chapter__title::text' )
		# extract and clean the chapter titles text				
		chapter_titles_text = [t.strip() for t in chapter_titles.extract()]
		# store this in dictonary
		dict_dc[ chapter_titles_text ] = chapter_titles_text



	# parse_href method: to work on the website pages
	def parse_course_links( self, response ):
		
		# direct to the course titles
		titles = response.css('h4.course-block__title::text').extract()
		# direct to the course authors
		authors = response.css('div.course-block__author > img::attr(alt)').extract()
		# direct to the course hyperlinks
		links = response.css('div.course-block > a::attr(href)').extract()
		# direct to author's image
		images = response.css('div.course-block__author > img::attr(src)').extract()	
		# write_csv method: to write links to csv
		DCC_file = 'DataCampCourses.csv'
		with open( DCC_file, 'w' ) as f:
			f.write('Course Title' + '\t' + 'Course Author' + '\t' + 'Course Link' + '\t' + 'Authors\'s Image Link' + '\n')
			for i in range(len(titles)):
				f.write( "%s \t %s\t %s\t %s\n" % (titles[i], authors[i], links[i], images[i]) )	

		#f.close()		

#
# Initialize the dictionary 
dict_dc = dict()


#
# Run the Spider
process = CrawlerProcess( )
process.crawl( DCSpider )
process.start( )
