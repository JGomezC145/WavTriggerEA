# Author: Jeremy Gomez (JGomezC145)
# Description: Renames files in a folder with a base name and a number

import tkinter as tk
from tkinter import filedialog
import os
import shutil

class SoundRenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sound Renamer")
        self.geometry("800x500")

        # el fondo de la ventana es de color indigo
        self.config(bg="#4B0082")

        # detecta cuando se presione la tecla ESC y cierra la ventana
        self.bind("<Escape><Escape>", lambda event: self.destroy())
        self.bind("a", lambda event: self.select_files())
        self.bind("<Insert>", lambda event: self.select_files())
        self.bind("<Control-o>", lambda event: self.select_files())
        self.bind("<Control-e>", lambda event: self.set_destination_folder())
        self.bind("<Control-s>", lambda event: self.set_destination_folder())
        self.bind("<Control-r>", lambda event: self.rename_files())
        self.bind("<Control-q>", lambda event: self.destroy())
        #Cuando se presione enter se ejectuta la funcion rename_files
        self.bind("<Return>", lambda event: self.rename_files())
        #Cuando se presione control+enter se ejecuta la funcion rename_files
        self.bind("<Control-Return>", lambda event: self.rename_files())
        #Cuando se presione Delete se vacia la lista de archivos
        self.bind("<Delete>", lambda event: self.clear_file_list())

        self.file_list = []
        self.destination_folder = ""
        
        self.create_widgets()

    def create_widgets(self):

        # Etiqueta para mostrar la lista de archivos seleccionados alineado a la izquierda
        self.file_list_label = tk.Label(self, text="Archivos seleccionados:", bg="#4B0082", fg="white")
        self.file_list_label.pack(anchor=tk.W, padx=5, pady=5)

        # Listbox para mostrar la lista de archivos seleccionados
        self.file_listbox = tk.Listbox(self, bg="#4B0082", fg="white", selectbackground="green", selectforeground="white", selectmode=tk.EXTENDED)
        self.file_listbox.bind("<Double-Button-1>", self.delete_file)
        self.file_listbox.bind("<Delete>", self.delete_file)
        self.file_listbox.bind("<BackSpace>", self.delete_file)
        # self.file_listbox.bind("<Return>", self.delete_file)
        self.file_listbox.bind("<space>", self.play_file)


        self.file_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Botón para seleccionar archivos
        self.select_files_button = tk.Button(self, text="Seleccionar archivos", cursor="hand2", command=self.select_files, bg="green", fg="white")
        self.select_files_button.pack(pady=10, padx=5, fill=tk.X)

        # Botón para seleccionar carpeta de destino
        self.select_folder_button = tk.Button(self, text="Seleccionar carpeta de destino", cursor="hand2", command=self.set_destination_folder, bg="green", fg="white")
        self.select_folder_button.pack(pady=10, fill=tk.X)

        # Etiqueta para mostrar la carpeta de destino seleccionada
        self.destination_folder_label = tk.Label(self, text="Carpeta de destino aun no definida", bg="#4B0082", fg="white")
        self.destination_folder_label.pack(pady=5, padx=5, fill=tk.X)

        
        
        # Campo de texto para ingresar el nombre base de los archivos
        self.base_name_label = tk.Label(self, text="Nombre base:", bg="#4B0082", fg="white")
        self.base_name_label.pack()
        self.base_name_entry = tk.Entry(self)
        self.base_name_entry.pack(pady=5)
        
        # Botón para renombrar y guardar los archivos
        self.rename_button = tk.Button(self, text="Renombrar y guardar", cursor="hand2", command=self.rename_files, bg="green", fg="white")
        self.rename_button.pack(pady=10)
        
        # Etiqueta para mostrar el resultado del proceso
        self.result_label = tk.Label(self, text="", bg="#4B0082", fg="white")
        self.result_label.pack()


    def clear_file_list(self):
        self.file_list = []
        self.update_file_listbox()

    def delete_file(self, event):
        # obtiene el índice del elemento seleccionado
        index = self.file_listbox.curselection()[0]
        # elimina el elemento de la lista de archivos
        self.file_list.pop(index)
        # actualiza el listbox
        self.update_file_listbox()

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Sonidos al WAVTrigger", "*.wav")])
        if files:
            # añade los archivos seleccionados a la lista de archivos
            self.file_list.extend(files)

        self.update_file_listbox()

    def set_destination_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder = folder
            self.destination_folder_label.config(text="Carpeta de destino: {}".format(self.destination_folder), fg="green")

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.file_list:
            self.file_listbox.insert(tk.END, file_path)
    
    def play_file(self, event):
        index = self.file_listbox.curselection()[0]
        file_path = self.file_list[index]
        os.startfile(file_path)
        

        
    def rename_files(self):
        base_name = self.base_name_entry.get().strip()
        


        
        """ if not base_name:
            self.result_label.config(text="Ingrese un nombre base válido")
            return """
        
        if not self.file_list:
            self.result_label.config(text="No se han seleccionado archivos")
            return
        
        if not self.destination_folder:
            self.destination_folder_label.config(text="--Debes seleccionar una carpeta de destino--", fg="red")
            return
        
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)
        
        count = 1
        for file_path in self.file_list:
            if not file_path.lower().endswith(".wav"):
                self.result_label.config(text="Error: El archivo {} no es un archivo WAV".format(file_path))
                continue

            # obtiene el nombre del archivo sin la extensión
            file_name = os.path.basename(file_path)
            file_name_without_extension = os.path.splitext(file_name)[0]

            new_name = "{:03d}_{}_{}.wav".format(count, base_name, file_name_without_extension) if base_name else "{:03d}_{}.wav".format(count, file_name_without_extension)
                
            
            destination_path = os.path.join(self.destination_folder, new_name)
            shutil.copyfile(file_path, destination_path)
            
            count += 1
        
        self.result_label.config(text="Archivos renombrados y guardados correctamente")
        

if __name__ == "__main__":
    app = SoundRenamerApp()
    app.mainloop()

