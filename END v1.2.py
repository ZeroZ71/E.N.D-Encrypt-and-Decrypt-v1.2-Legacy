import os
import tkinter as tk
from tkinter import filedialog, messagebox

def seleccionar_archivo(titulo='Selecciona un archivo'):
    return filedialog.askopenfilename(title=titulo)

def seleccionar_directorio(titulo='Selecciona un directorio'):
    return filedialog.askdirectory(title=titulo)

def encriptar(archivo_entrada, carpeta_salida):
    try:
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

        nombre_archivo = os.path.basename(archivo_entrada)
        archivo_salida = os.path.join(carpeta_salida, nombre_archivo + '.enc')

        with open(archivo_entrada, 'rb') as f:
            datos = f.read()
        resultado = ''.join(format(byte, '08b') for byte in datos)

        with open(archivo_salida, 'w') as f:
            f.write(resultado)
        return archivo_salida
    except Exception as e:
        messagebox.showerror("Error", f"Error al encriptar: {e}")
        return None

def desencriptar(archivo_entrada, carpeta_salida):
    try:
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

        nombre_archivo = os.path.basename(archivo_entrada)
        if nombre_archivo.endswith('.enc'):
            nombre_archivo = nombre_archivo[:-4]  # quitar extensión .enc

        archivo_salida = os.path.join(carpeta_salida, nombre_archivo)

        with open(archivo_entrada, 'r') as f:
            bits_str = f.read()
        if len(bits_str) % 8 != 0:
            messagebox.showerror("Error", "Archivo binario incompleto, no múltiplo de 8 bits.")
            return None

        bytes_array = bytearray(int(bits_str[i:i+8], 2) for i in range(0, len(bits_str), 8))

        with open(archivo_salida, 'wb') as f:
            f.write(bytes_array)
        return archivo_salida
    except Exception as e:
        messagebox.showerror("Error", f"Error al desencriptar: {e}")
        return None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Encriptador / Desencriptador de Archivos")
        self.geometry("1280x720")
        self.resizable(False, False)

        self.opcion = tk.StringVar(value="1")

        # Crear widgets
        tk.Label(self, text="Seleccione una opción:").pack(pady=10)

        tk.Radiobutton(self, text="Encriptar archivo", variable=self.opcion, value="1").pack(anchor='w', padx=20)
        tk.Radiobutton(self, text="Desencriptar archivo", variable=self.opcion, value="2").pack(anchor='w', padx=20)
    
        self.btn_seleccionar_archivo = tk.Button(self, text="Seleccionar archivo", command=self.seleccionar_archivo)
        self.btn_seleccionar_archivo.pack(pady=10)

        self.label_archivo = tk.Label(self, text="Archivo seleccionado: Ninguno")
        self.label_archivo.pack()

        self.btn_seleccionar_carpeta = tk.Button(self, text="Seleccionar carpeta destino", command=self.seleccionar_carpeta)
        self.btn_seleccionar_carpeta.pack(pady=10)

        self.label_carpeta = tk.Label(self, text="Carpeta destino: Ninguna")
        self.label_carpeta.pack()

        self.btn_ejecutar = tk.Button(self, text="Ejecutar", command=self.ejecutar)
        self.btn_ejecutar.pack(pady=15)

        self.archivo_entrada = None
        self.carpeta_salida = None

    def seleccionar_archivo(self):
        archivo = seleccionar_archivo("Seleccione el archivo")
        if archivo:
            self.archivo_entrada = archivo
            self.label_archivo.config(text=f"Archivo seleccionado: {os.path.basename(archivo)}")

    def seleccionar_carpeta(self):
        carpeta = seleccionar_directorio("Seleccione carpeta destino")
        if carpeta:
            self.carpeta_salida = carpeta
            self.label_carpeta.config(text=f"Carpeta destino: {carpeta}")

    def ejecutar(self):
        if not self.archivo_entrada:
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo.")
            return
        if not self.carpeta_salida:
            messagebox.showwarning("Advertencia", "Debe seleccionar una carpeta destino.")
            return
        if not os.path.isfile(self.archivo_entrada):
            messagebox.showerror("Error", "El archivo seleccionado no existe.")
            return

        if self.opcion.get() == "1":
            archivo_salida = encriptar(self.archivo_entrada, self.carpeta_salida)
            if archivo_salida:
                messagebox.showinfo("Éxito", f"Archivo encriptado correctamente:\n{archivo_salida}")
        elif self.opcion.get() == "2":
            archivo_salida = desencriptar(self.archivo_entrada, self.carpeta_salida)
            if archivo_salida:
                messagebox.showinfo("Éxito", f"Archivo desencriptado correctamente:\n{archivo_salida}")
        else:
            messagebox.showerror("Error", "Opción inválida.")

if __name__ == '__main__':
    app = App()
    app.mainloop()