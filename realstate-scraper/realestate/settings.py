# -*- coding: utf-8 -*-

from fake_useragent import UserAgent

# Scrapy settings for realestate project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'realestate'

SPIDER_MODULES = ['realestate.spiders']
NEWSPIDER_MODULE = 'realestate.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = UserAgent()['chrome']

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'realestate.middlewares.RealestateSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'realestate.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'realestate.pipelines.RealestatePipeline': 100,
    'realestate.pipelines.MongoDBPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'realestate.extensions.FilesystemCacheStorage'

# Log Messages
LOG_LEVEL='INFO'

# MongoDB
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "realestate_scraper"
MONGODB_COLLECTION = "realestate"

# Jmespath
JMESPATH = """{
  AnuncianteTipo:AnuncianteTipo
  Area:Area
  Bairro:BairroOficial||Bairro
  Cidade:CidadeOficial||Cidade
  CEP:CEP
  CodImobiliaria:CodImobiliaria
  CodigoAnunciante:CodigoAnunciante
  CodigoOfertaImobiliaria:CodigoOfertaImobiliaria
  CodigoOfertaZAP:CodigoOfertaZAP
  DataAtualizacaoHumanizada:DataAtualizacaoHumanizada
  DetalhesOferta:DetalhesOferta
  DistanciaMetro:DistanciaMetro
  DistanciaOnibus:DistanciaOnibus
  Endereco:Endereco
  Estado:Estado
  FormatarSubTipoImovel:FormatarSubTipoImovel
  FormatarSubTipoOferta:FormatarSubTipoOferta
  Fotos:join(` `, Fotos[].UrlImagemTamanhoGG)
  Latitude:Latitude
  LogNota:LogNota
  Longitude:Longitude
  NomeAnunciante:NomeAnunciante
  Nota:Nota
  Observacao:Observacao
  OrigemLead:OrigemLead
  PrecoCondominio:PrecoCondominio
  QuantidadeQuartos:QuantidadeQuartos
  QuantidadeSuites:QuantidadeSuites
  QuantidadeVagas:QuantidadeVagas
  SubTipo:SubTipo
  SubTipoOferta:SubTipoOferta
  Tipo:Tipo
  TipoDaOferta:TipoDaOferta
  TituloPagina:TituloPagina
  Transacao:Transacao
  URLAtendimento:URLAtendimento
  UrlFicha:UrlFicha
  UrlFotoDestaqueTamanhoM:UrlFotoDestaqueTamanhoM
  UrlFotoDestaqueTamanhoP:UrlFotoDestaqueTamanhoP
  UrlLogotipoCliente:UrlLogotipoCliente
  Valor:Valor
  ValorIPTU:ValorIPTU
  ZapID:ZapID
  scraped_time:scraped_time
  updated_time:updated_time
}"""
