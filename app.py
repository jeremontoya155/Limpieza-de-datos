import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from sklearn import preprocessing
from datetime import datetime

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
        
        # Botón para eliminar duplicados de la columna seleccionada
        self.remove_duplicates_button = tk.Button(self.root, text="Eliminar Duplicados", command=self.remove_duplicates)
        self.remove_duplicates_button.pack(pady=5)
        
        # Botón para normalizar los datos de la columna seleccionada
        self.normalize_button = tk.Button(self.root, text="Normalizar Datos", command=self.normalize_data)
        self.normalize_button.pack(pady=5)
        
        # Botón para manejar valores nulos
        self.handle_nulls_button = tk.Button(self.root, text="Manejar Valores Nulos", command=self.handle_nulls)
        self.handle_nulls_button.pack(pady=5)
        
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
    
    def remove_duplicates(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de eliminar duplicados.")
            return
        
        try:
            # Obtener la columna seleccionada
            column_name = self.column_menu.get()
            
            # Eliminar los duplicados y mantener solo los valores únicos en la columna seleccionada
            unique_df = self.dataframe.drop_duplicates(subset=[column_name])
            
            # Mostrar el DataFrame con los valores únicos
            self.show_dataframe(unique_df)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los duplicados: {str(e)}")
    
    def show_dataframe(self, dataframe):
        # Limpiar árbol antes de cargar datos
        for child in self.tree.get_children():
            self.tree.delete(child)
        
        # Definir nuevas columnas del árbol
        self.tree["columns"] = tuple(dataframe.columns)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Insertar datos en el árbol
        for index, row in dataframe.iterrows():
            self.tree.insert("", tk.END, values=tuple(row))
    
    def normalize_data(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de normalizar los datos.")
            return
        
        # Obtener la columna seleccionada
        column_name = self.column_menu.get()
        
        # Menú desplegable para seleccionar el tipo de normalización
        normalize_options = ["Convertir a Float", "Convertir a Int", "Convertir a Fecha Corta", "Convertir a Fecha Larga"]
        selected_option = tk.StringVar()
        selected_option.set(normalize_options[0])  # Establecer la opción predeterminada
        
        # Función para realizar la normalización
        def apply_normalization():
            option = selected_option.get()
            if option == "Convertir a Float":
                self.convert_to_float(column_name)
            elif option == "Convertir a Int":
                self.convert_to_int(column_name)
            elif option == "Convertir a Fecha Corta":
                self.convert_to_short_date(column_name)
            elif option == "Convertir a Fecha Larga":
                self.convert_to_long_date(column_name)
            normalization_dialog.destroy()
        
        # Cuadro de diálogo para seleccionar la opción de normalización
        normalization_dialog = tk.Toplevel(self.root)
        normalization_dialog.title("Normalizar Datos")
        
        option_label = tk.Label(normalization_dialog, text="Seleccione una opción de normalización:")
        option_label.pack()
        
        option_menu = tk.OptionMenu(normalization_dialog, selected_option, *normalize_options)
        option_menu.pack()
        
        apply_button = tk.Button(normalization_dialog, text="Aplicar", command=apply_normalization)
        apply_button.pack()

    def convert_to_float(self, column_name):
        try:
            self.dataframe[column_name] = self.dataframe[column_name].astype(float)
            self.update_treeview()
        except ValueError as e:
            messagebox.showerror("Error de conversión", f"No se pudo convertir la columna '{column_name}' a tipo float: {e}")

    def convert_to_int(self, column_name):
        try:
            self.dataframe[column_name] = self.dataframe[column_name].astype(float).astype(int)
            self.update_treeview()
        except ValueError as e:
            messagebox.showerror("Error de conversión", f"No se pudo convertir la columna '{column_name}' a tipo int: {e}")

    def convert_to_short_date(self, column_name):
        try:
            self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name]).dt.strftime("%m/%d/%Y")
            self.update_treeview()
        except ValueError as e:
            messagebox.showerror("Error de conversión", f"No se pudo convertir la columna '{column_name}' a fecha corta: {e}")

    def convert_to_long_date(self, column_name):
        try:
            self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name]).dt.strftime("%B %d, %Y")
            self.update_treeview()
        except ValueError as e:
            messagebox.showerror("Error de conversión", f"No se pudo convertir la columna '{column_name}' a fecha larga: {e}")

    def handle_nulls(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de manejar los valores nulos.")
            return
        
        # Obtener la columna seleccionada
        column_name = self.column_menu.get()
        
        # Menú desplegable para seleccionar cómo manejar los valores nulos
        handle_options = ["Eliminar Filas con Nulos", "Rellenar con un Valor", "Dejar Nulos"]
        selected_option = tk.StringVar()
        selected_option.set(handle_options[0])  # Establecer la opción predeterminada
        
        # Función para manejar los valores nulos
        def apply_handle_nulls():
            option = selected_option.get()
            if option == "Eliminar Filas con Nulos":
                self.dataframe = self.dataframe.dropna(subset=[column_name])
            elif option == "Rellenar con un Valor":
                fill_value = simpledialog.askstring("Rellenar con un Valor", f"Ingrese el valor con el cual desea rellenar los nulos en '{column_name}':")
                self.dataframe[column_name] = self.dataframe[column_name].fillna(fill_value)
            elif option == "Dejar Nulos":
                pass
            self.update_treeview()
            handle_nulls_dialog.destroy()
        
        # Cuadro de diálogo para seleccionar la opción de manejo de nulos
        handle_nulls_dialog = tk.Toplevel(self.root)
        handle_nulls_dialog.title("Manejar Valores Nulos")
        
        option_label = tk.Label(handle_nulls_dialog, text="Seleccione una opción para manejar los valores nulos:")
        option_label.pack()
        
        option_menu = tk.OptionMenu(handle_nulls_dialog, selected_option, *handle_options)
        option_menu.pack()
        
        apply_button = tk.Button(handle_nulls_dialog, text="Aplicar", command=apply_handle_nulls)
        apply_button.pack()
    
    def update_treeview(self):
        # Limpiar árbol antes de cargar datos
        for child in self.tree.get_children():
            self.tree.delete(child)
        
        # Insertar datos en el árbol
        for index, row in self.dataframe.iterrows():
            self.tree.insert("", tk.END, values=tuple(row))
    
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
