import psycopg2
import exptoexl

def createtable(conn):
    cur1 = conn.cursor()
    cr_q = """
    create table mobile( id int not null, model text not null, price real);
    """
    cur1.execute(cr_q)
    conn.commit()
    print(" table created")
def insersomedata(conn):
    cur1 = conn.cursor()
    ins_q = "insert into mobile (id,model,price) values(%s,%s,%s)"
    try:
        cur1.execute(ins_q,(1,"IPhone 4s",450))
        cur1.execute(ins_q,(2,"Sotel 1000",460))
        cur1.execute(ins_q,(3,"Aurora 12",750))
        cur1.execute(ins_q,(4,"Nokia 345",190))
        cur1.execute(ins_q,(5,"Motorola D23",950))
        cur1.execute(ins_q,(6,"Xenium 4",670))
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        conn.commit()
        cur1.close()
##### Begin
try:
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect("postgres://postgres:postgrespw@localhost:49153")
    cur = conn.cursor()

	# execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
    print("Select executed successfully!... ") 
	# close the communication with the PostgreSQL
    
    #createtable(conn)
    #insersomedata(conn)
    cur.execute("SELECT * from mobile")
    r = cur.fetchall()
    print("Result ", r)
    for a in r:
       print(" Id : %s ,  Model :  %s , Price : %s "%(a[0],a[1],a[2]))
    colnames = [desc[0] for desc in cur.description]
    exptoexl.make_xls(colnames,r)
    print("   Columns: \n")
    print(colnames)
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


    
