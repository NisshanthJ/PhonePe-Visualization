import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import time

import mysql.connector
from sqlalchemy import create_engine


mydb = mysql.connector.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor(buffered=True)
engine = create_engine("mysql+mysqlconnector://root:@localhost/phonepedb") 


mycursor.execute('create database if not exists phonepedb')
mycursor.execute('use phonepedb')


icon='https://cdn.iconscout.com/icon/free/png-512/free-phonepe-2709167-2249157.png?f=webp&w=256'
st.set_page_config(page_title='PHONEPE PULSE',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide')

title_text = '''<h1 style='font-size: 36px;color:white;text-align: center'>PHONEPE PULSE PROJECT</h1>'''
st.markdown(title_text, unsafe_allow_html=True)


selected = option_menu("PHONEPE",
                        options=["Introduction", "Visualization", "Insights"],
                        default_index=1,
                        orientation="vertical",
                        styles={"container": {"width": "100%","border": "2px ridge #000000","background-color": "	#353935"},
                                "icon": {"color": "#F8CD47", "font-size": "20px"}
                               
                           })


if selected =="Introduction":
        col1,col2=st.columns(2)
        with col1:
                st.subheader(':brown[Problem Statement:]')
                st.markdown('''<h5> The Phonepe pulse Github repository contains a large amount of data related to
various metrics and statistics. The goal is to extract this data and process it to obtain
insights and information that can be visualized in a user-friendly manner.<h5>''',unsafe_allow_html=True)


if selected =="Visualization":
        
        def ind_geo():
                geo="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                return geo
        
        geo_type = st.radio('Category Selection',["**Transactions**","**Users**"], index = None)

        if geo_type=="**Transactions**":
                trans_geo_year_wise = st.toggle('Year-Wise')

                if not trans_geo_year_wise:
                        cat=st.radio('Category Selection',["Transaction Amount","Transaction Count"])
                        if cat =="Transaction Amount":
                                st.title(":white[ Net Transaction Amount for inclusive of all the years ]")

                                df = pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Total Transaction Amount',
                                        AVG(Transaction_amount) as 'Average Transaction Amount'
                                        from agg_transaction
                                        GROUP by state''',con=engine)

                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale='Viridis',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.plotly_chart(fig,use_container_width = True)

                        if cat =="Transaction Count":
                                st.title(":white[Net Transaction Count for States inclusive of all the years]")

                                df = pd.read_sql_query('''SELECT state,sum(Transaction_count) as 'Total Transaction Count',
                                        AVG(Transaction_count) as 'Average Transaction Count'
                                        from agg_transaction
                                        GROUP by state''',con=engine)

                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Count',
                                        color_continuous_scale='Viridis',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.plotly_chart(fig,use_container_width = True)

                if trans_geo_year_wise:
                        df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from agg_transaction''',con=engine)
                        selected_year = st.select_slider("Select Year",options=df_year['Year'].tolist())
                        trans_geo_quater_wise= st.toggle('Quater-Wise')

                        if not trans_geo_quater_wise:
                                df = pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Total Transaction Amount',
                                                AVG(Transaction_amount) as 'Average Transaction Amount',
                                                sum(Transaction_count) as 'Total Transaction Count',
                                                AVG(Transaction_count) as 'Average Transaction Count'
                                                from agg_transaction where year=%s
                                                GROUP by state''',con=engine,params=[(selected_year,)])
                        
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount','Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale=px.colors.sequential.Plasma,
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Transaction Amount and Count for States in {selected_year}  ]")
                                st.plotly_chart(fig,use_container_width = True)

                        if trans_geo_quater_wise:
                                df_quater=pd.read_sql_query('''SELECT DISTINCT Quater as 'Quater' from agg_transaction''',con=engine)
                                selected_Quater = st.select_slider("Select Quater",options=df_quater['Quater'].tolist())

                                df = pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Total Transaction Amount',
                                                AVG(Transaction_amount) as 'Average Transaction Amount',
                                                sum(Transaction_count) as 'Total Transaction Count',
                                                AVG(Transaction_count) as 'Average Transaction Count'
                                                from agg_transaction where year=%s and Quater=%s
                                                GROUP by state''',con=engine,params=(selected_year, selected_Quater))
                                
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount','Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale=px.colors.sequential.matter_r,
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Transaction Amount and Count for States in {selected_year}-Q{selected_Quater}]")
                                st.plotly_chart(fig,use_container_width = True)

        if geo_type=="**Users**":
                user_geo_year_wise = st.toggle('Year-Wise')

                if not user_geo_year_wise:
                        st.title(":violet[ Total Register users Across States-Sum of all Year ]")

                        df = pd.read_sql_query('''SELECT DISTINCT state, SUM(Registered_Users) as 'Total Registered User',
                                        AVG(Registered_Users) as 'Average Register User'
                                        FROM map_user
                                        GROUP BY state''',con=engine)

                        fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='state',
                                        hover_data=['Total Registered User','Average Register User'],
                                        color='Total Registered User',
                                        color_continuous_scale='Viridis',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                        fig.update_layout(height=600)
                        st.plotly_chart(fig,use_container_width = True)

                if user_geo_year_wise:
                        df_year=pd.read_sql_query('''SELECT DISTINCT year as 'Year' from map_user''',con=engine)
                        selected_year = st.select_slider("Select Year",options=df_year['Year'].tolist())
                        user_geo_quater_wise= st.toggle('Quater-Wise')

                        if not user_geo_quater_wise:
                                df = pd.read_sql_query('''SELECT DISTINCT state, SUM(Registered_Users) as 'Total Registered User',
                                                AVG(Registered_Users) as 'Average Register User'
                                                FROM map_user WHERE  year=%s
                                                GROUP BY state''',con=engine,params=[(selected_year,)])
                        
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                locations='state',
                                                hover_data=['Total Registered User','Average Register User'],
                                                color='Total Registered User',
                                                color_continuous_scale=px.colors.sequential.Plasma,
                                                mapbox_style="carto-positron",zoom=3.5,
                                                center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Registered User for States in {selected_year}  ]")
                                st.plotly_chart(fig,use_container_width = True)

                        if user_geo_quater_wise:
                                df_quater=pd.read_sql_query('''SELECT DISTINCT Quater as 'Quater' from map_user''',con=engine)
                                selected_Quater = st.select_slider("Select Quater",options=df_quater['Quater'].tolist())

                                df = pd.read_sql_query('''SELECT DISTINCT state, SUM(Registered_Users) as 'Total Registered User',
                                                AVG(Registered_Users) as 'Average Register User'
                                                FROM map_user WHERE  year=%s and Quater=%s
                                                GROUP BY state''',con=engine,params=(selected_year,selected_Quater))
                        
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                locations='state',
                                                hover_data=['Total Registered User','Average Register User'],
                                                color='Total Registered User',
                                                color_continuous_scale=px.colors.sequential.matter_r,
                                                mapbox_style="carto-positron",zoom=3.5,
                                                center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Registered User for States in {selected_year}-Q{selected_Quater} ]")
                                st.plotly_chart(fig,use_container_width = True)


if selected =="Insights":
        select_insight=option_menu('',options=["Insights"],
                                orientation='horizontal',
                                styles={"container":{"border": "2px ridge #000000"},
                                })
        
        if select_insight =="Insights":
                qust=[  'Top 10 states with highest transaction',
                        'Top 10 states with lowest transaction',
                        'Top 10 states with highest Registered User',
                        'Top 10 District with highest transaction',
                        'Top 10 District with lowest transaction',
                        'Top 10 District with highest Registered User',
                        'Top 10 Brands widely prefered for Transaction',
                        'Sum of Transaction by Type or categories',
                        'Top 10 Postal code with highest Transaction',
                        'Top 10 Postal code with highest Registered user'
                        ]
                query=st.selectbox(':white[Choose a query]',options=qust,index=None)


                if query=='Top 10 states with highest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Transaction Amount'
                                        from agg_transaction
                                        GROUP by state
                                        ORDER by sum(Transaction_amount) DESC LIMIT 10;''',con=engine)
                                
                                fig=px.bar(df,x='state',y='Transaction Amount',
                                                color='state',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 state of Highest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT state, SUM(Transaction_count) AS 'Transaction Count' FROM agg_transaction
                                                WHERE state IN ( SELECT state FROM 
                                                (SELECT state, SUM(Transaction_amount) AS amount FROM agg_transaction 
                                                GROUP BY state ORDER BY amount DESC LIMIT 10 )as top_state )
                                                GROUP BY state order by sum(Transaction_count) DESC''',con=engine)
                                
                                fig=px.bar(df,x='state',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        

                if query=='Top 10 states with lowest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT state,sum(Transaction_amount) as 'Transaction Amount'
                                        from agg_transaction GROUP by state
                                        ORDER by sum(Transaction_amount) ASC LIMIT 10''',con=engine)
                                df['state']=df['state'].str.replace('Dadra and Nagar Haveli and Daman and Diu','Dadra')

                                fig=px.bar(df,x='state',y='Transaction Amount',
                                                color='state',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 state of lowest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                        with col2:
                                df=pd.read_sql_query('''SELECT state, SUM(Transaction_count) AS 'Transaction Count' FROM agg_transaction
                                                WHERE state IN ( SELECT state FROM 
                                                (SELECT state, SUM(Transaction_amount) AS amount FROM agg_transaction 
                                                GROUP BY state ORDER BY amount ASC LIMIT 10 )as top_state )
                                                GROUP BY state order by sum(Transaction_count) ASC''',con=engine)
                                df['state']=df['state'].str.replace('Dadra and Nagar Haveli and Daman and Diu','Dadra')
                                
                                fig=px.bar(df,x='state',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                    
                   
                if query=='Top 10 states with highest Registered User':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT state ,sum(Registered_Users) as 'Registered User' FROM map_user 
                                                GROUP BY state ORDER BY sum(Registered_Users) DESC limit 10''',con=engine)
                                
                                fig=px.bar(df,x='state',y='Registered User',
                                                color='state',
                                                hover_data=['Registered User'],
                                                title='Top 10 state of highest Registered User',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT state, SUM(App_Opens) AS 'App Opened' FROM map_user WHERE state IN 
                                                (SELECT state  FROM (SELECT state, SUM(Registered_Users) AS 'R_user'
                                                FROM map_user GROUP BY state ORDER BY sum(Registered_Users) DESC LIMIT 10)as top_user )
                                                GROUP BY state ORDER BY sum(App_Opens) DESC''',con=engine)
                                
                                fig=px.bar(df,x='state',y='App Opened',
                                                color='App Opened',
                                                hover_data=['App Opened'],
                                                title='App Opened',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                     

                if query=='Top 10 District with highest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT District,sum(Transaction_amount) as 'Transaction Amount'
                                        from map_transaction GROUP by District
                                        ORDER by sum(Transaction_amount) DESC LIMIT 10;''',con=engine)
                                df['District']=df['District'].str.replace('Central','Delhi Central')
                                
                                fig=px.bar(df,x='District',y='Transaction Amount',
                                                color='District',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 District of Highest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT District, SUM(Transaction_count) AS 'Transaction Count' FROM map_transaction 
                                        WHERE District IN (SELECT District  FROM (SELECT District, SUM(Transaction_amount) AS 'amount' 
                                        FROM map_transaction GROUP BY District ORDER BY amount DESC LIMIT 10)as top_dist )
                                        GROUP BY District ORDER BY SUM(Transaction_count) DESC;''',con=engine)
                                df['District']=df['District'].str.replace('Central','Delhi Central')

                                fig=px.bar(df,x='District',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        

                if query=='Top 10 District with lowest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT District,sum(Transaction_amount) as 'Transaction Amount'
                                        from map_transaction GROUP by District
                                        ORDER by sum(Transaction_amount) ASC LIMIT 10;''',con=engine)
                                
                                fig=px.bar(df,x='District',y='Transaction Amount',
                                                color='District',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 District of Lowest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT District, SUM(Transaction_count) AS 'Transaction Count' FROM map_transaction 
                                        WHERE District IN (SELECT District  FROM (SELECT District, SUM(Transaction_amount) AS 'amount' 
                                        FROM map_transaction GROUP BY District ORDER BY amount ASC LIMIT 10)as top_dist )
                                        GROUP BY District ORDER BY SUM(Transaction_count) ASC;''',con=engine)

                                fig=px.bar(df,x='District',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Transaction Count',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)



                if query=='Top 10 Brands widely prefered for Transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT DISTINCT User_brand as 'User Brand' ,SUM(User_count) as 'Count'
                                                FROM agg_user GROUP BY User_brand
                                                order by SUM(User_count) DESC LIMIT 10''',con=engine)
                                
                                fig=px.bar(df,x='User Brand',y='Count',
                                                color='User Brand',
                                                hover_data=['Count'],
                                                title='Top 10 Brands widely prefered for Transaction (sum of all states)',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df=pd.read_sql_query('''SELECT User_brand AS 'User Brand', (SUM(User_count) / total_count) * 100 AS 'Percentage'
                                                FROM agg_user
                                                CROSS JOIN (SELECT SUM(User_count) AS total_count FROM agg_user) AS total
                                                GROUP BY User_brand
                                                ORDER BY SUM(User_count) DESC LIMIT 10;''',con=engine)
                                
                                fig=px.pie(df,names='User Brand',values='Percentage',color='User Brand',
                                                title='Percentage',
                                                color_discrete_sequence=px.colors.qualitative.Bold)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                      
                      

                if query=='Top 10 District with highest Registered User':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT District, sum(Registered_Users) as 'Registered User' FROM map_user
                                        GROUP BY District ORDER BY sum(Registered_Users) DESC LIMIT 10''',con=engine)
                                
                                fig=px.bar(df,x='District',y='Registered User',
                                                color='District',
                                                hover_data=['Registered User'],
                                                title='Top 10 District of highest Registered User ',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                        with col2:
                                df=pd.read_sql_query('''SELECT District, SUM(App_Opens) AS 'App Opened' FROM map_user WHERE District IN 
                                                (SELECT District  FROM (SELECT District, SUM(Registered_Users) AS 'R_user'
                                                FROM map_user GROUP BY District ORDER BY sum(Registered_Users) DESC LIMIT 10)as top_user )
                                                GROUP BY District ORDER BY sum(App_Opens) DESC''',con=engine)
                                
                                fig=px.bar(df,x='District',y='App Opened',
                                                color='App Opened',
                                                hover_data=['App Opened'],
                                                title='App Opened',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
             

                if query=='Sum of Transaction by Type or categories':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT DISTINCT Transaction_type as 'categories',SUM(Transaction_amount) as 'Transaction Amount'
                                                        from agg_transaction GROUP BY Transaction_type DESC''',con=engine)
                                
                                fig=px.pie(df,names='categories',values='Transaction Amount',color='categories',
                                                title='Sum of Transaction Amount by categories',hole=0.3,
                                                color_discrete_sequence=px.colors.qualitative.Bold)
                                st.plotly_chart(fig,use_container_width=True)
                        
                        with col2:
                                st.subheader('Sum of Transaction Amount')
                                st.dataframe(df,hide_index=True)
                      
                if query=='Top 10 Postal code with highest Transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT Pincode, sum(Transaction_amount) as 'Transaction Amount' FROM top_transaction
                                                GROUP BY Pincode ORDER BY sum(Transaction_amount) DESC LIMIT 10''',con=engine)
                                
                                fig=px.pie(df,names='Pincode',values='Transaction Amount',
                                                color="Pincode",
                                                title='Top 10 Postal code of highest Transaction Amount ',
                                                color_discrete_sequence=px.colors.qualitative.Pastel_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                        with col2:
                                df=pd.read_sql_query('''SELECT Pincode , SUM(Transaction_count) AS 'Transaction Count' FROM top_transaction
                                                WHERE Pincode IN (SELECT Pincode FROM (SELECT Pincode, SUM(Transaction_amount) AS 't_amt' 
                                                FROM top_transaction GROUP BY Pincode ORDER BY SUM(Transaction_amount) DESC LIMIT 10)as top_tran ) 
                                                GROUP BY Pincode ORDER BY SUM(Transaction_count) DESC;''',con=engine)
                                
                                fig=px.pie(df,names='Pincode',values='Transaction Count',
                                                color='Transaction Count',
                                                title='Transaction Count',
                                                color_discrete_sequence=px.colors.qualitative.Dark2_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                if query=='Top 10 Postal code with highest Registered user':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT Pincode, sum(Registered_Users) as 'Registered user' FROM top_user
                                                GROUP BY Pincode ORDER BY  sum(Registered_Users) DESC LIMIT 10''',con=engine)
                                
                                fig=px.pie(df,names='Pincode',values='Registered user',
                                                color="Pincode",
                                                title='Top 10 Postal code with highest Registered user ',
                                                color_discrete_sequence=px.colors.qualitative.Pastel_r)
                                st.plotly_chart(fig,use_container_width=True)

                        with col2:
                                st.write('Top 10 Postal code with highest Registered user')
                                st.dataframe(df,hide_index=True)
                        
