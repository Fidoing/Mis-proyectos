from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font, ttk
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="tu_usuario",
  password="tu_contraseña",
  database="tu_base_de_datos"
)
cur = mydb.cursor()
def main():
    root = tk.Tk()
    root.title("Programita")
    root.resizable(0,0)
    root.geometry("1100x700")
    image = Image.open("menu.png")
    # Convertir la imagen a PhotoImage
    canvas = tk.Canvas(root, width=1100, height=700)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    # Crear un Label y establecer la imagen como su fondo
    canvas.pack(fill="both", expand=True)



    #MENU DEL PROGRAMA
    Titulo_frame= Frame(canvas, width=900, height=400)
    canvas.create_window(500,5, window=Titulo_frame, anchor="nw")
    Titulo_frame.grid_propagate(False)
    Titulo = Label (Titulo_frame, bg= "pink", text="LISTA DE DATOS", fg='white')
    Titulo['font'] = ('Arial', 25)
    Titulo.pack()
    
    menu = Frame (canvas, bg="#456675", width=300, height=350)
    menu.columnconfigure(0, weight=1)
    menu.columnconfigure(1, weight=1)
    menu.columnconfigure(2, weight=1)
    menu.rowconfigure(0,weight=1)
    menu.rowconfigure(1,weight=1)
    menu.rowconfigure(2,weight=1)
    menu.rowconfigure(3,weight=1)
    menu.rowconfigure(4,weight=1)
    menu.grid_propagate(False)
    canvas.create_window(10,25, window=menu, anchor="nw")
    

    subMenu = Frame (canvas, bg="grey", width=300, height=275)
    canvas.create_window(10,400, window=subMenu, anchor="nw")
    subMenu.grid_propagate(False)
    subMenu.columnconfigure(0, weight=1)
    subMenu.columnconfigure(1, weight=1)
    subMenu.columnconfigure(2, weight=1)
    subMenu.rowconfigure(0, weight=1)
    subMenu.rowconfigure(1, weight=1)
    subMenu.rowconfigure(2, weight=1)
    subMenu.rowconfigure(3, weight=1)
    subMenu.rowconfigure(4, weight=4)

    Lista = Frame (canvas, bg="#456675", width=750, height=625)
    canvas.create_window(320,50, window=Lista, anchor="nw")
    Lista.pack_propagate(False)
    tree = ttk.Treeview(Lista)
    tree["columns"] = ("one", "two", "three","four")
    tree.column("#0", width=150, minwidth=70)
    tree.column("one", width=150, minwidth=150)
    tree.column("two", width=100, minwidth=100)
    tree.column("three", width=80, minwidth=50)
    tree.column("four", width=80, minwidth=50)

    # Crear las etiquetas de las columnas
    tree.heading("#0", text="ID", anchor=tk.W)
    tree.heading("one", text="Nombre", anchor=tk.W)
    tree.heading("two", text="Descripcion", anchor=tk.W)
    tree.heading("three", text="Precio", anchor=tk.W)
    tree.heading("four", text="Cantidad", anchor=tk.W)

    def reload_BD():
        cur.execute("SELECT * FROM productos")
        Lista_BD = cur.fetchall()
        if Lista_BD is not None:
            for fila in Lista_BD:
                ID_DB = fila[0]
                NOMRE_DB = fila[1]
                DESC_DB = fila[2]
                PRECIO_DB = fila[3]
                CANT_DB = fila[4]
                tree.insert("", "end", text=ID_DB,values=(NOMRE_DB,DESC_DB, PRECIO_DB,CANT_DB))
        
    reload_BD()
 
    def alarma_digito():
        alarma.config(text="ID, Precio y Cantidad \n deben ser numeros",font=('Arial', 14))
        subMenu.after(5000, borrar_mensaje)
    def borrar_mensaje():
        alarma.config(text="")
    def mostrar_mensaje():
        alarma.config(text="Ya existe esa ID ",font=('Arial', 19))
        subMenu.after(5000, borrar_mensaje)
        
    def Insertar_productos():
        id_get= Id_entry.get()
        nombre_get = Nombre_entry.get()
        descripcion_get = Descripcion_entry.get()
        precio_get = Precio_entry.get()
        cantidad_get = Cantidad_entry.get()
        sql='''INSERT INTO productos (ID, NOMBRE, DESCRIPCION, PRECIO, CANTIDAD) 
        VALUES('{}', '{}','{}', '{}','{}')'''.format(id_get, nombre_get, descripcion_get, precio_get, cantidad_get)
        cur.execute(sql)
        mydb.commit()
        
        
    def Eliminar_datosDB(Nombre):
        sql_delete="DELETE FROM productos WHERE ID = ('{}')".format(Nombre)
        cur.execute(sql_delete)
        mydb.commit()
        

    
    def Insertar_datos():
        id_get= Id_entry.get()
        nombre_get = Nombre_entry.get()
        descripcion_get = Descripcion_entry.get()
        precio_get = Precio_entry.get()
        cantidad_get = Cantidad_entry.get()
        if (id_get.isdigit() and precio_get.isdigit() and cantidad_get.isdigit()):

            sql = "SELECT * FROM productos WHERE ID = ('{}');".format(id_get)
            cur.execute(sql)
            resultados = cur.fetchone()
            if resultados is not None:
                subMenu.after(1, mostrar_mensaje)
                valor = resultados[0]

                for item in tree.get_children():
                    name = tree.item(item, option='text')
                    id_from_mysql = int(name)
                    if (id_from_mysql == valor):
                        return 
            
            tree.insert("", "end", text=id_get,values=(nombre_get,descripcion_get, precio_get,cantidad_get))
            Insertar_productos()
        else:
            alarma_digito()
    
    def Eliminar_datos():
        selected_item = tree.selection()[0]
        selected = tree.item(selected_item, option='text')
        Eliminar_datosDB(selected)
        tree.delete(selected_item)
 

    def Limpiar_todo():
        tree.delete(*tree.get_children())
        sql= "DELETE FROM productos"
        cur.execute(sql)
        mydb.commit()
    
    def Buscar():
        criterio = entrada.get()
        for iid in tree.get_children():
            item = tree.item(iid)
            if item['values'][0].lower() == criterio.lower():
                tree.selection_set(iid)
    # Empacar el Treeview
    tree.pack(fill="both",expand=1)

    
    menu_Titulo = Label(menu, text="Añadir nuevo dato", fg='white',font=('Helvetica', 24), bg="#456675")
    menu_Titulo.grid(row=0,column=0,columnspan=3,pady=10)
    Id = tk.Label(menu, text="Id", fg='white',font=('Arial', 20), bg="#456675")
    Id.grid(row=1,column=0,pady=10)
    Nombre = tk.Label(menu, text="Nombre", fg='white',font=('Arial', 20), bg="#456675")
    Nombre.grid(row=2,column=0,pady=10)
    Descripcion = tk.Label(menu, text="Descripcion", fg='white',font=('Arial', 20), bg="#456675")
    Descripcion.grid(row=3,column=0,pady=10)
    Precio = tk.Label(menu, text="Precio", fg='white',font=('Arial', 20), bg="#456675")
    Precio.grid(row=4,column=0,pady=10)
    Cantidad = tk.Label(menu, text="Cantidad", fg='white',font=('Arial', 20), bg="#456675")
    Cantidad.grid(row=5,column=0,pady=10)
    my_font = font.Font(size=15)
    Id_entry = Entry(menu,font=my_font, width=13)
    Id_entry.grid(row=1, column=1,pady=10,rowspan=1)
    Nombre_entry = Entry(menu,font=my_font, width=13)
    Nombre_entry.grid(row=2, column=1,pady=10,rowspan=1)
    Descripcion_entry = Entry(menu,font=my_font, width=13)
    Descripcion_entry.grid(row=3, column=1,pady=10,rowspan=1)
    Precio_entry = Entry(menu,font=my_font, width=13)
    Precio_entry.grid(row=4, column=1,pady=10,rowspan=1)
    Cantidad_entry = Entry(menu,font=my_font, width=13)
    Cantidad_entry.grid(row=5, column=1,pady=10,rowspan=1)
    entrada = Entry(subMenu,font=my_font, width=13)
    entrada.grid(row=2, column=0,pady=10,rowspan=1)


    
    Texto5 = Button(subMenu, text="Agregar", fg='white',font=('Arial', 20), bg="green", command=Insertar_datos)
    Texto6 = Button(subMenu, text="Eliminar", fg='white',font=('Arial', 20), bg="red", command=Eliminar_datos)
    Texto7 = Button(subMenu, text="Limpiar", fg='white',font=('Arial', 20), bg="sky blue", command=Limpiar_todo)
    Texto8 = Button(subMenu, text="Buscar por nombre", fg='white',font=('Arial', 10), bg="violet", command=Buscar)
    Texto5.grid(row=0,column=0,pady=10)
    Texto6.grid(row=0,column=1,pady=10)
    Texto7.grid(row=1,column=0,pady=10)
    Texto8.grid(row=2,column=1,pady=10)

    # ALARMA

    alarma = Label(subMenu, text="",bg="grey")
    alarma.grid(row=3,column=0, columnspan=2,rowspan=2)

    
       
    root.mainloop()
    
    

main()