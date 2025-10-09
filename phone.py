import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.graph_objects as go
import sqlalchemy 
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import plotly.express as px
import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
from PIL import Image

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",         # change to your username
    password="root",     # change to your password
    database="Phonepe"   # change to your db name
)

#STREAMLIT

st.set_page_config(layout= "wide")
st.title("PHONEPE TRANSACTION INSIGHTS")

with st.sidebar:


    select = option_menu("Main Menu",["HOME","DATA VISUALIZATION","INSIGHTS"])

if select=="HOME":
                
        clm1,clm2= st.columns(2)

        with clm1:

                st.header("PHONEPE")
                st.subheader("ANALYSIS & VISUALIZATION")
                st.markdown("CAPSTONE PROJECT")
                
        with clm2:

                st.image(Image.open(r"C:\Users\Welcome\Desktop\pulse\OIP (1).webp"))

  
        df = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")

        fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                color='active cases',
                color_continuous_scale='Reds'
                )

        fig.update_geos(fitbounds="locations", visible=False)

        st.title("INDIA's OVERALL VISUALIZATION")
        st.plotly_chart(fig)
        





elif select == "DATA VISUALIZATION" :
        

            quries= st.selectbox("Select the Quries", [ "1. Total Transactions and Amount by State",
                                                "2. Yearly Transaction",
                                                "3. Transaction Types Distribution",
                                                "4. Yearly Trend for All Brands",
                                                "5. Quarterly Engagement by Brand",
                                                "6. Top 10 State-Year Combinations by Insurance Amount",
                                                "7. Yearly Transaction Volume for All States",
                                                "8. Quarterly Trend for All India",
                                                "9. Quarter-wise Transactions for a State",
                                                "10. District Level User Engagement (App Opens per Registered User)",
                                                "11. Quarter-wise App Opens for a State",
                                                "12. Yearly Growth of User Registrations",
                                                "13. Districts with Highest Avg. Insurance Amount per Transaction",
                                                "14. Quarter-wise Insurance Transactions for a State",
                                                "15. Top 5 Districts by Insurance Amount",
                                                '16. Total Transactions by State',
                                                '17. Top 5 Districts by Transaction Amount',
                                                '18. Yearly Transaction Amount Trend',
                                                '19. Top 5 Pin Codes by Transaction Amount',
                                                '20. Districts with Highest Average Transaction Amount per Transaction',
                                                '21. Highest Average User Registration perQuarter by Pin Code',
                                                '22.Top 5 Pin Codes by User Registration',
                                                '23.Year-wise User Registration Trend',
                                                '24.Highest Average Insurance Transaction per Pin Code',
                                                '25.Quarter-wise Insurance Transactions for a State',
                                                '26.Top 5 Pin Codes by Insurance Transaction Value'])


            if quries == "1. Total Transactions and Amount by State":

                query = """
                SELECT Quarter, SUM(Transaction_amount) AS Total_Amount FROM aggregated_transaction GROUP BY Quarter ORDER BY Quarter;"""
                df = pd.read_sql(query, mydb)
                st.title("Transaction Amount by Quarter")
                st.bar_chart(df.set_index('Quarter')['Total_Amount'])

            elif quries == "2. Yearly Transaction":

                    query2 = """
                    SELECT States, SUM(Transaction_count) AS Total_Transactions FROM aggregated_transaction GROUP BY States ORDER BY Total_Transactions DESC;"""
                    df2 = pd.read_sql(query2, mydb)
                    st.title("Total Transactions by State")
                    st.bar_chart(df2.set_index('States')['Total_Transactions'])
                    
            elif quries == "3. Transaction Types Distribution":

                    query3 = """
                    SELECT Transaction_type, SUM(Transaction_count) AS Total_Transactions
                    FROM aggregated_transaction
                    GROUP BY Transaction_type
                    ORDER BY Total_Transactions DESC;
                    """
                    df3 = pd.read_sql(query3, mydb)
                    st.plotly_chart(
                        px.pie(df3, names='Transaction_type', values='Total_Transactions', title='Transaction Type Distribution'))
                    

            elif quries == "4. Yearly Trend for All Brands":
                
                    query4 = """
                    SELECT Years, Brands, SUM(Transaction_count) AS Users_Per_Year
                    FROM aggregated_users
                    GROUP BY Years, Brands
                    ORDER BY Years, Brands;
                    """
                    df4 = pd.read_sql(query4, mydb)
                    pivot4 = df4.pivot(index="Years", columns="Brands", values="Users_Per_Year")
                    st.title("Users for Each Brand")
                    st.line_chart(pivot4)

            elif quries == "5. Quarterly Engagement by Brand":

                    query5 = """
                    SELECT Years, Quarter, Brands, SUM(Transaction_count) AS Quarterly_Users
                    FROM aggregated_users
                    GROUP BY Years, Quarter, Brands
                    ORDER BY Years, Quarter, Brands;
                    """
                    df5 = pd.read_sql(query5, mydb)
                    heatmap_data = df5.pivot_table(index=['Years','Quarter'], columns='Brands', values='Quarterly_Users', fill_value=0)
                    fig5, ax5 = plt.subplots(figsize=(12, 8))
                    sns.heatmap(heatmap_data, annot=False, cmap="YlGnBu", ax=ax5)
                    st.title("Quarterly Engagement By Brand")
                    st.pyplot(fig5)        


            elif quries == "6. Top 10 State-Year Combinations by Insurance Amount":        
                
                    query6 = """
                    SELECT States, Years, SUM(Transaction_amount) AS State_Year_Amount
                    FROM aggregated_insurance
                    GROUP BY States, Years
                    ORDER BY State_Year_Amount DESC
                    LIMIT 10;
                    """
                    df6 = pd.read_sql(query6, mydb)
                    df6['State-Year'] = df6['States'] + ' ' + df6['Years'].astype(str)
                    st.title("Top 10 state by Insurance Amount")
                    st.bar_chart(df6.set_index('State-Year')['State_Year_Amount'])

            elif quries == "7. Yearly Transaction Volume for All States": 

                    query7 = """
                    SELECT States, Years, SUM(Transaction_count) AS Total_Transactions
                    FROM aggregated_insurance
                    GROUP BY States, Years
                    ORDER BY States, Years;
                    """
                    df7 = pd.read_sql(query7, mydb)
                    pivot7 = df7.pivot(index='States', columns='Years', values='Total_Transactions')
                    fig7, ax7 = plt.subplots(figsize=(12, 8))
                    sns.heatmap(pivot7, annot=False, cmap="YlGnBu", ax=ax7)
                    st.title("Yearly Transaction Volume for All States")
                    st.pyplot(fig7)       


            elif quries == "8. Quarterly Trend for All India":  

                    query8 = """
                    SELECT Years, Quarter, SUM(Transaction_count) AS India_Quarterly_Transactions
                    FROM aggregated_insurance
                    GROUP BY Years, Quarter
                    ORDER BY Years, Quarter;
                    """
                    df8 = pd.read_sql(query8, mydb)
                    df8['Year-Quarter'] = df8['Years'].astype(str) + ' Q' + df8['Quarter'].astype(str)
                    st.title("Quarterly Trend for All India")
                    st.line_chart(df8.set_index('Year-Quarter')['India_Quarterly_Transactions'])      

            elif quries == "9. Quarter-wise Transactions for a State":        
                
                    query9 = """
                    SELECT States, SUM(Transaction_count) AS total_transactions
                    FROM map_trans
                    GROUP BY States
                    ORDER BY total_transactions DESC;
                    """
                    df9 = pd.read_sql(query9, mydb)
                    fig9 = px.bar(df9, x='States', y='total_transactions', title='Total Transactions by State')
                    st.plotly_chart(fig9)

            elif quries == "10. District Level User Engagement (App Opens per Registered User)":
                
                    query10 = """
                    SELECT Districts, SUM(Transaction_amount) AS total_amount
                    FROM map_trans
                    GROUP BY Districts
                    ORDER BY total_amount DESC
                    LIMIT 5;
                    """
                    df10 = pd.read_sql(query10, mydb)
                    fig10 = px.pie(df10, names='Districts', values='total_amount', title='Top 5 Districts by Transaction Amount')
                    st.plotly_chart(fig10)


            elif quries == "11. Quarter-wise App Opens for a State":

                    query11 = """
                    SELECT Years, Quarter, SUM(Transaction_count) AS total_transactions
                    FROM map_trans
                    WHERE States = 'west-bengal'
                    GROUP BY Years, Quarter
                    ORDER BY Years, Quarter;
                    """
                    df11 = pd.read_sql(query11, mydb)
                    fig11 = px.bar(df11, x='Quarter', y='total_transactions', color='Years', barmode='group',
                                title='Quarter-wise Transactions for West Bengal')
                    st.plotly_chart(fig11)                        


            elif quries == "12. Yearly Growth of User Registrations":        
                
                    query12 = """
                    SELECT Districts, SUM(AppOpens) / SUM(RegisteredUsers) AS app_opens_per_user
                    FROM map_user
                    GROUP BY Districts
                    ORDER BY app_opens_per_user DESC
                    LIMIT 10;
                    """
                    df12 = pd.read_sql(query12, mydb)
                    fig12 = px.bar(df12, x='Districts', y='app_opens_per_user', title='App Opens per Registered User by District')
                    st.plotly_chart(fig12)

            elif quries == "13. Districts with Highest Avg. Insurance Amount per Transaction":
                
                    query13 = """
                    SELECT Years, Quarter, SUM(AppOpens) AS total_app_opens
                    FROM map_user
                    WHERE States = 'west-bengal'
                    GROUP BY Years, Quarter
                    ORDER BY Years, Quarter;
                    """
                    df13 = pd.read_sql(query13, mydb)
                    fig13 = px.bar(df13, x='Quarter', y='total_app_opens', color='Years', barmode='group', title='Quarter-wise App Opens: West Bengal')
                    st.plotly_chart(fig13)

            elif quries == "14. Quarter-wise Insurance Transactions for a State":
                
                    query14 = """
                    SELECT Years, SUM(RegisteredUsers) AS yearly_users
                    FROM map_user
                    GROUP BY Years
                    ORDER BY Years;
                    """
                    df14 = pd.read_sql(query14, mydb)
                    fig14 = px.line(df14, x='Years', y='yearly_users', markers=True, title='Yearly Growth of User Registrations')
                    st.plotly_chart(fig14)


            elif quries == "15. Top 5 Districts by Insurance Amount":
                
                    query15 = """
                    SELECT Districts, AVG(Transaction_amount) AS avg_amount
                    FROM map_insc
                    GROUP BY Districts
                    ORDER BY avg_amount DESC
                    LIMIT 10;
                    """
                    df15 = pd.read_sql(query15, mydb)
                    fig15 = px.bar(df15, x='Districts', y='avg_amount',
                                title='Highest Avg. Insurance Amount per Transaction by District')
                    st.plotly_chart(fig15)
            

            elif quries == '16. Total Transactions by State':
                
                    query16 = """
                    SELECT Years, Quarter, SUM(Transaction_count) AS total_transactions
                    FROM map_insc
                    WHERE States = 'west-bengal'
                    GROUP BY Years, Quarter
                    ORDER BY Years, Quarter;
                    """
                    df16 = pd.read_sql(query16, mydb)
                    fig16 = px.bar(df16, x='Quarter', y='total_transactions', color='Years', barmode='group',
                                title='Quarter-wise Insurance Transactions: West Bengal')
                    st.plotly_chart(fig16)
            

            elif quries == '17. Top 5 Districts by Transaction Amount':
                
                    query17 = """
                    SELECT Districts, SUM(Transaction_amount) AS total_amount
                    FROM map_insc
                    GROUP BY Districts
                    ORDER BY total_amount DESC
                    LIMIT 5;
                    """
                    df17 = pd.read_sql(query17, mydb)
                    fig17 = px.pie(df17, names='Districts', values='total_amount', title='Top 5 Districts by Insurance Amount')
                    st.plotly_chart(fig17)

            
            elif quries == '18. Yearly Transaction Amount Trend':
                
                    query18 = """
                    SELECT Years, SUM(Transaction_amount) AS yearly_amount
                    FROM top_trans
                    GROUP BY Years
                    ORDER BY Years;
                    """
                    df18 = pd.read_sql(query18, mydb)
                    fig18 = px.line(df18, x='Years', y='yearly_amount', markers=True, title='Yearly Transaction Amount Trend')
                    st.plotly_chart(fig18)

            elif quries == '19. Top 5 Pin Codes by Transaction Amount':
                
                    query19 = """
                    SELECT Pincodes, SUM(Transaction_amount) AS total_amount
                    FROM top_trans
                    GROUP BY Pincodes
                    ORDER BY total_amount DESC
                    LIMIT 5;
                    """
                    df19 = pd.read_sql(query19, mydb)
                    fig19 = px.pie(df19, names='Pincodes', values='total_amount', title='Top 5 Pin Codes by Transaction Amount')
                    st.plotly_chart(fig19)
                

            elif quries == '20. Districts with Highest Average Transaction Amount per Transaction':

                    query20= """
                    SELECT Pincodes, AVG(Transaction_amount) AS avg_amount
                    FROM top_trans
                    GROUP BY Pincodes
                    ORDER BY avg_amount DESC
                    LIMIT 10;
                    """
                    df20 = pd.read_sql(query20, mydb)
                    fig20 = px.bar(df20, x='Pincodes', y='avg_amount',
                                title='Highest Average Transaction Amount per Transaction by District')
                    st.plotly_chart(fig20)


            elif quries == '21. Highest Average User Registration perQuarter by Pin Code':
                
                    query21 = """
                    SELECT Pincodes, AVG(RegisteredUsers) AS avg_users
                    FROM top_user
                    GROUP BY Pincodes
                    ORDER BY avg_users DESC
                    LIMIT 10;
                    """
                    df21 = pd.read_sql(query21, mydb)
                    fig21 = px.bar(df21, x='Pincodes', y='avg_users', title='Highest Avg. User Registration per Quarter by Pin Code')
                    st.plotly_chart(fig21)

            elif quries == '22.Top 5 Pin Codes by User Registration':
                
                    query22 = """
                    SELECT Pincodes, SUM(RegisteredUsers) AS total_users
                    FROM top_user
                    GROUP BY Pincodes
                    ORDER BY total_users DESC
                    LIMIT 5;
                    """
                    df22 = pd.read_sql(query22, mydb)
                    fig22 = px.pie(df22, names='Pincodes', values='total_users', title='Top 5 Pin Codes by User Registration')
                    st.plotly_chart(fig22)

            elif quries == '23.Year-wise User Registration Trend':
                
                    query23 = """
                    SELECT Years, SUM(RegisteredUsers) AS yearly_users
                    FROM top_user
                    GROUP BY Years
                    ORDER BY Years;
                    """
                    df23 = pd.read_sql(query23, mydb)
                    fig23 = px.line(df23, x='Years', y='yearly_users', markers=True, title='Year-wise User Registration Trend')
                    st.plotly_chart(fig23)

            elif quries == '24.Highest Average Insurance Transaction per Pin Code':
                
                    query24 = """
                    SELECT Pincodes, AVG(Transaction_amount) AS avg_amount
                    FROM top_insc
                    GROUP BY Pincodes
                    ORDER BY avg_amount DESC
                    LIMIT 10;
                    """
                    df24 = pd.read_sql(query24, mydb)
                    fig24 = px.bar(df24, x='Pincodes', y='avg_amount', title='Highest Avg. Insurance Transaction per Pin Code')
                    st.plotly_chart(fig24)

            elif quries == '25.Quarter-wise Insurance Transactions for a State':
                
                    query25 = """
                    SELECT Years, Quarter, SUM(Transaction_count) AS total_transactions
                    FROM top_insc
                    WHERE States = 'west-bengal'
                    GROUP BY Years, Quarter
                    ORDER BY Years, Quarter;
                    """
                    df25 = pd.read_sql(query25, mydb)
                    fig25 = px.bar(df25, x='Quarter', y='total_transactions', color='Years', barmode='group',
                                title='Quarter-wise Insurance Transactions: West Bengal')
                    st.plotly_chart(fig25)

            elif quries == '26.Top 5 Pin Codes by Insurance Transaction Value':
                
                    query26 = """
                    SELECT Pincodes, SUM(Transaction_amount) AS total_amount
                    FROM top_insc
                    GROUP BY Pincodes
                    ORDER BY total_amount DESC
                    LIMIT 5;
                    """
                    df26 = pd.read_sql(query26, mydb)
                    fig26 = px.pie(df26, names='Pincodes', values='total_amount', title='Top 5 Pin Codes by Insurance Transaction Amount')
                    st.plotly_chart(fig26)


elif select == "INSIGHTS":
        
        i_r= st.selectbox("INSIGHTS & RECOMMENDATION", [ "1. High Transaction States Lead Payments",
                                                          "2. Quarter-on-Quarter Growth Is Strong",
                                                          "3. Some States Lag Behind",
                                                          "4. District Level Engagement Is Uneven",
                                                          "5. Rapid User Growth Until 2021, Then Decline",
                                                          "6. Top 5 Districts by Insurance Amount",
                                                          "7. Yearly Transaction Amount Trend",
                                                          "8. Quarter-wise Insurance Transactions for West Benga",
                                                          "9. Yearly Growth of User Registrations",
                                                          "10.Districts with Highest Average Transaction Amount per Transaction"])

        if i_r ==  "1. High Transaction States Lead Payments":

                ''' States like Maharashtra, Karnataka, and Tamil Nadu show the 
                 highest yearly transaction values,
                 indicating concentrated digital payment 
                 activity and user adoption.

                • Recommendation:
                 
                   Strengthen partnerships and merchant onboarding in these states to 
                   further boost digital penetration develop tailored offers.'''

    
        if i_r ==  "2. Quarter-on-Quarter Growth Is Strong":

                '''Transaction amounts have increased steadily from Q1 to Q4, suggesting strong growth in digital 
                  across periods. 
  
                •Recommendation : 
                
                   Capitalize on quarterly growth trends by launching targeted 
                   campaigns at the start of each quarter.'''
                
        if i_r ==  "3. Some States Lag Behind":

                '''Smaller states and UTs like Lakshadweep and Andaman-Nicobar show 
                minimal transaction activity and volume.

                •Recommendation:

                  Increase awareness campaigns and improve 
                  in underpenetrated regions.'''
                
        if i_r ==  "4. District Level Engagement Is Uneven":

                '''Districts such as Bengaluru Urban, Hyderabad, and Pune dominate 
                transaction amounts, while others lag considerably.   
    
                •Recommendation: 
                
                  Launch district-specific promotions and study driving
                  factors in high-engagement areas for replication.'''
                
        if i_r =="5. Rapid User Growth Until 2021, Then Decline":

                '''Yearly user trend data indicates a sharp increase till 2021,
                  followed by a drop in 2022 for most brands.    
  
                •Recommendation: 
                
                  Investigate the causes of the 2022 decline and address retention
                  issues with loyalty programs.'''
                
        if i_r ==  "6. Top 5 Districts by Insurance Amount":

                '''Bengaluru, Pune, Thane, Rangareddy, and Chennai dominate insurance transactions.

                •Recommendation: 
                  
                  Expand insurance awareness and digital penetration strategies 
                  other emerging districts to diversify revenue.'''
                
        if i_r ==  "7. Yearly Transaction Amount Trend":

                '''There is a significant peak followed by a decline and then a resurgence 
                in transaction amounts over years.

                •Recommendation:

                  Investigate causes of transaction dips and capitalize on growth
                  phases with targeted campaigns.'''

        if i_r ==  "8. Quarter-wise Insurance Transactions for West Bengal":

                '''Growth is observed over quarters with an increasing trend each year.

                •Recommendation: 
                
                  Maintain steady growth by improving insurance product 
                  variety and simplifying purchase processes quarterly.'''

        
        if i_r ==  "9. Yearly Growth of User Registrations":

                '''There is an upward trend in user registrations, showing increasing adoption.

                •Recommendation: 
                
                  Focus on onboarding through promotions and easy signup to keep the growth momentum.'''

        if i_r ==  "10.Districts with Highest Average Transaction Amount per Transaction":

                '''Some districts exhibit very high average transaction values, indicating high-value users.

                •Recommendation:                 

                  Target high-value districts with premium 
                  services and personalized financial products.'''