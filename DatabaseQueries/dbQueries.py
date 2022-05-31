import psycopg2

conn = psycopg2.connect("dbname=SupplyChain user=postgres password=tiger")
cur = conn.cursor()

def addBatch(batch_id,timestamp,hash):
    sql='''INSERT into "PartsBatch" values(%s,%s,%s);'''
    cur.execute(sql,(batch_id,timestamp,hash))
    conn.commit()

def getPreviousProduct():
    sql='''SELECT max("product_id") from "Product"'''
    cur.execute(sql,())
    result=cur.fetchone()
    return result[0] 

def addProduct(batch_id,product_id,timestamp,hash):
    sql='''INSERT into "Product" values(%s,%s,%s,NULL,NULL,NULL,NULL,NULL,%s,NULL,NULL,NULL);'''
    cur.execute(sql,(product_id,timestamp,hash,batch_id,))
    conn.commit()
#addProduct(1001,100101,"","0x00")
def addQC(product_id,timestamp,hash,message,grade):
    sql='''UPDATE "Product" set "qc_timestamp"=%s,"qc_hash"=%s,"qc_message"=%s,"qc_grade"=%s where "product_id"=%s'''
    cur.execute(sql,(timestamp,hash,message,grade,product_id,))
    conn.commit()

def fetchProduct(product_id):
    sql='''SELECT * from "Product" where "product_id"=%s'''
    cur.execute(sql,(product_id,))
    result=cur.fetchone()
    return result 

def getQualityQueue():
    sql='''SELECT "product_id" from "qualitycontrol" where "quality_status"=0'''
    cur.execute(sql,())
    result=cur.fetchall()
    return result

def addToQualityQueue(product_id,timestamp):
    sql='''INSERT into "qualitycontrol" values(%s,0,%s,NULL,NULL)'''
    cur.execute(sql,(product_id,timestamp,))
    conn.commit()

def updateQualityQueue(product_id,timestamp,grade):
    sql='''UPDATE "qualitycontrol" set "quality_status"=1,"check_timestamp"=%s,"grade"=%s where "product_id"=%s '''
    cur.execute(sql,(timestamp,grade,product_id))
    conn.commit()
def addQC(product_id,timestamp,hash,message,grade):
    sql='''UPDATE "Product" set "qc_timestamp"=%s,"qc_hash"=%s,"qc_message"=%s,"qc_grade"=%s where "product_id"=%s'''
    cur.execute(sql,(timestamp,hash,message,grade,product_id,))
    conn.commit()

def getStock(retailer):
    sql='''SELECT "product_id" from "Product" where "retailer"=%s'''
    cur.execute(sql,(retailer,))
    result=cur.fetchall()
    return result 

def getPrevOrder():
    sql='''SELECT max("order_id") from "order"'''
    cur.execute(sql,())
    result = cur.fetchone()
    return result[0]
#print(type(getPrevOrder()))
def addOrder(order_id,retailer,qty,timestamp,tx):
    sql='''INSERT into "order" values(%s,%s,%s,NULL,0,%s,%s)'''
    cur.execute(sql,(order_id,retailer,qty,timestamp,tx))
    conn.commit()

def getCheckedUnits():
    sql='''SELECT * from "Product" where "qc_grade"=1 and "retailer" IS NULL'''
    cur.execute(sql,())
    return cur.fetchall()

