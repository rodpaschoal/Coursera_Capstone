{\rtf1\ansi\ansicpg1252\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red31\green31\blue31;\red239\green239\blue239;}
{\*\expandedcolortbl;;\cssrgb\c16078\c16078\c16078;\cssrgb\c94902\c94902\c94902;}
\paperw11900\paperh16840\margl1440\margr1440\vieww15720\viewh8840\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs32 \cf2 \cb3 \expnd0\expndtw0\kerning0
FROM python:3.7-slim\cb1 \
\cb3 COPY . /app\cb1 \
\cb3 WORKDIR /app\cb1 \
\cb3 RUN pip install -r requirements.txt\cb1 \
\cb3 EXPOSE 80\cb1 \
\cb3 RUN mkdir ~/.streamlit\cb1 \
\cb3 RUN cp config.toml ~/.streamlit/config.toml\cb1 \
\cb3 RUN cp credentials.toml ~/.streamlit/credentials.toml\cb1 \
\cb3 WORKDIR /app\cb1 \
\cb3 ENTRYPOINT ["streamlit", "run"]\cb1 \
\cb3 CMD ["census_app.py"]}