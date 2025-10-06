# phone-visualization
The PhonePe Pulse project is a comprehensive data science mini-project that extracts, processes, and visualizes transaction data from the PhonePe Pulse platform. The project involves gathering large volumes of digital payment transaction data from the PhonePe Pulse GitHub repository, tabulating and cleaning the dataset, and storing it efficiently for further analysis. Using Python, Streamlit, and SQL databases, the project delivers interactive dashboards that offer deep insights into payment trends, transaction patterns, and customer behavior across different states and time periods in India. This project demonstrates the power of modern data visualization and analytics, making complex fintech data both accessible and actionable for business intelligence and decision-making.


Key features include:

                      >Data extraction and transformation from
                      JSON to DataFrame and storage in SQL databases.
                      
                      >Interactive, user-friendly dashboards built with
                      Streamlit for visual exploration of digital payment data.
                      
                      >Insights into trends at the state, district, year, and quarter level,
                      supporting analysis for industry and academic purposes.



This project highlights skills in data engineering, cleaning, analysis, and dynamic visualization using modern data science tools.




#TABLE CREATION

#AGGREGATED TABLES

#agg_tran


create_table_1='''CREATE TABLE if not exists aggregated_transaction (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Transaction_type VARCHAR(50),
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount DECIMAL(20,2))'''
cursor.execute(create_table_1)
mydb.commit()



insert_table_1 = '''INSERT INTO aggregated_transaction(States,Years,Quarter,Transaction_type,
                                                        Transaction_count,
                                                        Transaction_amount)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = aggre_transaction.values.tolist()
cursor.executemany(insert_table_1,data)
mydb.commit()



#agg_user

create_table_2='''CREATE TABLE if not exists aggregated_users (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Brands VARCHAR(50),
                                                                        Transaction_count BIGINT,
                                                                        Percentage FLOAT)'''
cursor.execute(create_table_2)
mydb.commit()



insert_table_2 = '''INSERT INTO aggregated_users(States,Years,Quarter,Brands,
                                                        Transaction_count,
                                                        Percentage)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = aggre_user.values.tolist()
cursor.executemany(insert_table_2,data)
mydb.commit()


#agg_ins

create_table_3='''CREATE TABLE if not exists aggregated_insurance (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Transaction_type VARCHAR(50),
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount DECIMAL(20,2))'''
cursor.execute(create_table_3)
mydb.commit()



insert_table_3 = '''INSERT INTO aggregated_insurance(States,Years,Quarter,Transaction_type,
                                                        Transaction_count,
                                                        Transaction_amount)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = aggre_insurance.values.tolist()
cursor.executemany(insert_table_3,data)
mydb.commit()




#MAP_TABLES


#map_tran

create_table_4='''CREATE TABLE if not exists map_trans (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Districts VARCHAR(50),
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount DECIMAL(20,2))'''
cursor.execute(create_table_4)
mydb.commit()



insert_table_4 = '''INSERT INTO map_trans(States,Years,Quarter,Districts,
                                                        Transaction_count,
                                                        Transaction_amount)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = map_tran.values.tolist()
cursor.executemany(insert_table_4,data)
mydb.commit()



#map_user

create_table_5='''CREATE TABLE if not exists map_user (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Districts VARCHAR(50),
                                                                        RegisteredUsers BIGINT,
                                                                        AppOpens BIGINT)'''
cursor.execute(create_table_5)
mydb.commit()



insert_table_5 = '''INSERT INTO map_user(States,Years,Quarter,Districts,
                                                        RegisteredUsers,
                                                        AppOpens)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = map_user.values.tolist()
cursor.executemany(insert_table_5,data)
mydb.commit()




#MAP_INSU

create_table_6='''CREATE TABLE if not exists map_insc (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Districts VARCHAR(50),
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount DECIMAL(20,2))'''
cursor.execute(create_table_6)
mydb.commit()



insert_table_6 = '''INSERT INTO map_insc(States,Years,Quarter,Districts,
                                                        Transaction_count,
                                                       Transaction_amount)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = map_insc.values.tolist()
cursor.executemany(insert_table_6,data)
mydb.commit()



#TOP_TABLES

#TOP_TRANS

create_table_7='''CREATE TABLE if not exists top_trans (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Pincodes INT,
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount DECIMAL(20,2))'''
cursor.execute(create_table_7)
mydb.commit()



insert_table_7 = '''INSERT INTO top_trans(States,Years,Quarter,Pincodes,
                                                        Transaction_count,
                                                        Transaction_amount)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = top_trans.values.tolist()
cursor.executemany(insert_table_7,data)
mydb.commit()



#TOP_USER

create_table_8='''CREATE TABLE if not exists top_user (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Pincodes INT,
                                                                        RegisteredUsers BIGINT)'''
cursor.execute(create_table_8)
mydb.commit()



insert_table_8 = '''INSERT INTO top_user(States,Years,Quarter,Pincodes,
                                                        RegisteredUsers)


                                                        values(%s,%s,%s,%s,%s)'''
data = top_user.values.tolist()
cursor.executemany(insert_table_8,data)
mydb.commit()


#TOP_INSU

create_table_9='''CREATE TABLE if not exists top_insc (
                                                                        States VARCHAR(50),
                                                                        Years   INT,
                                                                        Quarter INT,
                                                                        Pincodes INT,
                                                                        Transaction_count BIGINT,
                                                                        Transaction_amount DECIMAL(20,2))'''
cursor.execute(create_table_9)
mydb.commit()



insert_table_9 = '''INSERT INTO top_insc(States,Years,Quarter,Pincodes,
                                                        Transaction_count,
                                                        Transaction_amount)


                                                        values(%s,%s,%s,%s,%s,%s)'''
data = top_ins.values.tolist()
cursor.executemany(insert_table_9,data)
mydb.commit()





<img width="1105" height="604" alt="image" src="https://github.com/user-attachments/assets/1c95b39e-8186-4ad6-b955-4c142005dfa8" />

