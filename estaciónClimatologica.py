"""[summary]
 @Autor: Tomás Rodríguez Garrido
 @Fecha: 05-08-2021
 @Version: 1.0
 
 Intento de crear una estación metereológica usando una API externa desde https://openweathermap.org pass: Obelix01
 API key is b4384d42621600f8f67346e83c11878a
 
 Llamada a la API: (por nombre de ciudad, tiene más de 200.000 localizaciones está api, se puede hacer tambien por ID 
 y por localización pero vamos a lo facil en esta primera versión)
 
 api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key} 
  
 Parameters
 q	required	City name, state code and country code divided by comma, Please, refer to ISO 3166 for the state codes or country codes.
 You can specify the parameter not only in English. In this case, the API response should be returned in the same language as the language
 of requested location name if the location is in our predefined list of more than 200,000 locations.

 appid	required	Your unique API key (you can always find it on your account page under the "API key" tab)
 mode	optional	Response format. Possible values are xml and html. If you don't use the mode parameter format is JSON by default. Learn more
 units	optional	Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, 
                    standard units will be applied by default. Learn more
 lang	optional	You can use this parameter to get the output in your language. Learn more   

"""

import sys, os
import time
from datetime import date, datetime
from tkinter import (Button, Entry, Frame, Label, LabelFrame, PhotoImage, Tk,
                     TkVersion)
from tkinter.constants import CENTER, LEFT, RIGHT
from tkinter.font import BOLD
from typing import Text

import requests  # pip install requests
from PIL import Image, ImageTk  # pip install Pillow


class Estacion(Frame):
    def __init__(self, master, *args):
        super().__init__(master, *args)
        
        self.tiempo = { '01d': 'sol.png', '01n': 'sol.png', '02d': 'nublado_sol.png',
               '02n': 'nublado_sol.png', '03d': 'nublado.png', '03n': 'nublado.png',
               '04d': 'nublado.png', '04n': 'nublado.png',    
               '09d': 'lluvia2.png', '09n': 'lluvia2.png',
               '10d': 'lluvia2.png', '10n': 'lluvia2.png',      
               '11d': 'tormenta.png', '11n': 'tormenta.png',
               '13d': 'nieve.png', '13n': 'nieve.png',
               '50d': 'viento2.png', '50n': 'viento2.png', 
               }
        self.img_Tiempo = ''  #esto me guardará la ruta del archivo de mi imagen del tiempo
        self.paso = False  #señal para saber si ya consulte o no el tiempo
        self.label =''  #para guardar mi objeto label de la imagen
        self.timezon = 0  #para guardar la zona horaria
        
        
        self.click = True  #señal para saber si presione el boton de buscar
        
        #con esto hacemos que la interfaz sea responsive y cambie de tamaño al gusto        
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)        
        self.master.columnconfigure(2, weight = 1)
        
        self.master.rowconfigure(1, weight = 1)
        self.master.rowconfigure(2, weight = 1)
        self.master.rowconfigure(3, weight = 1) #añado una tercera fila
        self.master.rowconfigure(4, weight = 1)
        
        #cuadro superior donde pongo la ciudad y el boton buscar
        self.frame = Frame(self.master, bg = 'grey', highlightbackground= 'ivory', highlightthickness= 2)
        self.frame.grid(columnspan=3, row= 0, sticky= 'nsew', padx= 5, pady= 5)
        
        #Los 2 cuadrados donde mostrare el icono del tiempo, la descripción del tiempo y la temperatura que se siente o real sense temperature
        self.frame9 = Frame(self.master, bg = '#a1cda8', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame9.grid(columnspan=2, row= 1, sticky= 'nsew', padx= 5, pady= 5)
        self.frame10 = Frame(self.master, bg = '#a1cda8', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame10.grid(column=2, row= 1, sticky= 'nsew', padx= 5, pady= 5)        
        
        #Los 6 cuadrados donde mostrare la información de la temperatura, etc... 
        self.frame2 = Frame(self.master, bg = '#b5dfca', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame2.grid(column=0, row= 2, sticky= 'nsew', padx= 5, pady= 5)
        self.frame3 = Frame(self.master, bg = '#b5dfca', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame3.grid(column=1, row= 2, sticky= 'nsew', padx= 5, pady= 5)
        self.frame4 = Frame(self.master, bg = '#b5dfca', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame4.grid(column=2, row= 2, sticky= 'nsew', padx= 5, pady= 5)        
        self.frame5 = Frame(self.master, bg = '#b5dfca', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame5.grid(column=0, row= 3, sticky= 'nsew', padx= 5, pady= 5)
        self.frame6 = Frame(self.master, bg = '#b5dfca', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame6.grid(column=1, row= 3, sticky= 'nsew', padx= 5, pady= 5)
        self.frame7 = Frame(self.master, bg = '#b5dfca', highlightbackground= 'dark violet', highlightthickness= 2)
        self.frame7.grid(column=2, row= 3, sticky= 'nsew', padx= 5, pady= 5)
        
        #cuadro inferior
        self.frame8 = Frame(self.master, bg = '#c5e7e2', highlightbackground= 'ivory', highlightthickness= 2)
        self.frame8.grid(columnspan=3, row= 4, sticky= 'nsew', padx= 5, pady= 5)
        
        self.widgets()
        
    def animacion(self): 
        self.frame.config(highlightbackground='ivory')       #el contorno de cada frame cambia a ivory
        self.frame2.config(highlightbackground='ivory')
        self.frame3.config(highlightbackground='ivory')
        self.frame4.config(highlightbackground='ivory') 
        self.frame5.config(highlightbackground='ivory') 
        self.frame6.config(highlightbackground='ivory') 
        self.frame7.config(highlightbackground='ivory') 
        self.frame8.config(highlightbackground='ivory')
        self.frame9.config(highlightbackground='ivory')
        self.frame10.config(highlightbackground='ivory')
        
        self.obtener_tiempo()
        
        gif = Image.open("Estacion Climatologica/images/buscar.gif")     #carga la imagen
        frames = gif.n_frames
        
        #**************************************************************************************************************************
        # Esto me cambia la imagen del tiempo actual, y para colocarlo uso place en vez de pack, asi se me queda centrado.
        
        self.img_Tiempo2 = PhotoImage(file = "Estacion Climatologica/images/" + self.img_Tiempo)         
                        
        if self.paso == False:            
            self.imagenTiempo = Label(self.frame9, image= self.img_Tiempo2, bg='#a1cda8').place(relx=0.25, rely=0.25, anchor='ne')
            self.paso = True
        else:
            #imagenTiempo.pack_forget(self)            
            self.imagenTiempo = Label(self.frame9, image= self.img_Tiempo2, bg='#a1cda8').place(relx=0.25, rely=0.25, anchor='ne')
              
        #**************************************************************************************************************************
        
        if self.click == True: 
            for i in range(1, frames):
                self.inicio = PhotoImage(file= "Estacion Climatologica/images/buscar.gif", format='gif -index %i' %(i)) 
                self.bt_inicio['image'] = self.inicio
                time.sleep(0.04)
                self.master.update()
                self.click = False
                if i + 1 == frames:
                    self.click = True
    
    def obtener_tiempo(self):
        localidad = self.ingresa_ciudad.get()
        # API key is b4384d42621600f8f67346e83c11878a
        # API = api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key} 
        time.sleep(0.04)
        self.ingresa_ciudad.delete(0, 'end') #sirve para borrar una vez ingresada la ciudad el texto de localidad
        
        #Llamamos a la API del clima        
        API = 'https://api.openweathermap.org/data/2.5/weather?q=' + localidad + '&appid=b4384d42621600f8f67346e83c11878a' + '&lang=es'
        
        try: 
            json_datos = requests.get(API).json()                                     #Leemos los datos y por si da error lo metemos en try-catch
            self.temp['text'] = str(int(json_datos['main']['temp']- 273.15)) + " °C"
            self.temp_min['text'] = str(int(json_datos['main']['temp_min'] - 273.15)) + " °C"
            self.temp_max['text'] = str(int(json_datos['main']['temp_max'] - 273.15)) + " °C"
            self.temp_real['text'] = str(int(json_datos['main']['feels_like'] -273.12)) + " °C"
            self.presion['text'] = str(json_datos['main']['pressure']) + ' hPa' 
            self.humedad['text'] = str(json_datos['main']['humidity']) + ' %'
            self.viento['text'] = str(int(json_datos['wind']['speed'])*18/5) + ' km/h'
            self.localidad['text'] =  json_datos['name'] + ' - '+ json_datos['sys']['country'] 
            
            self.timezon = int(json_datos['timezone'])
            print(self.timezon)
            
            
            self.clongitud['text'] = 'Long: ' + str(json_datos['coord']['lon'])
            self.clatitud['text'] = 'Lat: ' + str(json_datos['coord']['lat'])   
            
            d1 = json_datos['weather'] #esto me da una lista de 1 elemento que es un diccionario
            elTiempo = ''
            elIcono = ''
            
            for elem in d1:
                for k, v in elem.items():
                    if k == 'description':
                        elTiempo = v
                    if k == 'icon':
                        elIcono = v
                        
            self.descripcion['text'] = elTiempo
            
            ruta =''
            for k, v in self.tiempo.items():
                if k == elIcono:
                    ruta = v
        
            self.img_Tiempo = ruta
            print(self.img_Tiempo)            
            
            ts = int(json_datos['sys']['sunrise'])
            ts2 = int(json_datos['sys']['sunset'])            
            self.amanecer['text'] = 'Amanece: ' + str(datetime.fromtimestamp(ts).strftime('%H:%M:%S'))
            self.anochecer['text'] = 'Anochece: ' + str(datetime.fromtimestamp(ts2).strftime('%H:%M:%S'))  
            '''
            Diferencias entre: Si uso el segundo tendria que añadir utc + 1 en invierno y utc + 2 en verano
               fromtimestamp, give you the date and time in local time
               utcfromtimestamp, gives you the date and time in UTC.            
            '''
                                    
            print(json_datos)
        except:
            self.aviso['text'] =  'Error,no encontrada!'
            self.temp['text'] = '-'
            self.temp_min['text'] = '-'
            self.temp_max['text'] = '-'
            self.temp_real['text'] = '-'
            self.presion['text'] = '-'
            self.humedad['text'] = '-'
            self.viento['text'] = '-'
            
            self.img_Tiempo = ''
                                  
            self.clongitud['text'] = ''
            self.clatitud['text'] = ''
            #self.icon['text'] = ''
            self.descripcion['text'] = ''
            self.amanecer['text'] = ''
            self.anochecer['text'] = ''
            
            self.master.update()
            time.sleep(1)
            self.aviso['text'] = ''
            self.localidad['text'] = ''
                                    
            #self.timezon['int'] = 0
            
    def hora(self):        
        h = time.strftime("%H:%M:%S")
        self.current_time_label.configure(text = h)
        self.after(1000, self.hora)
        
    
    def widgets(self):

        #ruta = os.path.abspath("Estacion Climatologica/images/fuertes lluvias.png")
        
        self.inicio = PhotoImage(file ="Estacion Climatologica/images/buscar.gif")             
        self.imagen_temp = PhotoImage(file ="Estacion Climatologica/images/temperaturas.png")       
        self.imagen_temp_min = PhotoImage(file ="Estacion Climatologica/images/temperaturasMIN.png")        
        self.imagen_temp_max = PhotoImage(file ="Estacion Climatologica/images/temperaturasMAX.png")       
        self.imagen_humedad = PhotoImage(file ="Estacion Climatologica/images/lluvia.png")       
        self.imagen_viento = PhotoImage(file ="Estacion Climatologica/images/viento2.png")
        self.imagen_presion = PhotoImage(file ="Estacion Climatologica/images/presion.png")
                    
        #Texto solicitando que ingresen la localidad
        Label(self.frame,text='Ingrese su localidad: ',fg= 'white', bg='gray',font=('Helvetica',14)).grid(column=0,row=0, padx=5)
        
        #bloque de la ciudad
        self.ingresa_ciudad = Entry(self.frame, font=('Helvetica', 12),highlightbackground = "DarkOrchid1", highlightcolor= "green2", highlightthickness=2,width=30, justify=LEFT, takefocus= True)
        self.ingresa_ciudad.grid(column=1,row=0)
        
        #boton buscar
        self.bt_inicio = Button(self.frame, image= self.inicio, bg='red',highlightthickness=0, activebackground='white', bd=0, command = self.animacion)
        self.bt_inicio.grid(column=2, row=0, padx=5, pady=2)
        
        
        #Texto para posibles errores
        self.aviso = Label(self.frame,fg= 'white', bg='gray',font=('Comic Sans MS',14))
        self.aviso.grid(column=3,row=0, padx=5)
        
        #Texto con la localidad encontrada y su pais
        self.localidad = Label(self.frame,fg= 'white', bg='gray',font=('Helvetica',14, 'bold'))
        self.localidad.grid(column=4,row=0, padx=5)
              
        #Hora actual       
        self.current_time_label = Label(self.frame, text= '', fg= 'white', bg='gray',font=('Helvetica', 14, 'bold'))
        self.current_time_label.grid(column=5,row=0, padx=10)
        self.hora()
                
        
        #Títulos de cada frame
        Label(self.frame9,text='Tiempo', bg='#a1cda8', font=('Arial',11, 'bold')).pack(expand=False, pady=14)
        Label(self.frame10,text='Temperatura Real', bg='#a1cda8', font=('Arial',11, 'bold')).pack(expand=False, pady=14)
        
        Label(self.frame2,text='Temperatura', bg='#b5dfca', font=('Arial',11, 'bold')).pack(pady=14)
        Label(self.frame3,text='Temperatura Máxima', bg='#b5dfca', font=('Arial',11, 'bold')).pack(pady=14)
        Label(self.frame4,text='Temperatura Mínima' , bg='#b5dfca', font=('Arial',11, 'bold')).pack(pady=14)
        Label(self.frame5,text='Humedad' , bg='#b5dfca', font=('Arial',11, 'bold')).pack(pady=14)
        Label(self.frame6,text='Viento' , bg='#b5dfca', font=('Arial',11, 'bold')).pack(pady=14)
        Label(self.frame7,text='Presión' , bg='#b5dfca', font=('Arial',11, 'bold')).pack(pady=14)
        
        
        Label(self.frame2, image= self.imagen_temp, bg='#b5dfca').place(relx=0.29, rely=0.25, anchor='ne')
        Label(self.frame3, image= self.imagen_temp_max, bg='#b5dfca').place(relx=0.25, rely=0.25, anchor='ne')
        Label(self.frame4, image= self.imagen_temp_min, bg='#b5dfca').place(relx=0.25, rely=0.25, anchor='ne')
        Label(self.frame5, image= self.imagen_humedad, bg='#b5dfca').place(relx=0.28, rely=0.25, anchor='ne')
        Label(self.frame6, image= self.imagen_viento, bg='#b5dfca').place(relx=0.25, rely=0.25, anchor='ne')
        Label(self.frame7, image= self.imagen_presion, bg='#b5dfca').place(relx=0.25, rely=0.25, anchor='ne')
    
        #print(self.img_Tiempo)     #me imprime la ruta de la imagen que quiero mostrar con el tiempo actual      
        
        self.temp = Label(self.frame2,  bg='#b5dfca',font=('Impact',20))
        self.temp.pack(expand=True, side='right')
        self.temp_max = Label(self.frame3,bg='#b5dfca',font=('Impact',20))
        self.temp_max.pack(expand=True, side='right')
        self.temp_min = Label(self.frame4, bg='#b5dfca',font=('Impact',20))
        self.temp_min.pack(expand=True, side='right')
        self.temp_real = Label(self.frame10,bg='#a1cda8',font=('Impact',20))
        self.temp_real.pack(expand=True, side='right')
        
        self.humedad = Label(self.frame5, bg='#b5dfca',font=('Impact',20))
        self.humedad.pack(expand=True, side='right')
        self.viento = Label(self.frame6, bg='#b5dfca',font=('Impact',20))
        self.viento.pack(expand=True, side='right')
        self.presion = Label(self.frame7, bg='#b5dfca',font=('Impact',20))
        self.presion.pack(expand=True, side='right')
        
        self.clongitud = Label(self.frame8, bg='#c5e7e2',font=('Helvetica',11))
        self.clongitud.pack(expand=False, side='right', padx=20)
        self.clatitud = Label(self.frame8, bg='#c5e7e2',font=('Helvetica',11))
        self.clatitud.pack(expand=False, side='right',padx=20)
        
        
        #me muestra la descripción del tiempo actual               
        self.descripcion = Label(self.frame9, bg='#a1cda8',font=('Impact',16))
        self.descripcion.pack(expand=True, side='right', padx=5)
        
        
        self.amanecer = Label(self.frame8, bg='#c5e7e2',font=('Helvetica',11))
        self.amanecer.pack(expand=False, side='left', padx=20)
        self.anochecer = Label(self.frame8, bg='#c5e7e2',font=('Helvetica',11))
        self.anochecer.pack(expand=False, side='left', padx=20)
        

if __name__ == "__main__":
    ventana = Tk()
    ventana.title('Estación Climática by Tomi 1.1')
    ventana.config(bg= '#627264')
    #ventana.config(bg= 'sky blue') se puede usar tanto el codigo en exadecimal como los colores de tkinder definidos por nombre
    ventana.minsize(height= 430, width= 860)
    ventana.maxsize(height= 430, width= 1200)

    ruta = os.path.abspath("Estacion Climatologica/images/fuertes lluvias.png")
    ventana.call('wm', 'iconphoto', ventana._w, ImageTk.PhotoImage(file=ruta))

    ventana.geometry('860x420')
    #ventana.resizable(0,0) esto deshabilita el boton maximizar
    app = Estacion(ventana)
    app.mainloop()