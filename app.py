#The imported libraries should be in Requirements config file in order to Heroku or Docker to work
import streamlit as st

with st.echo('below'):
    import pandas as pd
    import numpy as np
    import os
    import time

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    import requests
    from bs4 import BeautifulSoup

    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler
    import plotly.graph_objects as go
    import plotly.express as px

    from googletrans import Translator
    translator = Translator()

    curpath = os.path.dirname(os.path.abspath(__file__))

    #Sidebar widgets
    language = st.sidebar.selectbox('Language',['English','Português'])
    translate = True if language == 'English' else False

    st.sidebar.subheader('Sections')
    intro = st.sidebar.checkbox('Introduction', value=True)
    data = st.sidebar.checkbox('Data', value=True)
    method = st.sidebar.checkbox('Methodology', value=True)
    poi = st.sidebar.checkbox('The Neighborhood', value=True)
    residences = st.sidebar.checkbox('The Residences', value=True)
    discussion = st.sidebar.checkbox('Discussion', value=True)
    conclusion = st.sidebar.checkbox('Conclusion', value=True)
    gallery = st.sidebar.checkbox('Image Gallery', value=True)

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
    st.markdown('Git repo [@rodpaschoal](https://github.com/rodpaschoal)')
    st.markdown('---')

    #Introduction
    if intro:
        #Main video
        st.video('https://www.youtube.com/watch?v=dSvVIYH7k24&t=200s')
        st.markdown('###### Península, Barra da Tijuca, Rio de Janeiro / RJ, Brasil')
        st.markdown('---')

        #Introduction
        header = 'Introdução'
        introduction = 'O condomínio Península foi construída para trazer o contato com a natureza e a liberdade. As pessoas desfrutam do ar puro nas suas ruas arborizadas e aproveitam os parques com seus familiares.\n\n Apesar do cenário de chácara, o condomínio está no coração da Barra da Tijuca, com facilidades a poucos metros de caminhada.\n\n Essa página se destina àqueles interessados em conhecer mais sobre essa linda vizinhança.'
        draw(header, introduction)

        sub = 'Business Problem'
        st.subheader( sub )
        text ='Agora, vamos supor que você amou a vizinhança e deseja comprar um imóvel na Península. Como encontrar as melhores ofertas do mercado? Como fechar um bom negócio? '
        text = english(text) if translate else text
        st.write( text )

        text = 'Para encontrar uma boa oferta, costumamos filtrar e ordenar os resultados em páginas de busca de imóveis.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Apesar de intuitivo, pode ser exaustivo quando existem milhares de anúncios para analisar em apenas um bairro.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Sem contar que pode nos levar ao erro, pois quando filtramos para apartamentos com 2 quartos, podemos estar perdendo a oportunidade de ver um apartamento com 3 quartos que está sendo vendido pelo mesmo preço, por exemplo. '
        text = english(text) if translate else text
        st.write( text )

        text = 'No final, temos que filtrar diversas vezes para encontrar boas ofertas e repetir o processo sempre que anúncios são inseridos ou atualizados na base.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Será que é possível facilitar essa tarefa? Haveria uma ferramenta mais automatizada?'
        text = english(text) if translate else text
        st.write( text )

    #Data
    if data:
        header = 'Sobre os dados'
        data_sources = 'A geolocalização é obtida por meio do Foursquare, o qual é fornecedor oficial do Apple Maps, Samsung, Uber, dentre outros aplicativos populares.\n\n O preço dos imóveis é atualizado em tempo real com dados do Viva Real, uma das maiores plataformas para compra e venda de imóveis do Brasil.'
        draw(header, data_sources)
    
    #Methodology
    if method:
        header = 'Metodologia'
        methodology = 'Este projeto foi desenvolvido em Python, a linguagem de programação mais popular no mundo. As principais bibliotecas utilizadas foram: Pandas, Plotly, Sklearn, Beautifulsoup, Selenium e Streamlit para geração desta página.\n\n Para obter a geolocalização de pontos interessantes, usamos o endpoint \"explore\" na Location API do Foursquare, a qual entrega uma lista de locais mais interessantes nas redondezas e a categoria (restaurante, mall, café, atividade, dentre outros). A biblioteca plotly é utilizada para desenhar o mapa com os marcadores nos respectivos endereços. O endpoint \"search\" foi utilizado para buscar locais solicitados pelo usuário. \n\nA parte mais poderosa desse aplicativo é o algoritmo de machine learning. \n\n O robô busca em tempo real no Viva Real todos apartamentos na Península e mostra aqueles com os maiores descontos.\n\nA técnica utilizada é DBSCAN, algoritmo de machine learning capaz de identificar clusters, ou seja, conjuntos de dados que possuem muita similaridade entre si. No presente caso, imóveis com área, quartos, endereço e preços similares.\n\nA beleza dessa técnica é que ela também identifica outliers, que são dados totalmente dissimilares que não se encaixaram em nenhum conjunto. É justamente nos outliers onde vamos buscar os apartamentos com preços que não condizem com a realidade,i.e., as oportunidades.'
        draw(header, methodology)
        st.graphviz_chart('''
        digraph {
            Coordinates -> Foursquare
            Foursquare -> POI
            POI -> This_App
            Streets -> Viva_Real
            Viva_Real -> Residences
            Residences -> This_App
            This_App -> Map
            This_App -> Best_Deals
            }
        ''')

    if poi:
        #Neighborhood results 
        header = 'Conheça a vizinhança'
        text = 'Estão representados no mapa abaixo as principais atrações no entorno da Península:'
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
        st.plotly_chart( fig ) #, use_container_width=True 

        #print neighborhood Results in table format
        st.write( df[['name','categories']] )

        #user input to search more
        text = 'O que mais deseja encontrar?'
        text = english(text) if translate else text
        st.subheader( text )

        text = 'Procure no raio de 5 km da Península:'
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
            try:
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

            except:
                st.error('Error querying Foursquare API')
                return
    
        if user_input != '' : 
            df2 = call_search()
            st.write(df2)
    
    #Appartments results
    if residences:
        header = 'Conheça as residências'
        text = 'Primeiro vamos obter os dados.'
        draw(header,text)

        @st.cache
        def scrape_residences( url , max_pages=50 ):
        
            def scrape_one_page( data ):

                one_page = pd.DataFrame()

                for i,residence in enumerate( data ):
                    try:
                        title = residence.h2.a.text
                    except:
                        title = None
                    try:
                        link = residence.h2.a['href']
                    except:
                        link = None
                    try:
                        address = residence.find('span', class_='property-card__address js-property-card-address js-see-on-map').text
                    except:
                        address = None
                    try:
                        area = residence.find('span', class_='property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area').text
                    except:
                        area = None
                    try:
                        rooms = residence.find('li', class_='property-card__detail-item property-card__detail-room js-property-detail-rooms').text.split()[0]
                    except:
                        rooms = None
                    try:
                        suites = residence.find('li', class_='property-card__detail-item property-card__detail-item-extra js-property-detail-suites').text.split()[0]
                    except:
                        suites = None
                    try:
                        bathroom = residence.find('li', class_='property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom').text.split()[0]
                    except:
                        bathroom = None
                    try:
                        garages = residence.find('li', class_='property-card__detail-item property-card__detail-garage js-property-detail-garages').text.split()[0]
                    except:
                        garages = None
                    try:
                        price = residence.find('div', class_='property-card__price js-property-card-prices js-property-card__price-small').text
                    except:
                        price = None
                    try:
                        condo = residence.find('strong', class_='js-condo-price').text
                    except:
                        condo = None

                    residence_info = {  
                        'title': [title],
                        'link': [link], 
                        'address': [address],
                        'area': [area],
                        'rooms': [rooms], 
                        'suites': [suites], 
                        'bathroom': [bathroom], 
                        'garages': [garages], 
                        'price': [price], 
                        'condo': [condo]
                        } 
                    result = pd.DataFrame( residence_info, index=[i] )
                    one_page = one_page.append(result)

                return one_page
            
            results = pd.DataFrame()

            #Open chrome with Selenium
            path_chrome = os.environ.get('CHROMEDRIVER_PATH')
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=path_chrome, options=chrome_options)

            try:
                driver.get( url )
            except Exception as e:
                searching.text(e)

            for page in range(max_pages): #try to scrape up to max_pages
                
                try:
                    source = driver.page_source
                    soup = BeautifulSoup( source, 'lxml' ) #'lxml'

                    residences_elements = soup.find_all('div', class_='property-card__main-content')

                    residences = scrape_one_page( residences_elements )
                    results = results.append( residences, ignore_index=True )
                    
                    next_buttons = driver.find_elements_by_class_name('js-change-page') #or pagination__item
                    next_button = next_buttons[-1] #The Last Button is (Next Page), the others are the number of the pages
                    last_page = ( next_button.get_attribute('data-page') == '' )

                    if last_page:
                        break
                    else:
                        next_button.click() 

                    #Do not flood the website
                    time.sleep( np.random.randint(0,3) )

                except Exception as e:
                    searching.text(e)
                    continue
            
            #when the loop is finished
            driver.close()  
            return results 
    
        @st.cache
        def clean_dataset( df3 ):
            df3['link'] = 'https://www.vivareal.com.br' + df3['link']

            df3['vivareal-id'] = df3['link'].apply( lambda x: x.split('-')[-1].split('/')[0] )
            #df3['link'] = df3['link'].str.strip('/?__vt=vt:a')
            #df3['link'] = df3['link'].str.strip('/?__vt=vt:b')
            #df3['link'] = df3['link'].str.strip('/?__vt=vt:c')
            #df3['link'] = df3['link'].str.strip('/?__vt=il')
            #df3['vivareal-id'] = df3['link'].str[-10:]
            #df3['vivareal-id'] = df3['vivareal-id'].str.strip('d-') 

            df3['price'] = df3['price'].str.strip().str.strip('R$').str.replace('.','')
            df3['condo'] = df3['condo'].str.strip().str.strip('R$').str.replace('.','')

            #Address - drop NaN
            df3.dropna(subset=['address'], inplace=True)
            df3['address'] = df3['address'].apply(lambda x: x.split('-')[0].strip().split(',')[0] )
            #Keep just addresses inside Peninsula addresses
            df3['address'] = df3[ df3['address'].isin( addresses ) ]['address']
            #Prepare address to visualization
            df3['address'] = df3['address'].str.replace('Rua','').str.replace('da Península','').str.replace('Avenida','').str.replace('de Mello Neto','')

            #Drop ads with no defined area
            df3 = df3[ ~df3['area'].str.contains('-') ] #also may drop paid banners

            #Drop ads with no price
            df3 = df3[ ~(df3['price'] == 'Sob Consulta') ] #also may drop paid banners
            df3 = df3[ ~df3['price'].str.contains('A partir de') ] #also may drop paid banners

            #Drop ads with defined number of rooms, bathrooms or garages are a range (like 2-3) split it
            df3 = df3[ ~df3['rooms'].str.contains('-') ]
            df3 = df3[ ~df3['bathroom'].str.contains('-') ]
            df3 = df3[ ~df3['garages'].str.contains('-') ]

            #Feature engineering - Important metric
            df3['price/m2'] = df3['price'].astype('int') / df3['area'].astype('int')

            #Drop ads with the same link
            df3.drop_duplicates(subset='link', inplace=True)

            #Drop ads with the same id
            df3.drop_duplicates(subset='vivareal-id', inplace=True)
            
            #Drop title as it does not add much information
            df3.drop('title', axis=1, inplace=True)

            #Drop suites as the informations are not reliable
            df3.drop('suites', axis=1, inplace=True)

            #Drop link as we now parsed the VivaReal ID
            #df3.drop('link', axis=1, inplace=True)

            #Convert to int
            numeric_features = ['area','rooms','bathroom','garages','price','price/m2']
            df3[numeric_features] = df3[numeric_features].astype('int')

            #Clip strange informations
            df3['garages'] = df3['garages'].clip(0,6)
            df3['bathroom'] = df3['bathroom'].clip(0,6)
            df3['rooms'] = df3['rooms'].clip(0,6)

            return df3
        
        df3 = pd.DataFrame()
        searching = st.empty()
        bar = st.progress(0)

        #Add options in sidebar to Tune the Model
        st.sidebar.subheader('Tune Machine Learning')
        eps = st.sidebar.slider('DBSCAN eps: minimum radius between each other\'s features (the lower eps the higher similarity)', 0.0, 1.0, 0.3)
        min_samples = st.sidebar.slider('DBSCAN min_samples: minimum number of ads with same features to form a cluster', 1, 50, 5)

        if st.sidebar.button('Run web scrapper & Refresh dataframe'):

            addresses = ['Rua Jacarandás da Península','Avenida Flamboyants da Península','Avenida das Acácias da Península','Rua Bauhíneas da Península','Rua Pau Brasil da Península','Rua das Bromélias da Península', 'Avenida João Cabral de Mello Neto']

            #Loop addresses and web scrape them all 
            for i,address in enumerate(addresses):

                address_search = address.lower().replace(' ','-').replace('í','i').replace('á','a').replace('é','e').replace('ã','a')
        
                url = f'https://www.vivareal.com.br/venda/rj/rio-de-janeiro/zona-oeste/barra-da-tijuca/{address_search}/apartamento_residencial/'

                searching.text( address + '...' )
            
                df_one_address = scrape_residences( url )
                df3 = df3.append( df_one_address, ignore_index=True )

                bar.progress( (i+1) / len(addresses) )

            searching.text( 'Done! ' + str(len(df3.index)) + ' ads scraped' )
            #Data wrangling
            df3 = clean_dataset( df3 )
            #Save a copy
            df3.to_csv(curpath + '/dataframe.csv')

        @st.cache
        def read_dataframe():
            #To read a copy already saved
            #url_github = 'https://raw.githubusercontent.com/rodpaschoal/Coursera_Capstone/master/dataframe.csv'
            #df3 = pd.read_csv( url_github , error_bad_lines=False)

            df3 = pd.read_csv( curpath + '/dataframe.csv' , error_bad_lines=False)

            #If The CSV has a first empty columns
            #df3.drop('Unnamed: 0', axis=1,inplace=True) 
            return df3 
        
        df3 = read_dataframe()
        searching.text( 'Done! ' + str(len(df3.index)) + ' ads read from csv' )
        bar.progress( 1.0 )
        #Last modified
        try:
            last_modified = time.ctime( os.path.getmtime( curpath + '/dataframe.csv' ) )
            st.text('Last modified - ' + last_modified )
        except Exception as e:
            st.text(e)  

        #Filter dataframe
        #st.write('---')
        st.subheader('Filters')
        filter_rooms = st.slider('Max Rooms', 1,6,6)
        filter_area = st.slider('Max Area',1,600,600)
        filter_price = st.slider('Max Price',1,10000000,10000000)
        filter_pricem2 = st.slider('Max Price/m2',1,20000,20000)
        df3 = df3[ df3['rooms'] <= filter_rooms ]
        df3 = df3[ df3['area'] <= filter_area ]
        df3 = df3[ df3['price'] <= filter_price ]
        df3 = df3[ df3['price/m2'] <= filter_pricem2 ]
        #st.write('---')
        
        #Selecting the numeric features to use and then transform categorical in numeric
        features = ['address','area','rooms','bathroom','garages','price']
        X = pd.get_dummies( df3[features], columns=['address'], prefix='', prefix_sep='' )

        #For distances it is important for to be in the same range (0,1)
        for column in X:
            #X[column] = MinMaxScaler().fit_transform( X[[column]] ) - not a good idea
            X[column] = StandardScaler().fit_transform( X[[column]] )

        #Unsupervised machine learning clustering algorithm
        model = DBSCAN( eps=eps, min_samples=min_samples )
        model.fit( X )
        X['cluster'] = model.labels_
        df3['cluster'] = model.labels_

        #Set to string to Plotly recognize as category later when plot visual
        df3['cluster'] = df3['cluster'].astype('str')
        
        # Best Deal defined - an outlier with very low price/m2 for its address
        best_deals = df3[ (df3['cluster'] == '-1') & ( df3['price/m2'] < df3['price/m2'].mean() ) ]
        n = len( best_deals.index )
        df3.loc[ best_deals.index , 'cluster'] = '-2'

        #Many penthouses in cluster -2, let us create cluster -3 with apartments not greater than 150 m2
        small_best_deals = df3[ (df3['cluster'] == '-2') & (df3['rooms'] <= 3) ]
        n_small = len( small_best_deals.index )
        df3.loc[ small_best_deals.index , 'cluster' ] = '-3'

        #Show Results
        text = 'Resultados'
        text = english(text) if translate else text
        st.subheader( text )
        st.write( len(df3['cluster'].unique()) , 'Clusters' )
        st.text( 'Cluster (-1) : Bad offers' )
        st.text( 'Cluster (-2) : Best 4+ rooms apartments' )
        st.text( 'Cluster (-3) : Best 3- rooms apartments' )
        st.text( 'Others : Normal offers' )
        st.info( 'Hint: double click in right legend isolate a selected cluster' )
        
        #Visualize clusters and result dataframe
        #@st.cache
        def vis_results(df3):
            fig = px.scatter_3d(
                            df3, 
                            x='price/m2',
                            y='address', 
                            z='rooms', 
                            color='cluster',
                            #size='price/m2',
                            #symbol='rooms', 
                            hover_data=['price','area','price/m2','rooms','bathroom','garages','condo','vivareal-id','address'],
                            color_discrete_sequence=px.colors.qualitative.G10
                            )
            st.write( fig )

            #Print dataframe with filters filters
            cols = ['cluster','vivareal-id','price/m2','price','area','rooms','address','bathroom','garages','condo']
            df3 = df3[cols]        
            df3['cluster'] = df3['cluster'].astype('int')
            df3.sort_values('cluster', inplace=True )
            st.write( df3 )

            if n > 0:
                text2 = 'Ofertas na tabela com preço por m2 em promoção, verifique o cluster -3!'
                text2 = english(text2) if translate else text2
                st.write( n_small , text2 )
                st.write( len(df3.index) , 'Total' ) 
            else:
                text4 = 'Não parece ter uma barganha nesse momento'
                text4 = english(text4) if translate else text4
                st.write( text4 )

        vis_results(df3)

        st.markdown( '[VivaReal website](https://www.vivareal.com.br)' )

        if st.checkbox('Show Links'):
            for link in small_best_deals['link']:
                st.write(link) 

    if discussion:
        header = 'Discussão'
        text = 'Como meu primeiro projeto de inteligência artificial, fiquei impressionado com a velocidade em que milhares de anúncios foram capturados, analisados e classificados.'
        draw(header,text)

        text='A facilidade de deploy e a acertividade das classificações do DBSCAN quando abri os anúncios, me fez perceber como ele pode ajudar para fazer análises preliminares de dados.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Na tabela abaixo pode ser verificado o dataframe no qual cada linha é um cluster identificado pelo algoritmo, com o valor médio de cada característica.'
        text = english(text) if translate else text
        st.write( text )

        df3_by_cluster = df3.groupby('cluster').mean()
        df3_by_cluster['n_samples'] = df3.groupby('cluster').count()['price']
        df3_by_cluster['address'] = df3.groupby('cluster').first()['address']
        df3_by_cluster = df3_by_cluster[['n_samples','address','price/m2','price','area','rooms','bathroom','garages','condo']]

        st.write( df3_by_cluster )

        text = 'Ao analisar os clusters -2 e -3, verifica-se um preço por m2 muito abaixo da média, que é:'
        text = english(text) if translate else text
        st.write( text )

        mean_pricem2 = df3['price/m2'].mean()
        st.info( 'R$ {:.0f}/m2'.format(mean_pricem2) )

        text = 'Na verdade, a faixa dos 25% mais baratos é:'
        text = english(text) if translate else text
        st.write( text )

        quartile_pricem2 = df3['price/m2'].quantile(.25)
        st.info( 'R$ {:.0f}/m2'.format(quartile_pricem2) )

        text = 'Esta era exatamente a proposta do projeto, encontrar as melhores ofertas para os clientes.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Pontos de atenção'
        text = english(text) if translate else text
        st.subheader( text )

        text = 'Uma limitação do modelo é incluir muitas coberturas (penthouses) como ofertas diferenciadas, pois como não existem muitos anúncios similares, ele não é capaz de compará-las.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Um cuidado com o uso é notar que o modelo captura anúncios falsos, onde o preço é claramente um golpe para atrair clientes. Prática vulgarmente conhecida como boi de piranha.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Melhorias futuras'
        text = english(text) if translate else text
        st.subheader( text )

        text = 'Uma sugestão para trabalhos futuros seria otimizar o tuning do modelo com métodos como \"knee point\" para identificar o melhor \"eps\" automaticamente. Outra sugestão seria avaliá-lo através métricas de eficiência.'
        text = english(text) if translate else text
        st.write( text )

    if conclusion:
        header = 'Conclusão'
        text = 'Para encontrar uma boa oferta, costumamos filtrar e ordenar manualmente os resultados em páginas de busca de imóveis diversas vezes e repetimos o procedimento quando os anúncios são atualizados.'
        draw(header,text)

        text = 'Com DBSCAN, a gente faz uma busca automática e consegue identificar os apartamentos com as mesmas características (área, dormitórios, banheiros, vagas de garagem e localização) porém com preços totalmente diferentes.'
        text = english(text) if translate else text
        st.write( text )

        text = 'No presente estudo de caso, o modelo analisa cerca de 2000 anúncios na Península em tempo real, i.e., sempre que entram anúncios novos ele refaz novamente o processo.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Na seção \"Discussão\" vemos que é possível economizar até 75% do preço. Essa é uma interessante evidência de como a inteligência artificial pode ajudar pessoas a fazer melhores escolhas.'
        text = english(text) if translate else text
        st.write( text )

        text = 'Espero que esse projeto possa contribuir de alguma forma e estou muito feliz de compartilhá-lo para o mundo.'
        text = english(text) if translate else text
        st.write( text )

        st.code(' print(\'Hello World\') ')

    #Gallery
    if gallery:
        header = 'Galeria de imagens'
        header = english(header) if translate else header
        st.header( header )
        st.image('peninsula-joy.jpg', use_column_width=True)
        
    #Source code (with st.echo() running)
    st.write('---')
    header = 'Código Fonte'
    text = 'Este é um projeto open source desenvolvido para o trabalho final do certificado em Data Science da IBM.'
    draw(header,text)