import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time

placa = Arduino ('COM3')
it = util.Iterator(placa)
it.start()
time.sleep(0.5)

cont1 = 0
cont2 = 0
cont3 = 0

sizex_circ = 40
sizey_circ = 40

xcenter = 500

a_0 = placa.get_pin('a:0:i')
a_1 = placa.get_pin('a:1:i')
a_2 = placa.get_pin('a:2:i')

pin_led4 = placa.get_pin('d:10:o')
pin_led5 = placa.get_pin('d:9:o')
pin_led6 = placa.get_pin('d:8:o')

ventana = Tk()
ventana.geometry('1280x800')
ventana.title("Quiz")

# Fetch the service account key JSON file contents
cred = credentials.Certificate('key/key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testdatabase-c031c.firebaseio.com/'
})


marco1 = Frame(ventana, bg="gray", highlightthickness=1, width=1280, height=800, bd= 5)
marco1.place(x = 0,y = 0)

img = Image.open("logo.jpg")
img = img.resize((150,150))
photoImg=  ImageTk.PhotoImage(img)
b=Label(marco1,text="")
b.configure(image=photoImg)
b.place(x = 1060,y = 20)

alerta = Label(marco1, text="Sergio Andres Rodriguez Perez",bg='white', font=("Arial Bold", 30), fg="black")
alerta.place(x=300, y = 20)

draw = Canvas(marco1, width=300, height=300,bg='gray')
draw.place(x = 500,y = 500)

alerta = Label(marco1, text="",bg='red', font=("Arial Bold", 30), fg="black")
alerta.place(x=600, y = 400)


led1_draw=draw.create_oval(10,10,10+sizex_circ,10+sizey_circ,fill="white")
led2_draw=draw.create_oval(120,10,120+sizex_circ,10+sizey_circ,fill="white") 
led3_draw=draw.create_oval(250,10,250+sizex_circ,10+sizey_circ,fill="white")


def update_label():
    global cont1,cont2,cont3
    global a_0,a_1,a_2
    global alerta
    global pin_led6, pin_led5, pin_led4

    cont = a_0.read()
    cont1 = a_0.read()

    cont_indicador.config(text = str(cont1))

    ref = db.reference("sensores")
    ref.update({
        'adc1': cont
    }) 

    if(cont1 > 0.5):
        draw.itemconfig(led1_draw, fill = 'yellow')
        pin_led4.write(1)
    else:
        draw.itemconfig(led1_draw, fill = 'white')
        pin_led4.write(0)


    cont = a_1.read()
    cont2 = a_1.read()
    cont_indicador1.config(text = str(cont2))

    cont = a_1.read()
    ref.update({
        'adc2': cont
    })

    if(cont2 > 0.5):
        draw.itemconfig(led2_draw, fill = 'yellow')
        pin_led5.write(1)
    else:
        draw.itemconfig(led2_draw, fill = 'white')
        ppin_led5.write(0)

    cont = a_2.read()
    cont3 = a_2.read()
    cont_indicador2.config(text = str(cont3))

    ref.update({
        'adc3' : cont
    })

    if(cont3 > 0.5):
        draw.itemconfig(led3_draw, fill = 'yellow')
        pin_led6.write(1)
    else:
        draw.itemconfig(led3_draw, fill = 'white')
        pin_led6.write(0)

    ventana.after(5000,update_label)

    if(cont1 > 0.5 or cont2 > 0.5 or cont3 > 0.5):
        alerta.config(text = "Alerta")
        ref.update({
            'Alerta' : "Alerta"
        })
    else:
        alerta.place_forget()



cont_indicador= Label(marco1, text=str(cont1),bg='cadet blue1', font=("Arial Bold", 15), fg="white")
cont_indicador.place(x=20 + xcenter, y=90)

aviso_adc1 =Label(marco1, text="ADC1",bg='cadet blue1', font=("Arial Bold", 15), fg="white")
aviso_adc1.place(x =0 + xcenter,y=130)

cont_indicador1= Label(marco1, text=str(cont2),bg='cadet blue1', font=("Arial Bold", 15), fg="white")
cont_indicador1.place(x=120 + xcenter, y=90)

aviso_adc2 =Label(marco1, text="ADC2",bg='cadet blue1', font=("Arial Bold", 15), fg="white")
aviso_adc2.place(x = 100 + xcenter,y=130)

cont_indicador2= Label(marco1, text=str(cont3),bg='cadet blue1', font=("Arial Bold", 15), fg="white")
cont_indicador2.place(x=220 + xcenter, y=90)

aviso_adc3 =Label(marco1, text="ADC3",bg='cadet blue1', font=("Arial Bold", 15), fg="white")
aviso_adc3.place(x = 200 + xcenter,y=130)

update_label()

ventana.mainloop()