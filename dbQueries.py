import psycopg2

conn = psycopg2.connect("dbname=SupplyChain user=postgres password=tiger")
cur = conn.cursor()

def addBatch(batch_id,timestamp,hash):
    sql='''INSERT into "PartsBatch" values(%s,%s,%s);'''
    cur.execute(sql,(batch_id,timestamp,hash))
    conn.commit()

def addProduct(batch_id,product_id,timestamp,hash):
    
    sql='''INSERT into "Product" values(%s,%s,%s,NULL,NULL,NULL,NULL,NULL,%s);'''
    cur.execute(sql,(product_id,timestamp,hash,batch_id,))
    conn.commit()

def addQC(product_id,timestamp,hash,officer_name,message,grade):
    sql='''UPDATE "Product" set "qc_timestamp"=%s,"qc_hash"=%s, "qc_officer"=%s,"qc_message"=%s,"qc_grade"=%s where product_id=%s'''
    cur.execute(sql,(timestamp,hash,officer_name,message,grade,product_id,))
    
    conn.commit()

def fetchProduct(product_id):
    sql='''SELECT * from "Product" where "product_id"=%s'''
    cur.execute(sql,(product_id,))
    result=cur.fetchone()
    return result 

