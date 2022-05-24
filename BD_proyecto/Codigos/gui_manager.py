import mysql.connector
import pandas as pd
import time
import datetime as datetime
import tkinter as tk
#FUNCTIONS
def toggle():
    t,st='REGISTRO','BIOMETRICO'
    if(reg_bio.config('text')[-1]=='REGISTRO'):t,st='EMPLEADOS','INGRESO'
    else:None
    label2.configure(text=st)
    reg_bio.configure(text=t)
def chart_change(choice):
    today=datetime.datetime.today().replace(minute=0, hour=0, second=0, microsecond=0)
    if choice=='Ingreso Diario':
        end=today+datetime.timedelta(hours=24)
        print(today,end)
    elif choice=='Ingreso Semanal':
        start=today-datetime.timedelta(days=7)
        print(start,today)
    elif choice=='Ingreso Mensual':
        start=today-datetime.timedelta(days=30)
        print(start,today)
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
label2=tk.Label(root,text='INGRESOS',font=('Ubuntu',14),background=bkc)
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
reg_bio=tk.Button(text='EMPLEADOS',width=10,command=toggle,pady=10)
reg_bio.place(x=6*dx+w/2,y=3*dy)
#MAIN LOOP
root.mainloop()

