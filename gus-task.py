# ---- GESTOR DE TAREAS ----    | ---- TASK MANAGER ---- 
# - Agregar nuevas tareas       | - Add new tasks
# - Modificar tareas anteriores | - Modify previus tasks
# - Marcar tareas finalizadas   | - Mark finished tasks
# - Eliminar tareas             | - Delete tasks


from tkinter import *
import sqlite3

root = Tk()
root.title('Tareas')
root.geometry('500x500')
root.config(bg='#BCC2C0')



# -------------------------------------------------- VARIABLES GLOBALES
completado = ''
color = '#2C323C'



# -------------------------------------------------- BASE DE DATOS BBDD

# conexión a base de datos / BBDD conexion
conex = sqlite3.connect('task.db')

# creación del cursor / cursor creation
c = conex.cursor()



# -------------- creación de la tabla de BBDD ----- BBDD table creation
# campo 1 => identificador del registro en la BBDD [tarea]
# campo 2 => creación, fecha de creación de la tarea, capta momento exacto
# campo 3 => descripción, texto que introduce user explicando la tarea
# campo 4 => completado, booleano que mostrará status de la tarea

c.execute("""
        CREATE TABLE if not exists tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        descripcion TEXT NOT NULL,
        completado BOOLEAN NOT NULL
    );
    """)

# ejecución de la instrucción c.execute
conex.commit()



# ----------------------------------------------- FUNCIONES - FUNCTIONS

# -----------------------------------eliminar tareas ----- delete tasks 
def remove1(id):
    """
    Función que elimina las tareas según su identificador id, actualizando 
    la base de datos y hace un renderizado automático de la interfaz

    Args:
        id (int): identificador de la tarea - autoincrement bbdd

    Returns:
        Eliminación de la tarea de la base de datos y de la interfaz
    """
    def remove2():
        c.execute("DELETE FROM tareas WHERE id = ?", (id, ))
        conex.commit()
        mostrar()

    return remove2



# ------------------------ tareas completadas ----- mark finished tasks 
def marcados1(id):
    """
    Función que marca las tareas completadas, actualizando la base de
    datos y realizando un renderizado de interfaz automático
    currying => retrasar la ejecución de una función anidandola dentro de otra

    Args: 
        id (int): identificador de la tarea - autoincrement bbdd

    Returns:
        Tarea marcada y cambio de color de texto
    """
    def marcados2():
        tarea = c.execute("SELECT * FROM tareas WHERE id = ?", (id,)).fetchone()
        c.execute("UPDATE tareas SET completado = ? WHERE id = ?", (not tarea[3], id))
        conex.commit()
        mostrar()
    return marcados2



# -------------renderizar las tareas [mostrar todas] ----- render tasks 
def mostrar():
    """
    Función que renderiza y actualiza el status de las tareas

    Args:
        None

    Returns:
        Actualización de status de tareas en interfaz
    """

    global completado
    global color
    rows = c.execute("SELECT * FROM tareas").fetchall()   # genera lista de tuplas
    for widget in frame.winfo_children():   # elimina los elementos de la pantalla 
        widget.destroy()
    for i in range(0, len(rows)):
        id = rows[i][0]
        completado = rows[i][3]   # en la tupla indice 3
        descripcion = rows[i][2]
        color = '#8E8E99' if completado else '#2C323C'
        l = Checkbutton(frame, text=descripcion, fg=color, width=60, anchor='w', bg='#BCC2C0', command=marcados1(id))
        l.grid(row=i, column=0, sticky='w')
        be = Button(frame, text='×', bg='#BCC2C0', fg='#FF5F00', bd=0, padx=5, command=remove1(id))
        be.grid(row=i, column=1)
        l.select() if completado else l.deselect()



# ---------------------------- agregar nueva tarea ----- add a new task
def agregar_tarea():
    """
    Función para agregar tareas a la bbdd y actualizar la interfaz

    Args:
        None

    Returns: 
        Tarea agregada
    """
    tarea = e.get()
    if tarea:
        c.execute("""
        INSERT INTO tareas (descripcion, completado) VALUES (?,?)""", (tarea, False))
        conex.commit()
        e.delete(0, END)
        mostrar()
    else:
        pass



# ------------------ INTERFAZ GRÁFICA ------------- GRAPHICAL INTERFACE

esp1 = Label(root, text=' ', bg='#BCC2C0')
esp1.grid(row=0, column=0)

l = Label(root, text='Tarea >', fg='#2C323C', bg='#BCC2C0', padx=3)
l.grid(row=1, column=0, padx=3, pady=3)

e = Entry(root, width=64, bg='#BCC2C0', fg='#2C323C', insertbackground="#2C323C", bd=0)
e.grid(row=1, column=1, padx=3, pady=3)
# insertbackground da color al cursor de escritura

b = Button(root, text='✚', bg='#FF5F00', fg='#ffffff', bd=0, padx=3, command=agregar_tarea)
b.grid(row=1, column=2, padx=3, pady=3)

esp2 = Label(root, text=' ', bg='#BCC2C0')
esp2.grid(row=2, column=0)

frame = LabelFrame(root, text='Mis tareas', bg='#BCC2C0', fg='#2C323C', pady=5, padx=5)
frame.grid(row=3, column=0, columnspan=3, sticky='nswe', padx=5)


e.focus()   # coloca el cursor automáticamente en el entry / cursor on entry
root.bind('<Return>', lambda x: agregar_tarea())

# bind permite usar el intro por teclado para agregar una tarea
mostrar()
root.mainloop()
