from tkinter import TOP,Toplevel,BOTTOM,X,font,BOTH, Listbox,S,Tk,Radiobutton,Label,Button,messagebox,Entry,LabelFrame,W,StringVar,FLAT,END,N,Text,ACTIVE,Scrollbar,RIGHT,Y,LEFT,Spinbox
import PIL
from ttkbootstrap import Style
from datosDeRelleno import *
import pandas as pd
from estilo import *
import datetime as dt
import clases
from random import randint
from math import floor
import csv
import matplotlib.pyplot as plt
import numpy as np
from heapq import merge
from collections import OrderedDict


#Esta función permite rellenar los datos del paciente al buscarlo por rut
def autocompletarPaciente():
    _busqueda=buscar_rut_entry.get()
    paciente=clinica_objeto.buscarPaciente(_busqueda)

    if len(paciente)==0:
        messagebox.showwarning(message="No se ha podido encontrar el rut ingresado...", title="Error")
    
        for i in range(len(lista_entry_datos_paciente)):
            lista_entry_datos_paciente[i].delete(0,END)
            prevision_btn.set("Sin Prevision")
    
        return
    paciente=paciente[0]
    datos_paciente=[paciente.getRut(), paciente.getPrimerNombre(), paciente.getSegundoNombre(),paciente.getPrimerApellido(), paciente.getSegundoApellido(), paciente.getNumeroTelefonico(),paciente.getEmail(),paciente.getEdad()]

    prevision_btn.set(paciente.getPrevision())
    
    for i in range(len(datos_paciente)):
        lista_entry_datos_paciente[i].delete(0,END)
        lista_entry_datos_paciente[i].insert(0,datos_paciente[i])

#Permite la actualización de los datos
def actualizarListbox(datos):
    lista_medicos_listbox.delete(0,END)
    for medico in datos:
        lista_medicos_listbox.insert(END, medico.getNombreCompleto()+" "+medico.getEspecialidad())
    
    return

#función para seleccionar médicos
def seleccionarMedico(evento):
    medico_seleccionado_label["text"]=lista_medicos_listbox.get(ACTIVE)
    return

#función para buscar nombre de médico
def buscarMedico(evento):
    escrito=buscar_doctor_entry.get()
    
    if escrito == "":
        datos=clinica_objeto.getMedicos()
    else:
        datos=clinica_objeto.buscarMedico(escrito)
    
    actualizarListbox(datos)

#Actualiza medicos disponibles
def actualizarListboxCita(datos):
    lista_medicos_listbox.delete('0.0',END)
    for medico in datos:
        lista_medicos_listbox.insert('0.0', )

#
def seleccionarCita(evento):
    medico_seleccionado_label["text"]=lista_medicos_listbox.get(ACTIVE)

#función para buscar cita
def buscarCita(evento):
    escrito=buscar_doctor_entry.get()
    
    if escrito == "":
        datos=clinica_objeto.getMedicos()
    else:
        datos=clinica_objeto.buscarMedico(escrito)
    
    actualizarListbox(datos)

#función para cancelar la cita
def cancelarCita():
    busqueda= ingresar_codigo_entry.get()
    for paciente in clinica_objeto.getPacientes():
            paciente.eliminarCita(busqueda)
            info_cita_txtbox.delete('0.0',END)
            actualizarDatosCitas()
    for medico in clinica_objeto.getMedicos():
            medico.eliminarCita(busqueda)
            info_cita_txtbox.delete('0.0',END)
            actualizarDatosCitas()
    return False

#función para confirmar la cita
def confirmarCita():
    confirmada=0
    busqueda= ingresar_codigo_entry.get()
    for paciente in clinica_objeto.getPacientes():
        for cita in paciente.getCitas():
            if cita.getCodigo()==busqueda:
                info_cita_txtbox.delete('0.0',END)
                cita.setConfirmada(True)
                texto= "Fecha Citada: "+str(cita.getFechaCitada())+"\nPaciente: "+ cita.getPaciente().getNombreCompleto()+"\nMedico: "+cita.getMedico().getNombreCompleto()+"\nPrestacion: "+cita.getPrestacion()+"\nModalidad: "+cita.getModalidad()+"\nConfirmada: "+str(cita.getConfirmada())
                info_cita_txtbox.insert('0.0',texto)
                messagebox.showinfo(message="Cita confirmada")
                actualizarDatosCitas()

                confirmada=True
    for medico in clinica_objeto.getMedicos():
        for cita in medico.getCitas():
            if cita.getCodigo()==busqueda:
                info_cita_txtbox.delete('0.0',END)
                cita.setConfirmada(True)
                texto= "Fecha Citada: "+str(cita.getFechaCitada())+"\nMedico: "+ cita.getMedico().getNombreCompleto()+"\nMedico: "+cita.getMedico().getNombreCompleto()+"\nPrestacion: "+cita.getPrestacion()+"\nModalidad: "+cita.getModalidad()+"\nConfirmada: "+str(cita.getConfirmada())
                info_cita_txtbox.insert('0.0',texto)
                messagebox.showinfo(message="Cita confirmada")
                actualizarDatosCitas()

                confirmada=True
    if confirmada:return True
    else: return False

#buscar cita por codigo
def buscarCodigo():
    info_cita_txtbox.delete('0.0',END)
    busqueda= ingresar_codigo_entry.get()
    for paciente in clinica_objeto.getPacientes():
        for cita in paciente.getCitas():
            if cita.getCodigo()==busqueda:
                texto= "Fecha Citada: "+str(cita.getFechaCitada())+"\nPaciente: "+ cita.getPaciente().getNombreCompleto()+"\nMedico: "+cita.getMedico().getNombreCompleto()+"\nPrestacion: "+cita.getPrestacion()+"\nModalidad: "+cita.getModalidad()+"\nConfirmada: "+str(cita.getConfirmada())

                info_cita_txtbox.insert('0.0',texto)
                return
    info_cita_txtbox.insert(END,"Su cita no fue encontrada...\n Revise su codigo o comuniquese con nuestro equipo")

#verifica los datos ingresados para el paciente
# y marca aquellos entry dependiendo de si esta bien(verde) o mal (rojo)
def verificarDatosPaciente():
    
    for img in check_list:
        img.configure(image=nada_img)
    
    
    cant_error=0
    for i in range(len(lista_entry_datos_paciente)):
        fila=posicion_img[i][0]
        columna=posicion_img[i][1]
        check_list[i].grid(row=fila, column=columna)
        if i==0:
            if not(clases.Persona.isRut(rut_entry.get())) :
                lista_entry_datos_paciente[i].config(bg=Cinnabar)
                check_list[i].configure(image=equis_img)
                cant_error+=1
            else:
                lista_entry_datos_paciente[i].config(bg=JungleGreen)
                check_list[i].configure(image=check_img)
        elif i in [1,3,4]:       
            if not(lista_entry_datos_paciente[i].get().isalpha()):
                lista_entry_datos_paciente[i].config(bg=Cinnabar)
                check_list[i].configure(image=equis_img)
                cant_error+=1
                    
            else:
                lista_entry_datos_paciente[i].config(bg=JungleGreen)
                check_list[i].configure(image=check_img)
        elif i==5:
            if not(lista_entry_datos_paciente[i].get().isdigit()):
                lista_entry_datos_paciente[i].config(bg=Cinnabar)
                cant_error+=1
                check_list[i].configure(image=equis_img)
            else:
                lista_entry_datos_paciente[i].config(bg=JungleGreen)
                check_list[i].configure(image=check_img)
                          
        elif i==6:
            if not(clases.Persona.isMail(email_entry.get())):
                email_entry.config(bg=Cinnabar)
                check_list[i].configure(image=equis_img)
                cant_error+=1
            else:
                email_entry.config(bg=JungleGreen)
                check_list[i].configure(image=check_img)
        elif i==7:
            if not(edad_entry.get().isdigit()):
                edad_entry.config(bg=Cinnabar)
                check_list[i].configure(image=equis_img)
                cant_error+=1
            else:
                if int(edad_entry.get())<150 and int(edad_entry.get())>0:
                    edad_entry.config(bg=JungleGreen)
                    check_list[i].configure(image=check_img)
                else:
                    edad_entry.config(bg=Cinnabar)
                    check_list[i].configure(image=equis_img)
                    cant_error+=1
                    
                    
    if cant_error!=0:
        messagebox.showwarning(message="Los datos ingresados son INCORRECTOS, reviselos y vuelva a intentarlo", title="Error")
        return False    
    else:
        return True
       
#agrega un paciente

def agregarDatosPaciente():
     
    if not(verificarDatosPaciente()):
        return False
    else:
        paciente_temporal=clases.Paciente(nombre1_entry.get(), nombre2_entry.get(), apellido1_entry.get(), apellido2_entry.get(), rut_entry.get(), edad_entry.get(),
        email_entry.get(), tel_contacto_entry.get())
        paciente_temporal.setPrevision(prevision_btn.get())
        if clinica_objeto.agregarPaciente(paciente_temporal):
            messagebox.showinfo(message="Se han guardado sus datos correctamente", title="Éxito")
            agregarPacienteCSV()
            
        elegirFecha()
        return True

#función para cancelar los datos del paciente
def cancelarDatosPaciente():
    for img in check_list:
        img.configure(image=nada_img)
    
    prevision_btn.set("Sin Prevision")
    for i in range(len(lista_entry_datos_paciente)):
        lista_entry_datos_paciente[i].delete(0,END)
        lista_entry_datos_paciente[i].config(bg="#9ca2a9")
        
#función para modificar los datos agregados del paciente
def modificarDatosPaciente():
    if not(verificarDatosPaciente()):
        return False
    else:
        paciente_temporal=clases.Paciente(nombre1_entry.get(), nombre2_entry.get(), apellido1_entry.get(), apellido2_entry.get(), rut_entry.get(), edad_entry.get(),
        email_entry.get(), tel_contacto_entry.get())
        paciente_temporal.setPrevision(prevision_btn.get())
        if clinica_objeto.modificarPaciente(paciente_temporal):
            messagebox.showinfo(message="Los datos se han modificado", title="Éxito")
            actualizarDatosPacientes()

    cancelarDatosPaciente()
   
#función para agendar la cita
def elegirFecha():
    paciente=clinica_objeto.buscarPaciente(rut_entry.get())[0]
    medico= lista_medicos_listbox.get(ACTIVE).split()

    medico.pop()
    aux=""
    for palabra in medico:
        aux+=palabra+" "
    aux=aux[:-1]
    medico=clinica_objeto.buscarMedico(aux)[0]
    
    def agregarCita():
        temp.pack_forget()
        fecha= dt.datetime(int(seleccion_Año.get()), int(seleccion_Mes.get()), int(seleccion_Dia.get()),int(seleccion_hora.get()),int(seleccion_minutos.get()))
        cita_auxiliar=clases.Cita(fecha, medico, paciente, modalidad.get())
        if not(paciente.agregarCita(cita_auxiliar)) and not(medico.agregarCita(cita_auxiliar)):
            messagebox.showwarning(message="Esa hora no está disponible, intenta otra...", title="Error")
            return False
        
        else:
            label=Label(temp,text="La cita a sido agendada con exito\nGuarde el siguiente codigo para administrar su cita").pack()
            entry=Entry(temp)
            entry.pack(fill=Y, expand=True)
        
            label2=Label(temp,text="RECUERDE CONFIRMAR SU CITA O NO SERÁ ATENDIDO").pack()
            entry.insert(0,cita_auxiliar.getCodigo())
            entry.config(state="readonly")
            temp.pack()
            agregarCitaCSV()
            return True

    if medico_seleccionado_label["text"]=="":
        messagebox.showwarning(message="Recuerde escoger al Medico", title="Error")
        return
    #escoger modalidad
    
    elegir_fecha=Toplevel()
    modalidad.set("Online")
    escoger_fecha_frame=LabelFrame(elegir_fecha, text="Datos Cita",bg=Charade,font=subtitulo_font, labelanchor=N)
    temp=LabelFrame(elegir_fecha)
    escoger_modalidad=LabelFrame(escoger_fecha_frame,text="Modalidad",padx=5, pady=5,bg=Charade,font=subtitulo2_font, labelanchor=N)
    escoger_modalidad.pack(fill=BOTH, expand=True, padx=30, pady=10)
    online_btn=Radiobutton(escoger_modalidad,highlightthickness=0, text="Online", variable=modalidad,value="Online", bg=Charade,font=subtitulo5_font)
    online_btn.grid(row=0,column=0)
    presencial_btn=Radiobutton(escoger_modalidad,highlightthickness=0, text="Presencial", variable=modalidad,value="Presencial", bg=Charade, font=subtitulo5_font)
    presencial_btn.grid(row=0,column=1)

    #seleccionar fecha cita
    disponibilidad_citas_frame=LabelFrame(escoger_fecha_frame, text="Seleccionar fecha:", bg=Charade, font=subtitulo2_font, labelanchor=N)
    disponibilidad_citas_frame.pack(fill=BOTH, expand=True, padx=30, pady=10)
    seleccion_Dia=Spinbox(disponibilidad_citas_frame,width=10,state="readonly" ,values=("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))
    seleccion_Dia.grid(row=1, column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Día",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=1,column=0)
    seleccion_Mes=Spinbox(disponibilidad_citas_frame,width=10 ,values=("01","01","03","04","05","06","07","08","09","10","11","12"),state="readonly" )
    seleccion_Mes.grid(row=2,column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Mes",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=2,column=0)
    seleccion_Año=Spinbox(disponibilidad_citas_frame,width=10,state="readonly"  ,values=("2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031"))
    seleccion_Año.grid(row=3,column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Año",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=3,column=0)
    #seleccionar hora cita
    seleccion_hora=Spinbox(disponibilidad_citas_frame,width=10,state="readonly" ,values=("8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"))
    seleccion_minutos=Spinbox(disponibilidad_citas_frame,width=10 ,values=("00","30"))
    seleccion_hora.grid(row=4,column=1)
    seleccion_minutos.grid(row=5,column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Hora",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=4,column=0)
    dia_label=Label(disponibilidad_citas_frame,text="Minutos",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=5,column=0)
    
   
    boton_hora=Button(disponibilidad_citas_frame,text="Reservar Hora",command=lambda:agregarCita(), image = reservar_hora_ic)
    boton_hora.grid(row=6,column=0, columnspan=2)
    escoger_fecha_frame.pack()
    
#reagenda un cita  
def reagendarCita():
    paciente=clinica_objeto.buscarPaciente(rut_entry.get())[0]
    medico= lista_medicos_listbox.get(ACTIVE).split()

    medico.pop()
    aux=""
    for palabra in medico:
        aux+=palabra+" "
    aux=aux[:-1]
    medico=clinica_objeto.buscarMedico(aux)[0]

    busqueda= ingresar_codigo_entry.get()
    def reagendarCita():
        fecha= dt.datetime(int(seleccion_Año.get()), int(seleccion_Mes.get()), int(seleccion_Dia.get()),int(seleccion_hora.get()),int(seleccion_minutos.get()))
 
        for paciente in clinica_objeto.getPacientes():
            if paciente.modificarCita(fecha,busqueda):
                buscarCodigo()

                elegir_fecha.destroy()
                messagebox.showinfo(message="La cita ha sido reagendada con exito", title="Éxito")
    



    elegir_fecha=Toplevel()
    escoger_fecha_frame=LabelFrame(elegir_fecha, text="Datos Cita",bg=Charade,font=subtitulo_font, labelanchor=N)
    temp=LabelFrame(elegir_fecha)

    #seleccionar fecha cita
    disponibilidad_citas_frame=LabelFrame(escoger_fecha_frame, text="Seleccionar fecha:", bg=Charade, font=subtitulo2_font, labelanchor=N)
    disponibilidad_citas_frame.pack(fill=BOTH, expand=True, padx=30, pady=10)
    seleccion_Dia=Spinbox(disponibilidad_citas_frame,width=10,state="readonly" ,values=("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))
    seleccion_Dia.grid(row=1, column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Día",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=1,column=0)
    seleccion_Mes=Spinbox(disponibilidad_citas_frame,width=10 ,values=("01","01","03","04","05","06","07","08","09","10","11","12"),state="readonly" )
    seleccion_Mes.grid(row=2,column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Mes",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=2,column=0)
    seleccion_Año=Spinbox(disponibilidad_citas_frame,width=10,state="readonly"  ,values=("2021","2022","2023","2024","2025","2026","2027","2028","2029","2030","2031"))
    seleccion_Año.grid(row=3,column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Año",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=3,column=0)
    #seleccionar hora cita
    seleccion_hora=Spinbox(disponibilidad_citas_frame,width=10,state="readonly" ,values=("8","9","10","11","12","13","14","15","16","17","18","19","20","21","22"))
    seleccion_minutos=Spinbox(disponibilidad_citas_frame,width=10 ,values=("00","30"))
    seleccion_hora.grid(row=4,column=1)
    seleccion_minutos.grid(row=5,column=1)
    dia_label=Label(disponibilidad_citas_frame,text="Hora",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=4,column=0)
    dia_label=Label(disponibilidad_citas_frame,text="Minutos",bg=Charade, font=subtitulo4_font)
    dia_label.grid(row=5,column=0)
    
   
    boton_hora=Button(disponibilidad_citas_frame,text="Reservar Hora",command=lambda:reagendarCita(), image = reservar_hora_ic)
    boton_hora.grid(row=6,column=0, columnspan=2)
    escoger_fecha_frame.pack()
    actualizarDatosCitas()
"""
def actualizarImg():
    lista_datos=leerArchivos()
    graficarDatos(False,lista_datos[0],"Edades de los Pacientes","bar","Edades", "Pacientes por Edad")
    graficarDatos(False,lista_datos[1],"Especialidades de los doctores","pie", "Especialidades")
    graficarDatos(False,lista_datos[2],"Modalidad","pie", "Modalidad de la cita")
    graficarDatos(False,lista_datos[3],"Prestación","pie", "Prestación de los pacientes")
    graficarDatos(False,lista_datos[4],"Previsión del paciente","pie", "Previsión de los pacientes")
    graficarDatos(False,lista_datos[5],"Pacientes confirmados","pie", "Pacientes que han confirmado")
    edades_grafico_img = PIL.Image.open('./imagenes/Edades de los Pacientes.png')
    edades_grafico_img =edades_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
    edades_grafico_img = PIL.ImageTk.PhotoImage(edades_grafico_img)
    edades_grafico_btn.config(image =edades_grafico_img)
    
    especialidades_grafico_img = PIL.Image.open('./imagenes/Especialidades de los doctores.png')
    especialidades_grafico_img =especialidades_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
    especialidades_grafico_img = PIL.ImageTk.PhotoImage(especialidades_grafico_img)
    especialidades_grafico_btn.config(image =especialidades_grafico_img)
   

    modalidad_grafico_img = PIL.Image.open('./imagenes/Modalidad.png')
    modalidad_grafico_img =modalidad_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
    modalidad_grafico_img = PIL.ImageTk.PhotoImage(modalidad_grafico_img)
    modalidad_grafico_btn.config(image =modalidad_grafico_img)

    prestacion_grafico_img = PIL.Image.open('./imagenes/Prestación.png')
    prestacion_grafico_img =prestacion_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
    prestacion_grafico_img = PIL.ImageTk.PhotoImage(prestacion_grafico_img)
    prestacion_grafico_btn.config(image =prestacion_grafico_img)

    prevision_grafico_img = PIL.Image.open('./imagenes/Previsión del paciente.png')
    prevision_grafico_img =prevision_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
    prevision_grafico_img = PIL.ImageTk.PhotoImage(prevision_grafico_img)
    prevision_grafico_btn.config(image =prevision_grafico_img)

    confirmados_grafico_img = PIL.Image.open('./imagenes/Pacientes confirmados.png')
    confirmados_grafico_img =confirmados_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
    confirmados_grafico_img = PIL.ImageTk.PhotoImage(confirmados_grafico_img)
    confirmados_grafico_btn.config(image =confirmados_grafico_img)

"""
#csv manage
def leerArchivos():
    
    datos_pacientes = pd.read_csv('./datos/Pacientes.csv')
    edad_pacientes=datos_pacientes["edad"].values
    datos_prevision = datos_pacientes["prevision"].values
    #datos_ultima_prestacion=datos_pacientes["ultima prestacion"]
    #graficarDatos(edad_pacientes,"Edades de los Pacientes","bar","Edades", "Pacientes por Edad")

    especialidad_medicos = pd.read_csv('./datos/Medicos.csv')
    especialidad_medicos=especialidad_medicos["especialidad"].values
    #graficarDatos(especialidad_medicos,"Especialidades","pie")

    datos_citas = pd.read_csv("./datos/Citas.csv")
    datos_modalidad = datos_citas["modalidad"].values
    datos_prestacion = datos_citas["prestacion"].values
    confirmados = datos_citas["confirmada"].values
    lista_datos = [edad_pacientes, especialidad_medicos, datos_modalidad, datos_prestacion, datos_prevision, confirmados]
    return lista_datos

def agregarPacienteCSV():
    pacientes_csv = pd.read_csv('./datos/Pacientes.csv', index_col=0)
    agregar={'nombre completo': [clinica_objeto.getPacientes()[-1].getNombreCompleto()],
            'rut': [clinica_objeto.getPacientes()[-1].getRut()],
            'edad': [clinica_objeto.getPacientes()[-1].getEdad()],
            'email': [clinica_objeto.getPacientes()[-1].getEmail()],
            'numero de telefono': [clinica_objeto.getPacientes()[-1].getNumeroTelefonico()],
            'prevision': [clinica_objeto.getPacientes()[-1].getPrevision()]
            }
    pacientes_csv=pd.DataFrame(pacientes_csv)
    agregar=pd.DataFrame(agregar)
    pacientes_csv=pacientes_csv.append(agregar,ignore_index=True)
    pacientes_csv=pacientes_csv.drop_duplicates(subset="rut",ignore_index=True)
    pacientes_csv.to_csv("./datos/Pacientes.csv")
    actualizarDatosPacientes()

def agregarCitaCSV():
    citas_csv = pd.read_csv('./datos/Citas.csv', index_col=0)
    agregar={'codigo': [clinica_objeto.getCitas()[-1].getCodigo()],
             'rut paciente':[clinica_objeto.getCitas()[-1].getPaciente().getRut()],
             'rut medico':[clinica_objeto.getCitas()[-1].getMedico().getRut()],
             'fecha citada': [clinica_objeto.getCitas()[-1].getFechaCitada()],
             'fecha de creacion':[clinica_objeto.getCitas()[-1].getFechaCreacion()],
             'modalidad':[clinica_objeto.getCitas()[-1].getModalidad()],
             'prestacion':[clinica_objeto.getCitas()[-1].getPrestacion()],
             'confirmada':[clinica_objeto.getCitas()[-1].getConfirmada()],
             'tiempo restante':[clinica_objeto.getCitas()[-1].getTiempoRestante()]
             }
    citas_csv=pd.DataFrame(citas_csv)
    agregar=pd.DataFrame(agregar)
    citas_csv=citas_csv.append(agregar,ignore_index=True)
    citas_csv=citas_csv.drop_duplicates(subset="codigo",ignore_index=True)
    citas_csv.to_csv("./datos/Citas.csv")
    actualizarDatosCitas()

def merge_sort(m):
    if len(m) <= 1:
        return m
 
    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]
 
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))

def graficarDatos(caso,_datos,_titulo,_f,_titulo_x="x",_titulo_y="y"):
    aux = _datos.tolist()
    try:
        aux = merge_sort(aux)
        _datos=aux
    except TypeError:
        _datos=aux
    auxOrdenado = list(dict.fromkeys(_datos))
    count = 0
    cantidad = []
    for a in range (len(auxOrdenado)):
        cantidad.append(_datos.count(auxOrdenado[a]))
  

    porcentajes = []
    for a in range (len(cantidad)):
        porcentajes.append((cantidad[a]/(len(_datos)))*100)
        
   
    porAproximados =np.around(porcentajes).tolist()
    porAproximadosFinal = []

    for a in range (len(cantidad)):
        porAproximadosFinal.append(str(porAproximados[a])+"%")

   #datos
    datos=[]
    for a in range (len(cantidad)):
        datos.append(str(auxOrdenado[a]))

    if _f=="pie":
        plt.pie(porAproximados, explode=None, labels=porAproximadosFinal, shadow=True)
        plt.legend(datos, title= "Codigo de Color", loc=0, bbox_to_anchor=(0.1 , 0.3), shadow=True)
        plt.title("Porcentaje de "+_titulo)
        plt.savefig(f"./imagenes/"+_titulo+".png",dpi=300,bbox_inches="tight")
        if caso:plt.show()
        plt.close()

    elif _f=="bar":
        plt.bar(datos, cantidad, align="center")
        plt.title(_titulo)
        plt.ylabel(_titulo_y)
        plt.xlabel(_titulo_x)
        plt.grid(axis="y")
        plt.savefig(f"./imagenes/"+_titulo+".png",dpi=300,bbox_inches="tight")
        if caso:plt.show()
        plt.close()
    
def actualizarDatosPacientes():
   
    agregar={'nombre completo': [],
                'rut': [],
                'edad': [],
                'email': [],
                'numero de telefono': [],
                'prevision': []
                }
    pacientes_csv=pd.DataFrame(columns=agregar.keys())

    for paciente in clinica_objeto.getPacientes():
        agregar={'nombre completo': [paciente.getNombreCompleto()],
                'rut': [paciente.getRut()],
                'edad': [paciente.getEdad()],
                'email': [paciente.getEmail()],
                'numero de telefono': [paciente.getNumeroTelefonico()],
                'prevision': [paciente.getPrevision()],
                'ultima prestacion':[paciente.getUltimaPrestacion()]
                }
        agregar=pd.DataFrame(agregar)
        pacientes_csv=pacientes_csv.append(agregar,ignore_index=True)
    pacientes_csv=pacientes_csv.drop_duplicates(subset="rut",ignore_index=True)
    pacientes_csv.to_csv("./datos/Pacientes.csv")
    

def actualizarDatosCitas():
    agregar={'codigo': [],
             'rut paciente':[],
             'rut medico':[],
             'fecha citada': [],
             'fecha de creacion':[],
             'modalidad':[],
             'prestacion':[],
             'confirmada':[],
             'tiempo restante':[]
             }
    citas_csv=pd.DataFrame(columns=agregar.keys())
    for cita in clinica_objeto.getCitas():
        agregar={'codigo': [cita.getCodigo()],
             'rut paciente':[cita.getPaciente().getRut()],
             'rut medico':[cita.getMedico().getRut()],
             'fecha citada': [cita.getFechaCitada()],
             'fecha de creacion':[cita.getFechaCreacion()],
             'modalidad':[cita.getModalidad()],
             'prestacion':[cita.getPrestacion()],
             'confirmada':[cita.getConfirmada()],
             'tiempo restante':[cita.getTiempoRestante()]
             }
        agregar=pd.DataFrame(agregar)
        citas_csv=citas_csv.append(agregar,ignore_index=True)
    citas_csv=citas_csv.drop_duplicates(subset="codigo",ignore_index=True)
    citas_csv.to_csv("./datos/Citas.csv")
   


def informacionCitas():
    
    return
ventana_principal=Tk()
ventana_principal.title(str(clinica_objeto.getNombre())) 
ventana_principal.resizable(0,0)
lista_entry_datos_paciente=[]
s=Style()
s.theme_use("darkly")
posicion_img=[]

#boton para guardar fecha y hora
reservar_hora_ic = PIL.Image.open('./imagenes/reservarhora.png')
reservar_hora_ic = reservar_hora_ic.resize((50, 50), PIL.Image.ANTIALIAS)
reservar_hora_ic = PIL.ImageTk.PhotoImage(reservar_hora_ic)


#FUENTES
titulo_font = font.Font(family="Arial",weight="bold",size=35)
subtitulo_font = font.Font(family="Arial Nova", weight="bold",size= 20)
subtitulo2_font = font.Font(family="Arial Narrow", weight="bold",size=15)
subtitulo3_font = font.Font (family= "Arial Narrow", size= 15)
subtitulo4_font = font.Font (family= "Arial Narrow", size= 15)
subtitulo5_font = font.Font (family= "Arial Narrow", size= 12)



#Todas las entradas necesarias para una cita
agendar_cita_frame=LabelFrame(ventana_principal,relief=FLAT, bg=Charade,bd=0)
agendar_cita_frame.pack(side=LEFT,fill=Y, expand=True, padx=40, pady=40)
agendar_cita_label=Label(agendar_cita_frame, text="Agendar Cita",font=titulo_font,bg=CuriousBlue, highlightthickness=0)
agendar_cita_label.pack(fill=X)

buscar_medico_frame=LabelFrame(agendar_cita_frame,text="Buscar Medico",width=30, bg=Charade, font=subtitulo_font, labelanchor=N)
buscar_medico_frame.pack(fill=BOTH, expand=True, padx=30, pady=10)
buscar_doctor_label=Label(buscar_medico_frame, text="Ingrese su Busqueda:", bg=Charade, font=subtitulo2_font)
buscar_doctor_label.grid(row=0,column=0,sticky=W)
buscar_doctor_entry=Entry(buscar_medico_frame, width=30, highlightthickness=0,relief=FLAT)
buscar_doctor_entry.grid(row=1,column=0, sticky=W)


framelistbox=LabelFrame(buscar_medico_frame, relief=FLAT)
framelistbox.grid(row=2,column=0)
lista_medicos_listbox=Listbox(framelistbox,width=45,height=4)
lista_medicos_listbox.pack(side=LEFT)
medico_seleccionado_label=Label(buscar_medico_frame, bg=Charade, font=subtitulo5_font)
buscar_doctor_label=Label(buscar_medico_frame, text="Medico escogido:", bg=Charade, font=subtitulo2_font)
buscar_doctor_label.grid(row=3,column=0,sticky=W)
medico_seleccionado_label.grid(row=4,column=0,sticky=W)
scrollbar = Scrollbar(framelistbox)
scrollbar.pack(side=RIGHT,fill=Y)
lista_medicos_listbox.config(yscrollcommand=scrollbar.set)
 
scrollbar.config(command=lista_medicos_listbox.yview)

    #Ingreso de datos del paciente

ingresar_paciente=LabelFrame(agendar_cita_frame,text="Datos del Paciente", bg=Charade, font=subtitulo_font, labelanchor=N)
ingresar_paciente.pack(fill=BOTH, expand=True, padx=30, pady=10)

    #autocompletar con rut

buscar_rut_ic = PIL.Image.open('./imagenes/buscapaciente.png')
buscar_rut_ic = buscar_rut_ic.resize((30, 30), PIL.Image.ANTIALIAS)
buscar_rut_ic = PIL.ImageTk.PhotoImage(buscar_rut_ic)
buscar_rut_label=Label(ingresar_paciente, text="Rut(sin puntos): ")
buscar_rut_label.grid(row=0,column=0)
buscar_rut_entry=Entry(ingresar_paciente, width=10)
buscar_rut_entry.grid(row=0,column=1,sticky=W)
buscar_rut_btn=Button(ingresar_paciente, text="Buscar" ,command=lambda:autocompletarPaciente(),  image=buscar_rut_ic)
buscar_rut_btn.grid(row=0,column=2)
rut_autocompletar_label=Label(ingresar_paciente, text="Buscar paciente por Rut: ", bg=Charade, font=subtitulo4_font)
rut_autocompletar_label.grid(row=0,column=0)

    #prevision
prevision_label=Label(ingresar_paciente, text="Prevision del Paciente:", bg=Charade, font=subtitulo4_font)
prevision_label.grid(row=1,column=0)
prevision_btn=StringVar()
prevision_btn.set("Sin Prevision")
opciones_prevision_frame=LabelFrame(ingresar_paciente, bg=Charade, relief=FLAT, bd=0)
opciones_prevision_frame.grid(columnspan=3)
sin_prevision_btn=Radiobutton(opciones_prevision_frame,highlightthickness=0, text="Sin Prevision", variable=prevision_btn,value="Sin Prevision", bg=Charade, font=subtitulo5_font)
sin_prevision_btn.pack(side=LEFT)
isapre_btn=Radiobutton(opciones_prevision_frame,highlightthickness=0,bg=Charade, text="Isapre", variable=prevision_btn,value="ISAPRE",  font=subtitulo5_font)
isapre_btn.pack(side=LEFT)
fonasa_btn=Radiobutton(opciones_prevision_frame,highlightthickness=0, text="Fonasa", variable=prevision_btn,value="FONASA", bg=Charade, font=subtitulo5_font)
fonasa_btn.pack(side=LEFT)


#
check_list=[]
    #rut
nada_img = PIL.Image.open('./imagenes/nada.png')
nada_img = nada_img.resize((10, 10),PIL.Image.ANTIALIAS)
nada_img = PIL.ImageTk.PhotoImage(nada_img)

check_img = PIL.Image.open('./imagenes/check.png')
check_img = check_img.resize((10, 10),PIL.Image.ANTIALIAS)
check_img = PIL.ImageTk.PhotoImage(check_img)

equis_img = PIL.Image.open('./imagenes/equis.png')
equis_img = equis_img.resize((10, 10),PIL.Image.ANTIALIAS)
equis_img = PIL.ImageTk.PhotoImage(equis_img)

rut_label=Label(ingresar_paciente, text="Rut (sin puntos):",bg=Charade, font=subtitulo4_font)
rut_label.grid(row=3,column=0)
rut_entry=Entry(ingresar_paciente, width=10)
rut_entry.grid(row=3,column=1)
lista_entry_datos_paciente.append(rut_entry)
rut_img=Label(ingresar_paciente,image=nada_img, bg=Charade)
check_list.append(rut_img)
posicion_img.append([3,2])

    #primer nombre

nombre1_label=Label(ingresar_paciente, text="Primer Nombre:",bg=Charade, font=subtitulo4_font)
nombre1_label.grid(row=4,column=0)
nombre1_entry=Entry(ingresar_paciente, width=10)
nombre1_entry.grid(row=4,column=1)
lista_entry_datos_paciente.append(nombre1_entry)
nombre1_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(nombre1_img)
posicion_img.append([4,2])

    #segundo nombre
nombre2_label=Label(ingresar_paciente, text="Segundo Nombre:", bg=Charade, font=subtitulo4_font)
nombre2_label.grid(row=5,column=0)
nombre2_entry=Entry(ingresar_paciente, width=10)
nombre2_entry.grid(row=5,column=1)
lista_entry_datos_paciente.append(nombre2_entry)
nombre2_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(nombre2_img)
posicion_img.append([5,2])

    #Primer Apellido
apellido1_label=Label(ingresar_paciente, text="Primer Apellido:", bg=Charade, font=subtitulo4_font)
apellido1_label.grid(row=6,column=0)
apellido1_entry=Entry(ingresar_paciente, width=10)
apellido1_entry.grid(row=6,column=1)
lista_entry_datos_paciente.append(apellido1_entry)
apellido1_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(apellido1_img)
posicion_img.append([6,2])

    #Segundo Apellido
apellido2_label=Label(ingresar_paciente, text="Segundo Apellido:", bg=Charade, font=subtitulo4_font)
apellido2_label.grid(row=7,column=0)
apellido2_entry=Entry(ingresar_paciente, width=10)
apellido2_entry.grid(row=7,column=1)
apellido2_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(apellido2_img)
lista_entry_datos_paciente.append(apellido2_entry)
posicion_img.append([7,2])
    
    #numero contacto
tel_contacto_label=Label(ingresar_paciente, text="Número Telefono/Celular:", bg=Charade, font=subtitulo4_font)
tel_contacto_label.grid(row=8,column=0)
tel_contacto_entry=Entry(ingresar_paciente, width=10)
tel_contacto_entry.grid(row=8,column=1)
lista_entry_datos_paciente.append(tel_contacto_entry)
tel_contacto_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(tel_contacto_img)
posicion_img.append([8,2])

    #email
email_label=Label(ingresar_paciente, text="Correo Electronico:", bg=Charade, font=subtitulo4_font)
email_label.grid(row=9,column=0)
email_entry=Entry(ingresar_paciente, width=10)
email_entry.grid(row=9,column=1)
lista_entry_datos_paciente.append(email_entry)
email_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(email_img)
posicion_img.append([9,2])

#edad
edad_label=Label(ingresar_paciente, text="Edad:", bg=Charade, font=subtitulo4_font)
edad_label.grid(row=10,column=0)
edad_entry=Entry(ingresar_paciente, width=10)
edad_entry.grid(row=10,column=1)
lista_entry_datos_paciente.append(edad_entry)
edad_img=Label(ingresar_paciente,image=nada_img,bg=Charade)
check_list.append(edad_img)
posicion_img.append([10,2])


#Frame de botones para agregar el paciente, borrar todas las entradas de datos de paciente o modificar sus datos.

botones_paciente_frame=LabelFrame(ingresar_paciente, bd=0, relief=FLAT,bg=Charade)
botones_paciente_frame.grid(columnspan=3,row=11,column=0)

confirmar_paciente_ic = PIL.Image.open('./imagenes/confirmar_paciente.png')
confirmar_paciente_ic = confirmar_paciente_ic.resize((50, 50), PIL.Image.ANTIALIAS)
confirmar_paciente_ic = PIL.ImageTk.PhotoImage(confirmar_paciente_ic)
confirmar_paciente_btn=Button(botones_paciente_frame,text="Confirmar", image = confirmar_paciente_ic, command=lambda:agregarDatosPaciente())
confirmar_paciente_btn.pack(side=LEFT,padx=30)

cancelar_paciente_ic = PIL.Image.open('./imagenes/cancelar_paciente.png')
cancelar_paciente_ic = cancelar_paciente_ic.resize((50, 50), PIL.Image.ANTIALIAS)
cancelar_paciente_ic = PIL.ImageTk.PhotoImage(cancelar_paciente_ic)
cancelar_paciente_btn=Button(botones_paciente_frame,text="Cancelar", image = cancelar_paciente_ic, command=lambda:cancelarDatosPaciente())
cancelar_paciente_btn.pack(side=RIGHT,padx=30)

modificar_paciente_ic = PIL.Image.open('./imagenes/modificarpaciente.png')
modificar_paciente_ic = modificar_paciente_ic.resize((50, 50), PIL.Image.ANTIALIAS)
modificar_paciente_ic = PIL.ImageTk.PhotoImage(modificar_paciente_ic)
modificar_paciente_btn=Button(botones_paciente_frame,text="Cancelar", image = modificar_paciente_ic, command=lambda:modificarDatosPaciente())
modificar_paciente_btn.pack(side=RIGHT,padx=30)


#en este se mostraran las citas por paciente, o por codigo de cita y debe confirmar, cancelar o reagendar la cita necesaria

citas_agendadas_frame=LabelFrame(ventana_principal,relief=FLAT, bg=Charade,bd=0)
citas_agendadas_frame.pack(side=LEFT,fill=X, expand=True, padx=40, pady=40, anchor=N)
citas_agendadas_label=Label(citas_agendadas_frame,bg=CuriousBlue, text="Mis Citas",font=titulo_font, highlightthickness=0)
citas_agendadas_label.pack(fill=X)

#ingresa el codigo
gestionar_cita_frame=LabelFrame(citas_agendadas_frame,text="Información de la Cita",bg=Charade,font=subtitulo_font, labelanchor=N)
gestionar_cita_frame.pack(fill=Y, expand=True, padx=30, pady=10)
ingresar_codigo_label=Label(gestionar_cita_frame, text="Ingrese el código de su cita",bg=Charade,font=subtitulo2_font)
ingresar_codigo_label.pack()
ingresar_codigo_entry=Entry(gestionar_cita_frame, width=30)
ingresar_codigo_entry.pack()

#Boton buscar
buscar_cita_ic = PIL.Image.open('./imagenes/buscacita.png')
buscar_cita_ic = buscar_cita_ic.resize((50, 50), PIL.Image.ANTIALIAS)
buscar_cita_ic = PIL.ImageTk.PhotoImage(buscar_cita_ic)
buscar_btn=Button(gestionar_cita_frame,text="Buscar", image=buscar_cita_ic, command=lambda:buscarCodigo())
buscar_btn.pack(pady=10)

#muestra la informacion encontrada de la cita
info_cita_txtbox=Text(gestionar_cita_frame,width=50,height=20)

info_cita_txtbox.pack(padx=10)

agendar_hora_ic = PIL.Image.open('./imagenes/confirmar.png')
agendar_hora_ic = agendar_hora_ic.resize((50, 50), PIL.Image.ANTIALIAS)
agendar_hora_ic = PIL.ImageTk.PhotoImage(agendar_hora_ic)
agendar_hora_btn=Button(gestionar_cita_frame,text="Confirmar", image = agendar_hora_ic,command=lambda:confirmarCita())
agendar_hora_btn.pack(side=LEFT,padx=15,pady=10)

cancelar_hora_ic = PIL.Image.open('./imagenes/cancelar.png')
cancelar_hora_ic = cancelar_hora_ic.resize((50, 50), PIL.Image.ANTIALIAS)
cancelar_hora_ic = PIL.ImageTk.PhotoImage(cancelar_hora_ic)
cancelar_hora_btn=Button(gestionar_cita_frame,text="Cancelar", image = cancelar_hora_ic, command=lambda:cancelarCita())
cancelar_hora_btn.pack(side=RIGHT,padx=15,pady=10)

#boton reagendar
reagendar_hora_ic = PIL.Image.open('./imagenes/reagendar.png')
reagendar_hora_ic = reagendar_hora_ic.resize((50, 50), PIL.Image.ANTIALIAS)
reagendar_hora_ic = PIL.ImageTk.PhotoImage(reagendar_hora_ic)
reagendar_hora_btn=Button(gestionar_cita_frame,text="Reagendar", image = reagendar_hora_ic,command=lambda:reagendarCita())
reagendar_hora_btn.pack(side=BOTTOM,padx=15,pady=10)


#dashboard y cita actual
dashboard_frame=LabelFrame(ventana_principal,relief=FLAT, bg=Charade,bd=0)
dashboard_frame.pack(side=LEFT,fill=Y, expand=True, padx=40, pady=40)
dashboard_label=Label(dashboard_frame, text="Dashboard",font=titulo_font,bg=CuriousBlue, highlightthickness=0)
dashboard_label.pack(fill=X)
dashboard_btn_lista=[]
lista_datos=leerArchivos()
graficarDatos(False,lista_datos[0],"Edades de los Pacientes","bar","Edades", "Pacientes por Edad")
graficarDatos(False,lista_datos[1],"Especialidades de los doctores","pie", "Especialidades")
graficarDatos(False,lista_datos[2],"Modalidad","pie", "Modalidad de la cita")
graficarDatos(False,lista_datos[3],"Prestación","pie", "Prestación de los pacientes")
graficarDatos(False,lista_datos[4],"Previsión del paciente","pie", "Previsión de los pacientes")
graficarDatos(False,lista_datos[5],"Pacientes confirmados","pie", "Pacientes que han confirmado")



edades_grafico_img = PIL.Image.open('./imagenes/Edades de los Pacientes.png')
edades_grafico_img =edades_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
edades_grafico_img = PIL.ImageTk.PhotoImage(edades_grafico_img)
edades_grafico_btn=Button(dashboard_frame, image =edades_grafico_img, command= lambda: graficarDatos(True,lista_datos[0],"Edades de los Pacientes","bar","Edades", "Pacientes por Edad"))
dashboard_btn_lista.append(edades_grafico_btn)

especialidades_grafico_img = PIL.Image.open('./imagenes/Especialidades de los doctores.png')
especialidades_grafico_img =especialidades_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
especialidades_grafico_img = PIL.ImageTk.PhotoImage(especialidades_grafico_img)
especialidades_grafico_btn=Button(dashboard_frame, image =especialidades_grafico_img, command= lambda:graficarDatos(True,lista_datos[1],"Especialidades de los doctores","pie", "Especialidades"))
dashboard_btn_lista.append(especialidades_grafico_btn)

modalidad_grafico_img = PIL.Image.open('./imagenes/Modalidad.png')
modalidad_grafico_img =modalidad_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
modalidad_grafico_img = PIL.ImageTk.PhotoImage(modalidad_grafico_img)
modalidad_grafico_btn=Button(dashboard_frame, image =modalidad_grafico_img, command= lambda: graficarDatos(True,lista_datos[2],"Modalidad","pie", "Modalidad de la cita"))
dashboard_btn_lista.append(modalidad_grafico_btn)

prestacion_grafico_img = PIL.Image.open('./imagenes/Prestación.png')
prestacion_grafico_img =prestacion_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
prestacion_grafico_img = PIL.ImageTk.PhotoImage(prestacion_grafico_img)
prestacion_grafico_btn=Button(dashboard_frame, image =prestacion_grafico_img, command= lambda: graficarDatos(True,lista_datos[3],"Prestación","pie", "Prestación de los pacientes"))
dashboard_btn_lista.append(prestacion_grafico_btn)

prevision_grafico_img = PIL.Image.open('./imagenes/Previsión del paciente.png')
prevision_grafico_img =prevision_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
prevision_grafico_img = PIL.ImageTk.PhotoImage(prevision_grafico_img)
prevision_grafico_btn=Button(dashboard_frame, image =prevision_grafico_img, command= lambda: graficarDatos(True,lista_datos[4],"Previsión del paciente","pie", "Previsión de los pacientes"))
dashboard_btn_lista.append(prevision_grafico_btn)

confirmados_grafico_img = PIL.Image.open('./imagenes/Pacientes confirmados.png')
confirmados_grafico_img =confirmados_grafico_img.resize((200, 100), PIL.Image.ANTIALIAS)
confirmados_grafico_img = PIL.ImageTk.PhotoImage(confirmados_grafico_img)
confirmados_grafico_btn=Button(dashboard_frame, image =confirmados_grafico_img, command= lambda: graficarDatos(True,lista_datos[5],"Pacientes confirmados","pie", "Pacientes que han confirmado")
)
dashboard_btn_lista.append(confirmados_grafico_btn)


for btn in dashboard_btn_lista:
    btn.pack()
modalidad=StringVar()


actualizarListbox(clinica_objeto.getMedicos())
lista_medicos_listbox.bind("<<ListboxSelect>>", seleccionarMedico)

ventana_principal.mainloop()
