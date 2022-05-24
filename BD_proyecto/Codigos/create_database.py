import mysql.connector
def create_database(**kw):
    db_name=kw.get('db_name',None) 
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= "" )
    cursor1=conexion1.cursor()
    line="CREATE DATABASE "+db_name
    try:
    	cursor1.execute(line)
    	conexion1.commit()
    	print("The database was created successfully...")
    except Exception as e: print(e)
    conexion1.close()
def create_table(**kw):
    table,var,db_name,line=kw.get('table',None),kw.get('var',[]),kw.get('db_name',None),""
    for a in var: line+=", "+a
    line="CREATE TABLE "+table+" (id INT AUTO_INCREMENT PRIMARY KEY"+line+");"
    print(line)
    conexion1=mysql.connector.connect(host="localhost",user="root",passwd="password",database=db_name)
    cursor1=conexion1.cursor()	
    try:	
        cursor1.execute(line)    
        conexion1.commit()
        print("The SQL table was created successfully...")
    except Exception as e: print(e)
    conexion1.close()
def create_relation(**kw):
    table1,table2,key1,key2,name,db_name=kw.get('table1',None),kw.get('table2',None),kw.get('key1',None),kw.get('key2',None),kw.get('name',None),kw.get('db_name',None)
    line='ALTER TABLE '+table1+' ADD CONSTRAINT '+name+' FOREIGN KEY ('+key1+') REFERENCES '+table2+'('+key2+') ON DELETE CASCADE ON UPDATE CASCADE;'
    print(line)
    try:
        conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database=db_name )
        cursor1=conexion1.cursor()
        cursor1.execute(line)
        conexion1.commit()
        print('The SQL relation was added successfully...')
    except Exception as e:print(e)
    conexion1.close()
create_database(db_name='sistema_peaje')
create_table(table='Biometrico',var=['id_empleado INT','timestamp BIGINT'],db_name='sistema_peaje')
create_table(table='Empleado',var=['nombre VARCHAR(4)','apellido VARCHAR(4)','CIN BIGINT','puesto VARCHAR(4)'],db_name='sistema_peaje')
create_table(table='Automovil',var=['id_chofer INT','tipo VARCHAR(4)','chapa VARCHAR(4)','marca VARCHAR(4)'],db_name='sistema_peaje')
create_table(table='Registro',var=['id_auto INT','timestamp BIGINT','monto BIGINT'],db_name='sistema_peaje')
create_table(table='Chofer',var=['nombre VARCHAR(4)','apellido VARCHAR(4)','CIN BIGINT','saldo BIGINT'],db_name='sistema_peaje')
create_relation(table1='Registro',table2='Automovil',key1='id_auto',key2='id',db_name='sistema_peaje',name='registros')
create_relation(table1='Automovil',table2='Chofer',key1='id_chofer',key2='id',db_name='sistema_peaje',name='dueño')
create_relation(table1='Biometrico',table2='Empleado',key1='id_empleado',key2='id',db_name='sistema_peaje',name='firma')
