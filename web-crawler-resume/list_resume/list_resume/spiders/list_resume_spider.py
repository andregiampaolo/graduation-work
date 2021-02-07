import scrapy

class ListResumeSpider(scrapy.Spider):
    name = "links_resume"

    def start_requests(self):
        number = 1
        links = []
        
        while number < 100:
            links.append('http://www.bne.com.br/lista-de-curriculos/10629174?pag='+str(number)+'&itens=50&gpag=0&gitens=20')
            number += 1
            
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        links = response.css('div.icones_pesquisa_curriculo a:last-child::attr(href)').extract()
        file = open('list_resume/spiders/links/resume-links.txt','a')
        for l in links:
        	file.write(l)
        	file.write('\n')
        file.close()				
        self.log('Saved file')