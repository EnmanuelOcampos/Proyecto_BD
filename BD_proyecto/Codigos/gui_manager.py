import mysql.connector
import pandas as pd
import time
import datetime as datetime
import tkinter as tk
from tkinter import ttk
global dsd,hst,header,result
dsd=datetime.datetime.today().replace(minute=0, hour=0, second=0, microsecond=0)
hst=dsd+datetime.timedelta(hours=24)
dsd,hst=str(dsd),str(hst)
header=('id','Nombre','Apellido','CIN','Puesto','Tarjeta','timestamp')
#FUNCTIONS
def data_get(**kw):
    table=kw.get('table',None)
    var=kw.get('var',None)
    desde=kw.get('desde',None)
    hasta=kw.get('hasta',None)
    desde=int(datetime.datetime.strptime(desde,"%Y-%m-%d %H:%M:%S").timestamp())
    hasta=int(datetime.datetime.strptime(hasta,"%Y-%m-%d %H:%M:%S").timestamp())
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= "sistema_peaje" )
    cursor1=conexion1.cursor() 
    df=pd.DataFrame(columns=var)
    for item in var:
        try:
            cursor1.execute("SELECT "+item+" FROM "+table+" WHERE timestamp>= "+str(desde)+" AND timestamp< "+str(hasta)+" ORDER BY timestamp ASC")
            df[item]=[i[0] for i in cursor1.fetchall()]
        except Exception as e:print(e)
    conexion1.close()
    return df
def toggle():
    global dsd,hst,header,result
    for i in result.get_children():result.delete(i)
    table,related,var,var2,t,st,header='Biometrico','Empleado',['id','id_empleado','timestamp'],'nombre,apellido,CIN,puesto,tarjeta','HISTORIAL','BIOMETRICO',('id','Nombre','Apellido','CIN','Puesto','Tarjeta','timestamp')
    if(reg_bio.config('text')[-1]=='HISTORIAL'):table,related,var,var2,t,st,header='Registro','Automovil',['id','id_auto','timestamp'],'id_chofer,tipo,chapa,marca,tarjeta','BIOMETRICO','HISTORIAL',('id','Chofer','Tipo','Chapa','Marca','Tarjeta','timestamp')
    else:None
    label2.configure(text=st)
    reg_bio.configure(text=t)
    refresh(table,related,var,var2,header)
def refresh(table,related,var,var2,header):
    df=data_get(table=table,desde=dsd,hasta=hst,var=var)
    id_df=df[var[0]].to_list()
    id_list=df[var[1]].to_list()
    time_list=df[var[2]].to_list()
    conexion1=mysql.connector.connect(host="localhost", user="root", passwd="password", database= "sistema_peaje" )
    cursor1=conexion1.cursor()
    data=[]
    for k in range(len(header)):result.heading(str(k),text=header[k])
    for i in range(0,len(id_list)):
        cursor1.execute("SELECT "+var2+" FROM "+related+" WHERE id="+str(id_list[i]))
        data.append((id_df[i],)+cursor1.fetchall()[0]+(time_list[i],))
    for d in data:result.insert('',tk.END,values=d)
    conexion1.close()
def update():
    global dsd,hst,header,result
    for i in result.get_children():result.delete(i)
    table,related,var,var2,header='Biometrico','Empleado',['id','id_empleado','timestamp'],'nombre,apellido,CIN,puesto,tarjeta',('id','Nombre','Apellido','CIN','Puesto','Tarjeta','timestamp')
    if(reg_bio.config('text')[-1]=='BIOMETRICO'):table,related,var,var2,header='Registro','Automovil',['id','id_auto','timestamp'],'id_chofer,tipo,chapa,marca,tarjeta',('id','Chofer','Tipo','Chapa','Marca','Tarjeta','timestamp')
    else:None
    refresh(table,related,var,var2,header)
def chart_change(choice):
    global dsd,hst
    today=datetime.datetime.today().replace(minute=0, hour=0, second=0, microsecond=0)
    if choice=='Ingreso Diario':
        dsd=today
        hst=today+datetime.timedelta(hours=24)
    elif choice=='Ingreso Semanal':
        dsd=today-datetime.timedelta(days=7)
        hst=today+datetime.timedelta(hours=24)
    elif choice=='Ingreso Mensual':
        dsd=today-datetime.timedelta(days=30)
        hst=today+datetime.timedelta(hours=24)
    dsd,hst=str(dsd),str(hst)
#GRAPHIC VARIABLES
w,h=1000,750
bkc='white'
dx,dy=50,50
#ROOT SCREEN CANVAS
root=tk.Tk()
root.title('Muon Matrix control panel')
canvas=tk.Canvas(root,width=w,height=h,relief='raised')
canvas.configure(background=bkc)
canvas.pack()
#GEOMETRIC FIGURES
canvas.create_rectangle(dx,2*dy+10,200+w/2,h-dy)
#LABELS
label1=tk.Label(root,text='PUESTO DE PEAJE RFID',font=('Ubuntu',20),background=bkc)
label2=tk.Label(root,text='HISTORIAL',font=('Ubuntu',14),background=bkc)
label3=tk.Label(root,text='OPCIONES',font=('Ubuntu',14),background=bkc)
canvas.create_window(w/2,dy,window=label1)
canvas.create_window(w/4+100,2*dy,window=label2)
canvas.create_window(3*dx+w/2+200,2*dy,window=label3)
#DROPDOWN BARS
options=["Ingreso Diario","Ingreso Semanal","Ingreso Mensual"]
var=tk.StringVar(root);var.set("Ingreso Diario")
bar_selec=tk.OptionMenu(root,var,*options,command=chart_change)
canvas.create_window(7*dx+w/2,5*dy,window=bar_selec)
#BUTTONS
reg_bio=tk.Button(text='BIOMETRICO',width=10,command=toggle,pady=10)
ref_but=tk.Button(text='REFRESH TABLE',width=10,command=update,pady=10)
reg_bio.place(x=6*dx+w/2,y=3*dy)
ref_but.place(x=6*dx+w/2,y=6*dy)
#TREEVIEW
result=ttk.Treeview(root,columns=('0','1','2','3','4','5','6'),show='headings',height=27)
for k in range(0,len(header)):
    result.heading(str(k),text=header[k])
    result.column(str(k),minwidth=0,width=90,stretch='no')
canvas.create_window(7.5*dx,8*dy,window=result)
#MAIN LOOP
root.mainloop()

