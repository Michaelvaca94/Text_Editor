import sys
import textwrap
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, Label
from tkinter.filedialog import askopenfile, asksaveasfilename


class Editor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Editor de texto')
        # Configuración tañamo minimo de la ventana
        self.rowconfigure(0, minsize=600, weight=1)
        # configuración minima de la segunda columna
        self.columnconfigure(1, minsize=600, weight=1)
        # Atributo de campo de texto
        self.campo_texto = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        # Atributo de archivo
        self.archivo = None
        # Atributo para saber si ya se abrio un archivo anteriormente
        self.archivo_abierto = False
        # Creación de componentes
        self._crear_componentes()
        # Crear menú
        self._crear_menu()

    def _crear_componentes(self):
        frame_botones = tk.Frame(self, relief=tk.RAISED, bd=2)
        boton_abrir = tk.Button(frame_botones, text='Abrir', command=self._abrir_archivo)
        boton_guardar = tk.Button(frame_botones, text='Guardar', command=self._guardar)
        boton_guardar_como = tk.Button(frame_botones, text='Guardar como...', command=self._guardar_como)
        boton_dar_formato = tk.Button(frame_botones, text='\nDar formato...\n', command=self._dar_formato)
        # Los botones los expandimos de manera horizontal (sticky='WE')
        boton_abrir.grid(row=0, column=0, sticky='WE', padx=5, pady=5)
        boton_guardar.grid(row=1, column=0, sticky='WE', padx=5, pady=5)
        boton_guardar_como.grid(row=2, column=0, sticky='WE', padx=5, pady=5)
        boton_dar_formato.grid(row=5, column=0, sticky='WE', padx=5, pady=5)
        # Se coloca el frame de manera vertical
        frame_botones.grid(row=0, column=0, sticky='NS')
        # Agregamos el campo de texto, se expandirá por completo el espacio disponible que le reste
        self.campo_texto.grid(row=0, column=1, sticky='NSWE')
        # Insertamos el contenido de campo texto


    def _crear_menu(self):
        # Creamos el menú de la app
        menu_app = tk.Menu(self)
        self.config(menu=menu_app)
        # Agregamos las opciones a nuestro menú
        # Agregamos menú archivo
        menu_archivo = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Archivo', menu=menu_archivo)
        # Agregamos las opciones del menú de archivo
        menu_archivo.add_command(label='Nuevo', command=self._nuevo)
        menu_archivo.add_command(label='Abrir', command=self._abrir_archivo)
        menu_archivo.add_command(label='Guardar', command=self._guardar)
        menu_archivo.add_command(label='Guardar como...', command=self._guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Salir', command=self.quit)

        # Agregamos las opciones del menú de editar
        menu_editar = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Edición', menu=menu_editar)
        # Agregamos las opciones del menú Edición
        menu_editar.add_command(label='Cortar', accelerator='CTRL+X',
                                command=lambda: self.focus_get().event_generate("<<Cut>>"))
        menu_editar.add_command(label='Copiar', accelerator='CTRL+C',
                                command=lambda: self.focus_get().event_generate("<<Copy>>"))
        menu_editar.add_command(label='Pegar', accelerator='CTRL+V',
                                command=lambda: self.focus_get().event_generate("<<Paste>>"))
        menu_editar.add_command(label='Seleccionar todo', accelerator='CTRL+A',
                                command=lambda: self.focus_get().event_generate("<<SelectAll>>"))
        menu_editar.add_separator()
        menu_editar.add_command(label='Dar formato...', command=self._dar_formato)

        # Agregamos el menu de ayuda
        menu_ayuda = tk.Menu(menu_app, tearoff=False)
        menu_app.add_cascade(label='Ayuda', menu=menu_ayuda)
        menu_ayuda.add_command(label='Acerca de', command=self._acerca_de)


    def _abrir_archivo(self):
        # Abrimos el archivo para edición (lectura-escritura)
        self.archivo_abierto = askopenfile(mode='r+',
                                           defaultextension='txt',
                                           filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
                                           )
        # Eliminamos el texto anterior
        self.campo_texto.delete(1.0, tk.END)
        # Revisamos si hay un archivo
        if not self.archivo_abierto:
            return
        # Abrimos el archivo en modo lectura/escritura como un recurso
        with open(self.archivo_abierto.name, 'r+') as self.archivo:
            # Leemos el contenido del archivo
            texto = self.archivo.read()
            # Insertamos el contenido del archivo
            self.campo_texto.insert(1.0, texto)
            # Modificamos el título de la aplicacion
            self.title(f'*Editor texto - {self.archivo.name}')

    def _guardar(self):
        # Si ya se abrió previamente un archivo, lo sobreescribimos
        if self.archivo_abierto:
            # Salvamos el archivo (lo abrimos en modo escritura)
            with open(self.archivo_abierto.name, 'w') as self.archivo:
                # Leemos el contenido de la caja de texto
                texto = self.campo_texto.get(1.0, tk.END)
                # Escribimos el contenido al mismo archivo
                self.archivo.write(texto)
                # Cambiamos el nombre del titulo de la app
                self.title(f'Editor Texto - {self.archivo.name}')
        else:
            self._guardar_como()

    def _guardar_como(self):
        # salvamos el archivo actual como un nuevo archivo
        self.archivo = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
            )
        if not self.archivo:
            return
        # Abrimos el archivo en modo escritura (write)
        with open(self.archivo, 'w') as archivo:
            # leemos el contenido de la caja de texto
            texto = self.campo_texto.get(1.0, tk.END)
            # Escribimos el contenido al nuevo archivo
            archivo.write(texto)
            # Cambiamso el nombre del archivo
            self.title(f'Editor texto - {archivo.name}')
            # Indicamos que hemso abierto un archivo
            self.archivo_abierto = archivo

    def _dar_formato(self):
        largo_texto = self.campo_texto.get(1.0, tk.END)
        self.campo_texto.delete(1.0, tk.END)
        texto_wrapper_objeto = textwrap.TextWrapper(width=35)
        final= texto_wrapper_objeto.fill(largo_texto)
        self.campo_texto.insert(1.0, final)

    def _nuevo(self):
        texto = self.campo_texto.get(1.0, tk.END)
        if texto != '':
            valor = messagebox.askyesnocancel('Editor de texto', ' ¿Desea guardar el archivo?')
            if valor == True:
                self._guardar_como()
                self.campo_texto.delete(1.0, tk.END)
                self.destroy()
                self.quit()
                editor = Editor()
                editor.mainloop()
            elif valor == False:
                self.destroy()
                self.quit()
                editor = Editor()
                editor.mainloop()

    def _acerca_de(self):
        ventana_info = tk.Toplevel()
        ventana_info.title('Acerca de...')
        ventana_info.resizable(0,0)
        ventana_info.geometry('300x280+400+200')
        imagenL = tk.PhotoImage(file='python.png')
        Label(ventana_info, image=imagenL).place(x=23, y=15 )
        tk.Label(ventana_info, text='Programa realizado en Python \n\n con la libreria Tkinter\n\n'
                                               'Autor: Ing. Michael Vaca').place(x=65, y=120 )
        boton = tk.Button(ventana_info, text='Aceptar', command=ventana_info.destroy)
        boton.place(x=120, y=220)
        ventana_info.mainloop()

        # pyinstaller --windowed --onefile --icon=./editor2.ico editor_texto_2.py
        # pyinstaller --windowed --onefile --add-data "*.png";"." --icon=./editor2.ico editor_texto_3.py


if __name__ == '__main__':
    editor = Editor()
    editor.mainloop()
