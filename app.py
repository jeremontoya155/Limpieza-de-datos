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
        # Crear un Notebook para las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Agregar la primera pestaña para la visualización del DataFrame
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Visualización")
        
        # Botón para seleccionar archivo en la primera pestaña
        self.select_button = tk.Button(self.tab1, text="Seleccionar Archivo", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # Árbol para mostrar el DataFrame en la primera pestaña
        self.tree = ttk.Treeview(self.tab1)
        self.tree["columns"] = ()
        self.tree.pack(pady=5)
        
        # Agregar la segunda pestaña para la edición y filtrado del DataFrame
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Edición y Filtrado")
        
        # Etiqueta y entrada para seleccionar columna en la segunda pestaña
        self.column_label = tk.Label(self.tab2, text="Seleccionar Columna:")
        self.column_label.pack()
        self.column_entry = tk.Entry(self.tab2)
        self.column_entry.pack()
        
        # Etiqueta y entrada para filtrar por cantidad en la segunda pestaña
        self.filter_label = tk.Label(self.tab2, text="Filtrar por Cantidad:")
        self.filter_label.pack()
        self.filter_entry = tk.Entry(self.tab2)
        self.filter_entry.pack()
        
        # Botón para aplicar filtro en la segunda pestaña
        self.filter_button = tk.Button(self.tab2, text="Aplicar Filtro", command=self.apply_filter)
        self.filter_button.pack()
        
        # Botón para descargar el DataFrame en la segunda pestaña
        self.download_button = tk.Button(self.tab2, text="Descargar DataFrame", command=self.download_dataframe)
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
            
            # Limpiar árbol antes de cargar datos en la primera pestaña
            for child in self.tree.get_children():
                self.tree.delete(child)
            
            # Definir columnas del árbol en la primera pestaña
            self.tree["columns"] = tuple(self.dataframe.columns)
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            
            # Insertar datos en el árbol en la primera pestaña
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", tk.END, values=tuple(row))
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el DataFrame: {str(e)}")
    
    def apply_filter(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de aplicar el filtro.")
            return
        
        try:
            # Obtener la columna y el valor del filtro
            column_name = self.column_entry.get()
            if not column_name:
                messagebox.showwarning("Columna no especificada", "Por favor ingrese el nombre de la columna.")
                return
            
            filter_value = self.filter_entry.get()
            if not filter_value:
                messagebox.showwarning("Valor no especificado", "Por favor ingrese un valor para aplicar el filtro.")
                return
            
            filter_value = float(filter_value)  # Convertir a float para comparación
            
            # Aplicar filtro
            self.dataframe = self.dataframe[self.dataframe[column_name] == filter_value]
            
            # Limpiar árbol antes de cargar datos en la primera pestaña
            for child in self.tree.get_children():
                self.tree.delete(child)
            
            # Definir columnas del árbol en la primera pestaña
            self.tree["columns"] = tuple(self.dataframe.columns)
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            
            # Insertar datos en el árbol en la primera pestaña
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", tk.END, values=tuple(row))
            
        except ValueError:
            messagebox.showwarning("Valor no válido", "Por favor ingrese un valor numérico para aplicar el filtro.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el filtro: {str(e)}")
    
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


