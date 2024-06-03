import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

class DataframeViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dataframe Viewer")
        # Obtener el ancho y alto de la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calcular las coordenadas x e y para que la ventana esté centrada
        x = (screen_width - 500) // 2
        y = (screen_height - 600) // 2

        # Definir la geometría de la ventana
        root.geometry("500x600+{}+{}".format(x, y))

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
        self.tree.pack(pady=5, fill="both", expand=True)
        
        # Agregar una barra de desplazamiento al Treeview
        self.tree_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        
  
        
        # Etiqueta y menú desplegable para seleccionar columna
        self.column_label = tk.Label(self.root, text="Seleccionar Columna:")
        self.column_label.pack()
        self.column_menu = ttk.Combobox(self.root, state="readonly")
        self.column_menu.pack()
        
        # Botón para eliminar la columna seleccionada
        self.delete_button = tk.Button(self.root, text="Eliminar Columna", command=self.delete_column)
        self.delete_button.pack(pady=5)
        
        # Etiqueta y entrada para filtrar por cantidad
        self.filter_label = tk.Label(self.root, text="Filtrar por Cantidad:")
        self.filter_label.pack()
        self.filter_entry = tk.Entry(self.root)
        self.filter_entry.pack()
        
        # Botón para aplicar filtro
        self.filter_button = tk.Button(self.root, text="Aplicar Filtro", command=self.apply_filter)
        self.filter_button.pack(pady=5)
        
        # Botón para descargar el DataFrame
        self.download_button = tk.Button(self.root, text="Descargar DataFrame", command=self.download_dataframe)
        self.download_button.pack(pady=10)
        
        # Menú desplegable para seleccionar el formato de descarga
        self.format_menu = ttk.Combobox(self.root, state="readonly", textvariable=self.format_selected)
        
        self.format_menu["values"] = [".csv", ".xlsx", ".json", ".txt"]
        self.format_menu.pack(pady=10)
    
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
            self.tree["show"] = "headings"
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)
            
            # Insertar datos en el árbol
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", tk.END, values=tuple(row))
            
            # Actualizar menú desplegable de columnas
            self.column_menu["values"] = self.tree["columns"]
            self.column_menu.current(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el DataFrame: {str(e)}")
    
    def save_edit(self, event):
        selected_item = self.tree.selection()[0]
        selected_column = self.column_menu.get()
        column_index = self.tree["columns"].index(selected_column)
        
        new_value = self.edit_entry.get()
        self.tree.set(selected_item, column=selected_column, value=new_value)
        
        row_index = self.tree.index(selected_item)
        self.dataframe.at[row_index, selected_column] = new_value
    
    def apply_filter(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de aplicar el filtro.")
            return
        
        try:
            # Obtener la columna y el valor del filtro
            column_name = self.column_menu.get()
            filter_value = self.filter_entry.get()
            if not filter_value:
                messagebox.showwarning("Valor no especificado", "Por favor ingrese un valor para aplicar el filtro.")
                return
            
            filter_value = float(filter_value)  # Convertir a float para comparación
            
            # Aplicar filtro
            self.dataframe = self.dataframe[self.dataframe[column_name] == filter_value]
            
            # Limpiar árbol antes de cargar datos
            for child in self.tree.get_children():
                self.tree.delete(child)
            
            # Insertar datos filtrados en el árbol
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", tk.END, values=tuple(row))
            
        except ValueError:
            messagebox.showwarning("Valor no válido", "Por favor ingrese un valor numérico para aplicar el filtro.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el filtro: {str(e)}")
    
    def delete_column(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de eliminar una columna.")
            return
        
        try:
            # Obtener la columna seleccionada
            column_name = self.column_menu.get()
            
            # Eliminar la columna
            self.dataframe.drop(columns=[column_name], inplace=True)
            
            # Limpiar árbol antes de cargar datos
            for child in self.tree.get_children():
                self.tree.delete(child)
            
            # Definir nuevas columnas del árbol
            self.tree["columns"] = tuple(self.dataframe.columns)
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)
            
            # Insertar datos en el árbol
            for index, row in self.dataframe.iterrows():
                self.tree.insert("", tk.END, values=tuple(row))
            
            # Actualizar menú desplegable de columnas
            self.column_menu["values"] = self.tree["columns"]
            self.column_menu.current(0)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la columna: {str(e)}")
    
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
