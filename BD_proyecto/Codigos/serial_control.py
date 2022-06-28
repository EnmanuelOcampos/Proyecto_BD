import serial
import time
import mysql.connector
try:
    string_auto="INSERT INTO Registro (id_auto,timestamp,monto) VALUES ({},{},{})"
    string_biom="INSERT INTO Biometrico (id_empleado,timestamp) VALUES ({},{})"
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= "sistema_peaje" )
    cursor1=conexion1.cursor()
    ser=serial.Serial(port='/dev/ttyUSB0',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
    while True:
        if ser.inWaiting():
            ct=str(int(time.time()))
            res=ser.readline(ser.in_waiting).decode('utf-8').replace('\n','').replace('\r','').split(',')
            ser.reset_input_buffer()
            if res[0]=="empleado":
                try:
                    cursor1.execute("SELECT id,nombre,apellido FROM Empleado WHERE tarjeta='"+res[1]+"'")
                    ret=[i for i in cursor1.fetchall()[0]]
                    cursor1.execute(string_biom.format(ret[0],ct))
                    conexion1.commit()
                    print(ret[1]+' '+ret[2]+' hora de llegada '+ct)
                except:print('Usuario no registrado...')
            elif res[0]=="automovil":
                try:
                    cursor1.execute("SELECT id,id_chofer,chapa FROM Automovil WHERE tarjeta='"+res[1]+"'")
                    ret=[i for i in cursor1.fetchall()[0]]
                    cursor1.execute("SELECT saldo FROM Chofer WHERE id="+str(ret[1]))
                    saldo=cursor1.fetchall()[0][0]
                    if saldo>0:
                        cursor1.execute("UPDATE Chofer SET saldo=saldo-5000 WHERE id="+str(ret[1]))
                        conexion1.commit()
                        cursor1.execute(string_auto.format(ret[0],ct,'5000'))
                        conexion1.commit()
                        cursor1.execute("SELECT nombre,apellido,saldo FROM Chofer WHERE id='"+str(ret[1])+"'")
                        ret=[i for i in cursor1.fetchall()[0]]
                        print('Chofer '+ret[0]+' '+ret[1]+' hora de cruce '+ct+' saldo actual: '+str(ret[2]))
                    else:print('Saldo insuficiente...')
                except:
                    print('Automovil no registrado...')
            time.sleep(2)
        time.sleep(0.1)
except Exception as e:print(e)
try:
    ser.close()
    conexion1.close()
except:None
