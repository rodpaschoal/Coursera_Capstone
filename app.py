#The imported libraries should be in Requirements config file in order to Heroku or Docker to work
import streamlit as st

with st.echo('below'):
    import pandas as pd
    import numpy as np
    import requests
    from googletrans import Translator
    translator = Translator()

    #Sidebar widgets
    language = st.sidebar.selectbox('Language',['English','Português'])
    translate = True if language == 'English' else False
    intro = st.sidebar.checkbox('Introduction', value=True)
    data = st.sidebar.checkbox('Data', value=True)
    method = st.sidebar.checkbox('Methodology', value=True)

    #Function to google translate the website texts
    def english(text):
        return translator.translate(text).text
    
    def draw(header,text):
        if translate: 
            header = english(header)
            text = english(text)
        st.header( header )
        st.write( text )
    
    #Main page
    title = 'Conheça a Península do Rio de Janeiro'
    title = english(title) if translate else title
    st.title(title)
    st.markdown('by [rodpaschoal](https://github.com/rodpaschoal)')
    st.markdown('---')

    #Introduction
    if intro:
        #Main video
        st.video('https://www.youtube.com/watch?v=dSvVIYH7k24&t=200s')
        st.markdown('###### Península, Barra da Tijuca, Rio de Janeiro / RJ, Brasil')
        st.markdown('---')

        #Introduction
        header = 'Introdução'
        introduction = 'A Península foi construída para trazer o contato com a natureza e a liberdade. As pessoas desfrutam do ar puro nas suas ruas arborizadas e aproveitam os parques com seus familiares.\n\n Apesar do cenário de chácara, o condomínio está no coração da Barra da Tijuca, com facilidades a poucos metros de caminhada.\n\n Essa página se destina àqueles interessados em conhecer mais sobre essa linda vizinhança.\n\n**Business Problem**\n\nAgora, vamos supor que você amou a vizinhança e deseja comprar um imóvel na Península. Como encontrar as melhores ofertas do mercado? Como fechar um bom negócio? '
        draw(header, introduction)

    #Data
    if data:
        header = 'Sobre os dados'
        data_sources = 'A geolocalização das atrações é obtida por meio do Foursquare, o qual é fornecedor oficial do Apple Maps, Samsung, Uber, dentre outros aplicativos populares.\n\n O preço dos imóveis é atualizado em tempo real com dados do Zap Imóveis, a maior plataforma para compra e venda de imóveis do Brasil.'
        draw(header, data_sources)
    
    #Methodology
    if method:
        header = 'Metodologia'
        methodology = 'Através do endpoint \"explore\" com as coordenadas da Península, o Foursquare entrega uma lista de pontos de interesse nas redondezas com ID e categoria (restaurante, mall, café, atividade, dentre outros). Com a ID, usamos o endpoint \"likes\" e acessamos o número de likes dos usuários. \n\nA parte mais poderosa desse aplicativo é o algoritmo de inteligência artificial. \n\nUm robô busca em tempo real no Zap Imóveis todos apartamentos na Península e mostra aqueles com um desconto excessivo.\n\nA técnica utilizada é DBSCAN, algoritmo de machine learning capaz de identificar clusters, ou seja, conjuntos de dados que possuem muita similaridade entre si. No presente caso, imóveis com área, quartos, endereço e preços similares.\n\nA beleza dessa técnica é que ela também identifica outliers, que são dados totalmente dissimilares que não se encaixaram em nenhum conjunto. É justamente nos outliers onde vamos buscar os apartamentos com preços que não condizem com a realidade,i.e., as oportunidades.'
        draw(header, methodology)
        st.graphviz_chart('''
        digraph {
            Coordinates -> Foursquare
            Foursquare -> POI
            POI -> This_App
            Streets -> Zap
            Zap -> Appartments
            Appartments -> This_App
            This_App -> Map
            This_App -> Best_Deal
            }
        ''')

    #Source code (with st.echo() running)
    header = 'Código Fonte'
    text = 'Este é um projeto open source desenvolvido para o trabalho final do certificado em Data Science da IBM.'
    header = english( header ) if translate else header
    text = english( text ) if translate else text
    st.header( header )
    st.write( text )