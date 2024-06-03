import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class DataframeViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dataframe Viewer")
        
        self.file_path = ""
        self.dataframe = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Botón para seleccionar archivo
        self.select_button = tk.Button(self.root, text="Seleccionar Archivo", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # Etiqueta para mostrar el DataFrame
        self.dataframe_label = tk.Label(self.root, text="DataFrame:")
        self.dataframe_label.pack(pady=5)
        
        # Cuadro de texto para mostrar el DataFrame
        self.dataframe_text = tk.Text(self.root, height=10, width=50)
        self.dataframe_text.pack(pady=5)
        
        # Botón para descargar el DataFrame en diferentes formatos
        self.download_button = tk.Button(self.root, text="Descargar DataFrame", command=self.download_dataframe)
        self.download_button.pack(pady=10)
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"),
                                                               ("Excel files", "*.xlsx;*.xls"),
                                                               ("JSON files", "*.json"),
                                                               ("Text files", "*.txt"),
                                                               ("All files", "*.*")))
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
            
            # Mostrar el DataFrame en el cuadro de texto
            self.dataframe_text.delete(1.0, tk.END)
            self.dataframe_text.insert(tk.END, self.dataframe.to_string())
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el DataFrame: {str(e)}")
    
    def download_dataframe(self):
        if self.dataframe is None:
            messagebox.showwarning("DataFrame no cargado", "Primero debe cargar un DataFrame antes de descargarlo.")
            return
        
        try:
            # Diálogo para seleccionar la ubicación de guardado
            save_path = filedialog.asksaveasfilename(defaultextension=".csv",
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
                    self.dataframe.to_json(save_path, orient='records', lines=True)
                elif save_path.endswith('.txt'):
                    self.dataframe.to_csv(save_path, sep='\t', index=False)
                else:
                    messagebox.showwarning("Formato no válido", "El formato seleccionado no es válido.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar el DataFrame: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
app = DataframeViewer(root)
root.mainloop()
