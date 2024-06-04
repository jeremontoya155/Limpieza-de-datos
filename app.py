import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class DataframeViewer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dataframe Viewer")
        self.geometry("800x600")

        self.file_path = ""
        self.dataframe = None
        self.format_selected = ctk.StringVar(value=".csv")

        self.create_widgets()

    def create_widgets(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(12, weight=1)

        self.select_button = ctk.CTkButton(self.sidebar_frame, text="Seleccionar Archivo", command=self.select_file)
        self.select_button.grid(row=0, column=0, padx=20, pady=10)

        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=2, sticky="ns")

        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.column_label = ctk.CTkLabel(self.sidebar_frame, text="Seleccionar Columna:")
        self.column_label.grid(row=1, column=0, padx=20, pady=10)

        self.column_menu = ctk.CTkComboBox(self.sidebar_frame)
        self.column_menu.grid(row=2, column=0, padx=20, pady=10)

        self.delete_button = ctk.CTkButton(self.sidebar_frame, text="Eliminar Columna", command=self.delete_column)
        self.delete_button.grid(row=3, column=0, padx=20, pady=10)

        self.filter_label = ctk.CTkLabel(self.sidebar_frame, text="Filtrar por Cantidad:")
        self.filter_label.grid(row=4, column=0, padx=20, pady=10)

        self.filter_entry = ctk.CTkEntry(self.sidebar_frame)
        self.filter_entry.grid(row=5, column=0, padx=20, pady=10)

        self.filter_button = ctk.CTkButton(self.sidebar_frame, text="Aplicar Filtro", command=self.apply_filter)
        self.filter_button.grid(row=6, column=0, padx=20, pady=10)

        self.remove_duplicates_button = ctk.CTkButton(self.sidebar_frame, text="Eliminar Duplicados", command=self.remove_duplicates)
        self.remove_duplicates_button.grid(row=7, column=0, padx=20, pady=10)

        self.normalize_button = ctk.CTkButton(self.sidebar_frame, text="Normalizar Datos", command=self.normalize_data)
        self.normalize_button.grid(row=8, column=0, padx=20, pady=10)

        self.handle_nulls_button = ctk.CTkButton(self.sidebar_frame, text="Manejar Valores Nulos", command=self.handle_nulls)
        self.handle_nulls_button.grid(row=9, column=0, padx=20, pady=10)

        self.download_button = ctk.CTkButton(self.sidebar_frame, text="Descargar DataFrame", command=self.download_dataframe)
        self.download_button.grid(row=10, column=0, padx=20, pady=10)

        self.format_menu = ctk.CTkComboBox(self.sidebar_frame, values=[".csv", ".xlsx", ".json", ".txt"], variable=self.format_selected)
        self.format_menu.grid(row=11, column=0, padx=20, pady=10)

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

            self.update_treeview()

            self.column_menu.configure(values=list(self.dataframe.columns))
            self.column_menu.set(list(self.dataframe.columns)[0])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el DataFrame: {str(e)}")

    def apply_filter(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de aplicar el filtro.")
            return

        try:
            column_name = self.column_menu.get()
            filter_value = self.filter_entry.get()
            if not filter_value:
                messagebox.showwarning("Valor no especificado", "Por favor ingrese un valor para aplicar el filtro.")
                return

            filter_value = float(filter_value)

            self.dataframe = self.dataframe[self.dataframe[column_name] == filter_value]

            self.update_treeview()

        except ValueError:
            messagebox.showwarning("Valor no válido", "Por favor ingrese un valor numérico para aplicar el filtro.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aplicar el filtro: {str(e)}")

    def delete_column(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de eliminar una columna.")
            return

        try:
            column_name = self.column_menu.get()
            self.dataframe.drop(columns=[column_name], inplace=True)
            self.update_treeview()

            self.column_menu.configure(values=list(self.dataframe.columns))
            self.column_menu.set(list(self.dataframe.columns)[0])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la columna: {str(e)}")

    def remove_duplicates(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de eliminar duplicados.")
            return

        try:
            column_name = self.column_menu.get()
            self.dataframe.drop_duplicates(subset=[column_name], inplace=True)
            self.update_treeview()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los duplicados: {str(e)}")

    def normalize_data(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de normalizar los datos.")
            return

        column_name = self.column_menu.get()
        normalize_options = ["Convertir a Float", "Convertir a Int", "Convertir a Fecha Corta", "Convertir a Fecha Larga"]
        selected_option = ctk.StringVar(value=normalize_options[0])

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

        normalization_dialog = ctk.CTkToplevel(self)
        normalization_dialog.title("Normalizar Datos")

        option_label = ctk.CTkLabel(normalization_dialog, text="Seleccione una opción de normalización:")
        option_label.pack(pady=10)

        option_menu = ctk.CTkComboBox(normalization_dialog, values=normalize_options, variable=selected_option)
        option_menu.pack(pady=10)

        apply_button = ctk.CTkButton(normalization_dialog, text="Aplicar", command=apply_normalization)
        apply_button.pack(pady=10)

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
            self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format='%Y-%m-%d').dt.date
            self.update_treeview()
        except Exception as e:
            messagebox.showerror("Error de conversión", f"No se pudo convertir la columna '{column_name}' a fecha corta: {e}")


    def convert_to_long_date(self, column_name):
        try:
            self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format='%Y-%m-%d %H:%M:%S')
            self.update_treeview()
        except Exception as e:
            messagebox.showerror("Error de conversión", f"No se pudo convertir la columna '{column_name}' a fecha larga: {e}")

    def handle_nulls(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de manejar los valores nulos.")
            return

        handle_nulls_options = ["Eliminar Filas con Valores Nulos", "Llenar Valores Nulos con 0", "Llenar Valores Nulos con Promedio"]
        selected_option = ctk.StringVar(value=handle_nulls_options[0])

        def apply_handling():
            option = selected_option.get()
            if option == "Eliminar Filas con Valores Nulos":
                self.drop_null_rows()
            elif option == "Llenar Valores Nulos con 0":
                self.fill_null_with_zero()
            elif option == "Llenar Valores Nulos con Promedio":
                self.fill_null_with_mean()
            handling_dialog.destroy()

        handling_dialog = ctk.CTkToplevel(self)
        handling_dialog.title("Manejar Valores Nulos")

        option_label = ctk.CTkLabel(handling_dialog, text="Seleccione una opción de manejo de valores nulos:")
        option_label.pack(pady=10)

        option_menu = ctk.CTkComboBox(handling_dialog, values=handle_nulls_options, variable=selected_option)
        option_menu.pack(pady=10)

        apply_button = ctk.CTkButton(handling_dialog, text="Aplicar", command=apply_handling)
        apply_button.pack(pady=10)

    def drop_null_rows(self):
        try:
            self.dataframe.dropna(inplace=True)
            self.update_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar las filas con valores nulos: {e}")

    def fill_null_with_zero(self):
        try:
            self.dataframe.fillna(0, inplace=True)
            self.update_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron llenar los valores nulos con cero: {e}")

    def fill_null_with_mean(self):
        try:
            self.dataframe.fillna(self.dataframe.mean(), inplace=True)
            self.update_treeview()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron llenar los valores nulos con el promedio: {e}")

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if self.dataframe is not None:
            self.tree["column"] = list(self.dataframe.columns)
            self.tree["show"] = "headings"

            for column in self.tree["column"]:
                self.tree.heading(column, text=column)

            dataframe_rows = self.dataframe.to_numpy().tolist()
            for row in dataframe_rows:
                self.tree.insert("", "end", values=row)

    def download_dataframe(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de descargarlo.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=self.format_selected.get(), filetypes=[("Archivos de datos", "*" + self.format_selected.get())])
        if save_path:
            try:
                if self.format_selected.get() == ".csv":
                    self.dataframe.to_csv(save_path, index=False)
                elif self.format_selected.get() == ".xlsx":
                    self.dataframe.to_excel(save_path, index=False)
                elif self.format_selected.get() == ".json":
                    self.dataframe.to_json(save_path, orient="records")
                elif self.format_selected.get() == ".txt":
                    self.dataframe.to_csv(save_path, sep='\t', index=False)

                messagebox.showinfo("Descarga Exitosa", "El DataFrame se ha descargado exitosamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo descargar el DataFrame: {e}")

if __name__ == "__main__":
    app = DataframeViewer()
    app.mainloop()
