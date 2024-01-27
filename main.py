from tkinter import *
from tkinter import ttk
from conexion import *

ventana = Tk()
ventana.title("Crud MySql Tkinter")
ventana.geometry("600x500")

db = DataBase()
modificar= False
dni=StringVar()
genero=StringVar()
nombres=StringVar()
apellidos=StringVar()


def seleccionar(event):
    id= tvEstudiantes.selection()[0]
    if int(id)>0:
        dni.set(tvEstudiantes.item(id, "values")[1])
        genero.set(tvEstudiantes.item(id, "values")[2])
        nombres.set(tvEstudiantes.item(id, "values")[3])
        apellidos.set(tvEstudiantes.item(id, "values")[4])


marco= LabelFrame(ventana, text="Formulario de gestión de estudiantes")
marco.place(x=50, y=50, width=500,height=400)

# labels and entrys
lblDni= Label(marco, text="DNI").grid(column= 0,row=0, padx=5,pady=5)
txtDni= Entry(marco, textvariable= dni)
txtDni.grid(column=1, row=0)

lblGen= Label(marco, text="Genero").grid(column= 0,row=1, padx=5,pady=5)
txtGen= ttk.Combobox(marco,values=["M","F"], textvariable= genero)
txtGen.grid(column=1, row=1)
txtGen.current(0)

lblNombres= Label(marco, text="Nombres").grid(column= 2,row=0, padx=5,pady=5)
txtNombres= Entry(marco, textvariable= nombres)
txtNombres.grid(column=3, row=0)

lblApellidos= Label(marco, text="Apellidos").grid(column= 2,row=1, padx=5,pady=5)
txtApellidos= Entry(marco, textvariable= apellidos)
txtApellidos.grid(column=3, row=1)

lblMensaje= Label(marco, text= "Mensajes", fg="green")
lblMensaje.grid(column=0, row=2,columnspan=4)

tvEstudiantes= ttk.Treeview(marco, selectmode= NONE)
tvEstudiantes.grid(column=0, row=3, columnspan=4, padx= 5)

tvEstudiantes["columns"] = ("ID","DNI","GENERO","NOMBRES","APELLIDOS")
tvEstudiantes.column("#0",width=0, stretch=NO)
tvEstudiantes.column("ID",width=50, anchor=CENTER)
tvEstudiantes.column("DNI",width=50, anchor=CENTER)
tvEstudiantes.column("GENERO",width=55, anchor=CENTER)
tvEstudiantes.column("NOMBRES",width=100, anchor=CENTER)
tvEstudiantes.column("APELLIDOS",width=100, anchor=CENTER)

tvEstudiantes.heading("#0",text="")
tvEstudiantes.heading("ID",text="ID", anchor= CENTER)
tvEstudiantes.heading("DNI",text="DNI", anchor= CENTER)
tvEstudiantes.heading("GENERO",text="GENERO", anchor= CENTER)
tvEstudiantes.heading("NOMBRES",text="NOMBRES", anchor= CENTER)
tvEstudiantes.heading("APELLIDOS",text="APELLIDOS", anchor= CENTER)
tvEstudiantes.bind("<<TreeviewSelect>>", seleccionar)

#Botones

btnEliminar = Button(marco, text="Eliminar", command=lambda:eliminar())
btnEliminar.grid(column=1, row=4)

btnNuevo = Button(marco, text="Guardar", command=lambda:nuevo())
btnNuevo.grid(column=2, row=4)

btnModificar = Button(marco, text="Seleccionar", command=lambda:actualizar())
btnModificar.grid(column=3, row=4)



#Funciones


def modificarFalse():
    global modificar
    modificar=False
    tvEstudiantes.config(selectmode=NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvEstudiantes.config(selectmode=BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)

def validar():
    return len(dni.get()) and len(nombres.get()) and len(apellidos.get())
        


def limpiar():
    dni.set("")
    nombres.set("")
    apellidos.set("")
    

def vaciarTabla():
    filas= tvEstudiantes.get_children()
    for fila in filas:
        tvEstudiantes.delete(fila)

def llenarTabla():
    vaciarTabla()
    sql="select * from estudiantes"
    db.cursor.execute(sql)
    filas= db.cursor.fetchall()
    for fila in filas:
        id= fila[0]
        tvEstudiantes.insert("", END, id, text= id, values= fila )
def eliminar():
    id= tvEstudiantes.selection()[0]
    if int(id)>0:
        sql = "delete from estudiantes where idestudiantes=" + id
        db.cursor.execute(sql)
        db.connection.commit()
        tvEstudiantes.delete(id)
        lblMensaje.config(text="Se ha eliminado el registro correctamente")
        limpiar()
    else:
        lblMensaje.config(text="Seleccione un registro para eliminar")
def nuevo():
    if modificar == False:
        
        if validar():
            val= (dni.get(),genero.get(),nombres.get(),apellidos.get())
            sql = "insert into estudiantes(dni, genero, nombres, apellidos) values (%s,%s,%s,%s)"
            db.cursor.execute(sql, val)
            db.connection.commit()
            lblMensaje.config(text= "Se guardó un registro correctamente", fg="green")
            llenarTabla()
            limpiar()
        else:
            lblMensaje.config(text= "Los campos no deben estar vacios", fg="red")
            
    else:
        modificarFalse()
        
    
    
    
def actualizar():
    if modificar == True:
        
        if validar():
            id= tvEstudiantes.selection()[0]
            val= (dni.get(),genero.get(),nombres.get(),apellidos.get())
            sql = "update estudiantes set dni=%s, genero=%s, nombres=%s, apellidos=%s where idestudiantes=" +id
            db.cursor.execute(sql, val)
            db.connection.commit()
            lblMensaje.config(text= "Se ha actualizado un registro correctamente", fg="green")
            llenarTabla()
            limpiar()
        else:
            lblMensaje.config(text= "Los campos no deben estar vacios", fg="red")
            
    else:
        modificarTrue()


llenarTabla()
ventana.mainloop()