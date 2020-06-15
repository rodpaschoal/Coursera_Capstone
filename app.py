#The imported libraries should be in Requirements config file in order to Heroku or Docker to work
import streamlit as st

with st.echo('below'):
    import pandas as pd
    import numpy as np
    import requests

    import pydeck as pdk
   
    import os

    from googletrans import Translator
    translator = Translator()

    #Sidebar widgets
    language = st.sidebar.selectbox('Language',['English','Português'])
    translate = True if language == 'English' else False
    intro = st.sidebar.checkbox('Introduction', value=True)
    data = st.sidebar.checkbox('Data', value=True)
    method = st.sidebar.checkbox('Methodology', value=True)
    poi = st.sidebar.checkbox('The Neighborhood', value=True)
    gallery = st.sidebar.checkbox('Gallery', value=True)

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
        introduction = 'O condomínio Península foi construída para trazer o contato com a natureza e a liberdade. As pessoas desfrutam do ar puro nas suas ruas arborizadas e aproveitam os parques com seus familiares.\n\n Apesar do cenário de chácara, o condomínio está no coração da Barra da Tijuca, com facilidades a poucos metros de caminhada.\n\n Essa página se destina àqueles interessados em conhecer mais sobre essa linda vizinhança.\n\n**Business Problem**\n\nAgora, vamos supor que você amou a vizinhança e deseja comprar um imóvel na Península. Como encontrar as melhores ofertas do mercado? Como fechar um bom negócio? '
        draw(header, introduction)

    #Data
    if data:
        header = 'Sobre os dados'
        data_sources = 'A geolocalização das atrações é obtida por meio do Foursquare, o qual é fornecedor oficial do Apple Maps, Samsung, Uber, dentre outros aplicativos populares.\n\n O preço dos imóveis é atualizado em tempo real com dados do Zap Imóveis, a maior plataforma para compra e venda de imóveis do Brasil.'
        draw(header, data_sources)
    
    #Methodology
    if method:
        header = 'Metodologia'
        methodology = 'Através do endpoint \"explore\" com as coordenadas da Península, o Foursquare entrega uma lista de pontos de interesse nas redondezas com ID e categoria (restaurante, mall, café, atividade, dentre outros). Com a ID, usamos o endpoint \"likes\" e acessamos o número de likes dos usuários. \n\nA parte mais poderosa desse aplicativo é o algoritmo de inteligência artificial. \n\n O robô busca em tempo real no Zap Imóveis todos apartamentos na Península e mostra aqueles com os maiores descontos.\n\nA técnica utilizada é DBSCAN, algoritmo de machine learning capaz de identificar clusters, ou seja, conjuntos de dados que possuem muita similaridade entre si. No presente caso, imóveis com área, quartos, endereço e preços similares.\n\nA beleza dessa técnica é que ela também identifica outliers, que são dados totalmente dissimilares que não se encaixaram em nenhum conjunto. É justamente nos outliers onde vamos buscar os apartamentos com preços que não condizem com a realidade,i.e., as oportunidades.'
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
            This_App -> Best_Deals
            }
        ''')

    if poi:
        #Neighborhood results 
        header = 'Conheça a vizinhança'
        text = 'Estão representados no mapa abaixo os principais pontos de interesse no entorno da Península:'
        draw(header,text)

        #params to Foursquare API
        peninsula = '-22.989906, -43.351655'
        foursquare_id = os.environ.get('FOURSQUARE_ID')
        foursquare_secret = os.environ.get('FOURSQUARE_SECRET')
        version = '20200606'
        url = 'https://api.foursquare.com/v2/venues/explore'
        params = dict(
            client_id= foursquare_id,
            client_secret= foursquare_secret,
            v= version,
            ll= peninsula,
            limit=500,
            radius=2000
        )
        #function to call explore at Foursquare API
        @st.cache
        def call_explore():
            try:
                results = requests.get( url , params=params ).json()
                venues = results['response']['groups'][0]['items']
                df = pd.json_normalize( venues )
                #collect just the information needed 
                filtered_columns = ['venue.name', 'venue.categories', 'venue.id', 'venue.location.lat', 'venue.location.lng']
                df = df.loc[:, filtered_columns]

                #function to get the name of the category
                def get_category_type(row):
                    categories_list = row['venue.categories']    
                    if len(categories_list) == 0:
                        return None
                    else:
                        return categories_list[0]['name']
                #apply function           
                df['venue.categories'] = df.apply(get_category_type, axis=1)
                # clean columns - remove .
                df.columns = [col.split(".")[-1] for col in df.columns]
                return df
            except:
                st.error('Error querying Foursquare API')

        #call explore endpoint to Foursquare API
        df = call_explore()

        #peninsula in map
        peninsula_location = [-22.989906 ,-43.351655]

        #plotly graphics objects
        import plotly.graph_objects as go

        mapbox_access_token = os.environ.get('MAPBOX_TOKEN')

        fig = go.Figure( go.Scattermapbox(
                lat= df['lat'],
                lon= df['lng'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=9
                ),
                text=df['name'] + ' / ' + df['categories'],
            ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat= peninsula_location[0],
                    lon= peninsula_location[1]
                ),
                pitch=0,
                zoom=13
            ),
        )
        #print using streamlit
        st.plotly_chart( fig, use_container_width=True )

        #print neighborhood Results in table format
        st.write( df[['name','categories']] )

        #user input to search more
        text = 'O que mais deseja encontrar? (raio de 5 km)'
        text = english(text) if translate else text
        user_input = st.text_input(text)

        #params to Foursquare API
        url = 'https://api.foursquare.com/v2/venues/search'
        params = dict(
            client_id= foursquare_id,
            client_secret= foursquare_secret,
            v= version,
            ll= peninsula,
            limit=10,
            radius=5000,
            query= user_input
        )
        #function to call explore at Foursquare API
        @st.cache
        def call_search():
            #try:
                results = requests.get( url , params=params ).json()
                venues = results['response']['venues']
                df = pd.json_normalize( venues )
                #collect just the information needed 
                filtered_columns = ['name', 'categories','location.distance','location.address']
                df = df.loc[:, filtered_columns]

                #function to get the name of the category
                def get_category_type(row):
                    categories_list = row['categories']    
                    if len(categories_list) == 0:
                        return None
                    else:
                        return categories_list[0]['name']
                #apply function           
                df['categories'] = df.apply(get_category_type, axis=1)
                # clean columns - remove .
                df.columns = [col.split(".")[-1] for col in df.columns]
                return df
            #except:
            #    st.error('Error querying Foursquare API')
    
    if user_input != '' : 
        df2 = call_search()
        st.write(df2)
    
    #Appartments results
    #header = 'Resultados dos apartamentos'
    #text = 'A query no Zap Imóveis resultou nos seguintes anúncios dentro do condomínio:'
    #draw(header,text)

    #create a 3D map
    #MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN')
    #scatter = pdk.Layer(
    #         'ScatterplotLayer',
    #         data=df,
    #         get_position='[lng, lat]',
    #         get_fill_color='[255, 140, 0]',
    #         get_line_color=[0, 0, 0],
    #         get_radius=200,
    #         pickable=True,
    #         opacity=0.6,
    #         stroked=True,
    #         filled=True,
    #         radius_scale=1,
    #         radius_min_pixels=1,
    #         radius_max_pixels=100,
    #         line_width_min_pixels=1,
    #     )
    #INITIAL_VIEW_STATE = pdk.ViewState(
    #                latitude= -22.989906, #Peninsula Latitude
    #                longitude= -43.351655, #Peninsula Longitude
    #                zoom=13,
    #                pitch=50,
    #            )
    #map_pdk = pdk.Deck( 
    #    map_style='mapbox://styles/mapbox/satellite-streets-v11',
    #    layers=[scatter], 
    #    initial_view_state=INITIAL_VIEW_STATE 
    #     )
    #print Results in a map
    #st.pydeck_chart( map_pdk )

     #Gallery
    if gallery:
        header = 'Galeria de imagens'
        header = english(header) if translate else header
        st.header( header )
        st.image('peninsula-joy.jpg')
        
    #Source code (with st.echo() running)
    header = 'Código Fonte'
    text = 'Este é um projeto open source desenvolvido para o trabalho final do certificado em Data Science da IBM.'
    header = english( header ) if translate else header
    text = english( text ) if translate else text
    st.header( header )
    st.write( text )