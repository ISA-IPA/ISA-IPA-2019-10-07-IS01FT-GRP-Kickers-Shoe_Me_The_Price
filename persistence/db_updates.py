import pandas as pd
import psycopg2.extras as ex
import time


def push_to_shoe_request(conn, details):
    date_today = time.ctime()

    cur = conn.cursor()
    
    email = details['email']
    shoes = details['shoes']
    size = details['size']
    updates = details['updates']
    gender = details['gender']
    
    if updates == True:
        updates = 'Daily'
        status = "Active"
    '''else:
        updates = "Once"'''
    
    if gender == "Male":
        gender = 'M'
    else:
        gender = 'F'
        
    
    
    sql_query = "INSERT INTO subscriber (subscriber_id , shoe_names , shoe_size ,gender ,frequency, request_date, subscription_status ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    cur.execute(sql_query, (email,shoes, size, gender, updates, date_today, status))
    
    conn.commit()
    

def get_customer_data(conn):
    
    sql = "select * from subscriber where frequency = 'Daily';"

    data = pd.read_sql_query(sql, conn)
    
    return data




def get_price_data(conn):
    
    sql = "select * from prices;"
    
    data = pd.read_sql_query(sql, conn)
    
    return data



def push_price_data(conn,shoename, website, price):
    date_today = time.ctime()

    cur = conn.cursor()

    sql_query = "INSERT INTO shoe_price_hist (shoename,website,date,price) VALUES (%s, %s, %s, %s)"
    
    cur.execute(sql_query, (shoename,website,date_today,price))
    
    conn.commit()


def push_df_to_subscriberDB(connection,df):
    table = 'subscriber'
    if len(df) > 0:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)
        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
        # create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)
        
        cur = connection.cursor()
        ex.execute_batch(cur, insert_stmt, df.values)
        connection.commit()
        cur.close()
        