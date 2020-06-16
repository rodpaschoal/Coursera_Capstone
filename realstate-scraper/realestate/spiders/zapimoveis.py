# -*- coding: utf-8 -*-
import re
import json
import scrapy

from collections import OrderedDict
from scrapy.http import Request, FormRequest
from scrapy.utils.url import parse_url


class ZapimoveisSpider(scrapy.Spider):
    name = "zap"
    allowed_domains = ["zapimoveis.com.br"]

    def __init__(self, urls=None, start=1, count=None, seed=None,
                 *args, **kwargs):
        super(ZapimoveisSpider, self).__init__(*args, **kwargs)
        self.seed = seed
        self.start = int(start) if start else 1
        self.count = int(count) if count else None
        self.start_urls = (re.findall('[^\s,]+', urls) or
                           ['https://www.zapimoveis.com.br/venda/imoveis/pe/'])


    def parse(self, response):
        hidden = lambda id: response.xpath(
                '/html/body/input[@id="{}"]/@data-value'.
                format(id)).extract_first()

        total_pages = int(hidden('quantidadeTotalPaginas').replace('.',''))

        hashfragment = OrderedDict([
            ('pagina', None),
            ('semente', self.seed or hidden('semente')),
        ])

        formdata = OrderedDict([
            ('tipoOferta', '1'),
            ('paginaAtual', None),
            ('pathName', parse_url(response.url).path),
            ('hashFragment', ''),
        ])

        headers = {'X-Requested-With': 'XMLHttpRequest'}
        url = 'https://www.zapimoveis.com.br/Busca/RetornarBuscaAssincrona/'

        from_page = self.start
        if self.count:
            to_page = min(self.start + self.count - 1, total_pages)
        else:
            to_page = total_pages

        self.crawler.stats.set_value('total_pages', total_pages)
        self.crawler.stats.set_value('selected_pages',
                                     max(0, to_page - from_page + 1))

        for page in range(from_page, to_page + 1):
            hashfragment['pagina'] = formdata['paginaAtual'] = str(page)
            formdata['hashFragment'] = json.dumps(hashfragment,
                                                  separators=(',', ':'))
            yield FormRequest(
                    url,
                    headers=headers,
                    formdata=formdata,
                    callback=self.parse_busca)

    def parse_busca(self, response):
        self.crawler.stats.inc_value('scraped_pages')

        data = json.loads(response.body)
        if 'Resultado' in data and 'Resultado' in data['Resultado']:
            yield from data['Resultado']['Resultado']
