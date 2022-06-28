import mysql.connector
import pandas as pd
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
def create_database(**kw):
    db_name=kw.get('db_name',None) 
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= "" )
    cursor1=conexion1.cursor()
    line="CREATE DATABASE "+db_name
    try:
        print(line)
        cursor1.execute(line)
        conexion1.commit()
        print("The database was created successfully...")
    except Exception as e: None
    conexion1.close()
def create_table(**kw):
    table,var,db_name,line=kw.get('table',None),kw.get('var',[]),kw.get('db_name',None),""
    for a in var: line+=", "+a
    line="CREATE TABLE "+table+" (id INT AUTO_INCREMENT PRIMARY KEY"+line+");"
    conexion1=mysql.connector.connect(host="localhost",user="root",passwd="password",database=db_name)
    cursor1=conexion1.cursor()	
    try:	
        print(line)
        cursor1.execute(line)    
        conexion1.commit()
        print("The SQL table was created successfully...")
    except Exception as e: None
    conexion1.close()
def create_relation(**kw):
    table1,table2,key1,key2,name,db_name=kw.get('table1',None),kw.get('table2',None),kw.get('key1',None),kw.get('key2',None),kw.get('name',None),kw.get('db_name',None)
    line='ALTER TABLE '+table1+' ADD CONSTRAINT '+name+' FOREIGN KEY ('+key1+') REFERENCES '+table2+'('+key2+') ON DELETE CASCADE ON UPDATE CASCADE;'
    try:
        print(line)
        conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database=db_name )
        cursor1=conexion1.cursor()
        cursor1.execute(line)
        conexion1.commit()
        print('The SQL relation was added successfully...')
    except Exception as e:None
    conexion1.close()
def csv_to_sql(**kw):
    path=kw.get('path',None)
    table=kw.get('table',None)
    df=pd.read_csv(path);print(df.head());
    var=df.columns.to_list()
    string="INSERT INTO "+table+" "+str(tuple(var)).replace("'","")+" VALUES "+"("+"{},"*(len(var)-1)+"{})"
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= "sistema_peaje" )
    cursor1=conexion1.cursor()
    l=len(df.index)
    dat,q='',0
    for v in var:
        exec('c'+str(q)+'=df["'+v+'"].to_list()')
        dat+=',c'+str(q)+'[k]';q+=1
    dat=dat[1:]
    print(df);print('Loading data...\n')
    printProgressBar(0,l,prefix='Progress:',suffix='Complete',length=50)
    for k in range(0,l):
        try:
            cursor1.execute(eval('string.format('+dat+')'))
            conexion1.commit()
        except Exception as e: print(e)
        printProgressBar(k+1,l,prefix='Progress:',suffix='Complete',length = 50)
    conexion1.close()
def drop_database(**kw):
    db_name=kw.get('db_name',None) 
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= db_name )
    cursor1=conexion1.cursor()
    line='DROP DATABASE '+db_name
    try:
        print(line)
        cursor1.execute(line)
        conexion1.commit()
        print('The database was dropped successfully...')
    except Exception as e:print(e)
    conexion1.close()
drop_database(db_name='sistema_peaje')
create_database(db_name='sistema_peaje')
create_table(table='Biometrico',var=['id_empleado INT','timestamp BIGINT'],db_name='sistema_peaje')
create_table(table='Empleado',var=['nombre VARCHAR(10)','apellido VARCHAR(10)','CIN BIGINT','puesto VARCHAR(10)','tarjeta VARCHAR(8)'],db_name='sistema_peaje')
create_table(table='Automovil',var=['id_chofer INT','tipo VARCHAR(10)','chapa VARCHAR(10)','marca VARCHAR(10)','tarjeta VARCHAR(8)'],db_name='sistema_peaje')
create_table(table='Registro',var=['id_auto INT','timestamp BIGINT','monto BIGINT'],db_name='sistema_peaje')
create_table(table='Chofer',var=['nombre VARCHAR(10)','apellido VARCHAR(10)','CIN BIGINT','saldo BIGINT'],db_name='sistema_peaje')
create_relation(table1='Registro',table2='Automovil',key1='id_auto',key2='id',db_name='sistema_peaje',name='registros')
create_relation(table1='Automovil',table2='Chofer',key1='id_chofer',key2='id',db_name='sistema_peaje',name='dueño')
create_relation(table1='Biometrico',table2='Empleado',key1='id_empleado',key2='id',db_name='sistema_peaje',name='firma')
csv_to_sql(path='/home/lucas/FIUNA/9no_semestre/BD/Proyecto/Codigos/datasets/choferes.csv',table='Chofer')
csv_to_sql(path='/home/lucas/FIUNA/9no_semestre/BD/Proyecto/Codigos/datasets/autos.csv',table='Automovil')
csv_to_sql(path='/home/lucas/FIUNA/9no_semestre/BD/Proyecto/Codigos/datasets/empleados.csv',table='Empleado')
