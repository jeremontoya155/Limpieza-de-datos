import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

class DataframeViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dataframe Viewer")
        
        self.file_path = ""
        self.dataframe = None
        self.format_selected = tk.StringVar()
        self.format_selected.set(".csv")  # Establecer CSV como formato predeterminado
        
        self.create_widgets()
    
    def create_widgets(self):
        # Botón para seleccionar archivo
        self.select_button = tk.Button(self.root, text="Seleccionar Archivo", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # Árbol para mostrar el DataFrame
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ()
        self.tree.pack(pady=5)
        
        # Botón para descargar el DataFrame
        self.download_button = tk.Button(self.root, text="Descargar DataFrame", command=self.download_dataframe)
        self.download_button.pack(pady=10)
        
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=(("All files", "*.*"),))
        if self.file_path:
            self.load_dataframe()
    
    def load_dataframe(self):
        try:
            if self.file_path.endswith('.csv'):
                self.dataframe = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xlsx', '.xls')):
                self.dataframe = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.json'):
                self.dataframe = pd.read_json(self.file_path)
            elif self.file_path.endswith('.txt'):
                self.dataframe = pd.read_csv(self.file_path, sep='\t')
            else:
                messagebox.showwarning("Formato no válido", "El archivo seleccionado no tiene un formato válido.")
                return
            
            # Limpiar árbol antes de cargar datos
            for child in self.tree.get_children():
                self.tree.delete(child)
            
            # Definir columnas del árbol
            self.tree["columns"] = tuple(self.dataframe.columns)
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            
            # Insertar datos en el árbol
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", tk.END, values=tuple(row))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el DataFrame: {str(e)}")
    
    def download_dataframe(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de descargarlo.")
            return
        
        try:
            # Diálogo para seleccionar la ubicación de guardado
            save_path = filedialog.asksaveasfilename(defaultextension=self.format_selected.get(),
                                                      filetypes=(("CSV files", "*.csv"),
                                                                 ("Excel files", "*.xlsx"),
                                                                 ("JSON files", "*.json"),
                                                                 ("Text files", "*.txt")))
            
            if save_path:
                if save_path.endswith('.csv'):
                    self.dataframe.to_csv(save_path, index=False)
                elif save_path.endswith('.xlsx'):
                    self.dataframe.to_excel(save_path, index=False)
                elif save_path.endswith('.json'):
                    self.dataframe.to_json(save_path, orient='records')
                elif save_path.endswith('.txt'):
                    self.dataframe.to_csv(save_path, sep='\t', index=False)
                else:
                    messagebox.showwarning("Formato no válido", "El formato seleccionado no es válido.")
                messagebox.showinfo("Archivo guardado", f"El archivo se ha guardado en: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar el DataFrame: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
app = DataframeViewer(root)
root.mainloop()

