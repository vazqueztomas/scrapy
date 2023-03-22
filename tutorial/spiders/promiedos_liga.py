from pathlib import Path
import scrapy


class LigaSpider(scrapy.Spider):
    name = 'liga_argentina'

    def start_requests(self):
        urls = ['https://www.promiedos.com.ar/primera',
                "https://www.promiedos.com.ar/primera=equipos"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f'{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')

        for equipo in response.css('div.eqs strong'):
            yield {
                'equipo': equipo.css('strong').get(),
            }

        next_page = "/" + response.css('ul.items-menu li a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
