# -*- coding: utf-8 -*-
import scrapy
import logging


class ResumeSpider(scrapy.Spider):
    name = "resume"
    resumes = []

    def start_requests(self):
        with open("./links/resume-links.txt","r") as file:
            lines = file.readlines()
            logging.debug('Link: %s', lines)
            for line in lines:
                url = line.strip()
                yield scrapy.Request(url=url, callback=self.parse)
            

    def parse(self, response):
        file = open('resumes/resume.txt','aw')
    
        arr_code = response.css('span#ucVisualizacaoCurriculo_lblCodigoCurriculo::text').extract()
        if arr_code:
            code = arr_code[0]
            file.write("\"")
            file.write(str(code))
            file.write("\":\"")
        else:
            logging.error('It was not possible get the content')
        
    
        table_rows = response.css('div#ucVisualizacaoCurriculo_pnlDadosExperienciaProfissional tr')
         
        for line in table_rows:
            texto = line.css('td::text').extract()
            t = texto[0].strip()

            if t == u'Atividade da Empresa:' or t == u'Função Exercida:' or t == u'Atribuições:':
                text_save = texto[1].encode('utf-8').strip()
                file.write(text_save)
                file.write('\n')
                del text_save
        file.write('",')                
        file.close()				
        self.log('Saved file')