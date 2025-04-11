import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import re
import signal
import sys
import os
from PIL import Image, ImageTk

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrcpy Control Panel")
        self.root.geometry("600x500")
        
        # Variables
        self.device_list = []
        self.selected_device = tk.StringVar()
        self.connection_mode = tk.StringVar(value="USB")
        self.ip_address = tk.StringVar()
        self.manual_device = tk.StringVar()
        self.port = tk.StringVar(value="5555")  # Puerto por defecto para ADB
        self.scrcpy_process = None
        
        # Configurar el manejador de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Inicializar la interfaz primero
        self.setup_ui()
        
        # Luego iniciar el servidor ADB
        self.start_adb_server()
        
    def start_adb_server(self):
        try:
            # Verificar si el servidor ADB está corriendo
            subprocess.run(['adb', 'start-server'], check=True)
            self.log("Servidor ADB iniciado correctamente")
        except subprocess.CalledProcessError as e:
            self.log(f"Error al iniciar el servidor ADB: {str(e)}")
        except FileNotFoundError:
            self.log("Error: ADB no está instalado o no está en el PATH")
            self.show_error("ADB no encontrado", 
                          "Por favor, asegúrate de que ADB esté instalado y en tu PATH.\n"
                          "Puedes instalarlo a través de Android SDK o Homebrew.")
            
    def show_error(self, title, message):
        messagebox.showerror(title, message)
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Lista de dispositivos
        devices_frame = ttk.Frame(main_frame)
        devices_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(devices_frame, text="Dispositivos detectados:").grid(row=0, column=0, sticky=tk.W)
        refresh_button = ttk.Button(devices_frame, text="🔄", width=3, command=self.refresh_devices)
        refresh_button.grid(row=0, column=1, padx=5)
        
        self.device_listbox = tk.Listbox(main_frame, height=5)
        self.device_listbox.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Agregar dispositivo manualmente
        manual_frame = ttk.Frame(main_frame)
        manual_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(manual_frame, text="Agregar dispositivo:").grid(row=0, column=0, sticky=tk.W)
        manual_entry = ttk.Entry(manual_frame, textvariable=self.manual_device)
        manual_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(manual_frame, text="Agregar", command=self.add_manual_device).grid(row=0, column=2)
        
        # Modo de conexión
        mode_frame = ttk.LabelFrame(main_frame, text="Modo de conexión", padding="5")
        mode_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(mode_frame, text="USB", variable=self.connection_mode, 
                       value="USB", command=self.toggle_mode).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(mode_frame, text="Wi-Fi", variable=self.connection_mode, 
                       value="Wi-Fi", command=self.toggle_mode).grid(row=0, column=1, padx=5)
        
        # Campo IP y Puerto
        self.ip_frame = ttk.Frame(main_frame)
        self.ip_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(self.ip_frame, text="IP:").grid(row=0, column=0)
        self.ip_entry = ttk.Entry(self.ip_frame, textvariable=self.ip_address)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(self.ip_frame, text="Puerto:").grid(row=0, column=2)
        port_entry = ttk.Entry(self.ip_frame, textvariable=self.port, width=6)
        port_entry.grid(row=0, column=3)
        
        # Botón para habilitar depuración Wi-Fi
        wifi_setup_button = ttk.Button(self.ip_frame, text="Habilitar Wi-Fi", 
                                     command=self.setup_wifi_debugging)
        wifi_setup_button.grid(row=0, column=4, padx=5)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Conectar", command=self.connect_device).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Desconectar", command=self.disconnect_device).grid(row=0, column=1, padx=5)
        
        # Logs
        ttk.Label(main_frame, text="Logs:").grid(row=6, column=0, sticky=tk.W)
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10)
        self.log_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Inicializar
        self.toggle_mode()
        
    def add_manual_device(self):
        device = self.manual_device.get().strip()
        if device:
            if device not in self.device_listbox.get(0, tk.END):
                self.device_listbox.insert(tk.END, device)
                self.log(f"Dispositivo agregado manualmente: {device}")
            else:
                self.log("El dispositivo ya está en la lista")
        else:
            self.log("Por favor, ingresa un ID de dispositivo o IP")
            
    def toggle_mode(self):
        if self.connection_mode.get() == "Wi-Fi":
            self.ip_frame.grid()
        else:
            self.ip_frame.grid_remove()
            
    def refresh_devices(self):
        try:
            # Primero verificar si ADB está disponible
            subprocess.run(['adb', 'version'], check=True, capture_output=True)
            
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            self.device_listbox.delete(0, tk.END)
            
            devices_found = False
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    device_id = line.split('\t')[0]
                    self.device_listbox.insert(tk.END, device_id)
                    devices_found = True
            
            if not devices_found:
                self.log("No se detectaron dispositivos. Asegúrate de que:")
                self.log("1. El dispositivo esté conectado por USB")
                self.log("2. La depuración USB esté habilitada")
                self.log("3. Hayas aceptado la solicitud de depuración en el dispositivo")
            else:
                self.log("Lista de dispositivos actualizada")
                
        except subprocess.CalledProcessError as e:
            self.log(f"Error al ejecutar ADB: {str(e)}")
        except FileNotFoundError:
            self.log("Error: ADB no está instalado o no está en el PATH")
            self.show_error("ADB no encontrado", 
                          "Por favor, asegúrate de que ADB esté instalado y en tu PATH.\n"
                          "Puedes instalarlo a través de Android SDK o Homebrew.")
            
    def connect_device(self):
        selected = self.device_listbox.curselection()
        if not selected:
            self.log("Por favor, selecciona un dispositivo")
            return
            
        device_id = self.device_listbox.get(selected[0])
        
        try:
            # Detener scrcpy anterior si existe
            if self.scrcpy_process:
                self.scrcpy_process.terminate()
                self.scrcpy_process = None

            # Iniciar nuevo proceso scrcpy
            self.scrcpy_process = subprocess.Popen(['scrcpy', '-s', device_id])
            self.log(f"Iniciando scrcpy para {device_id}")
        except Exception as e:
            self.log(f"Error al iniciar scrcpy: {str(e)}")
            
    def disconnect_device(self):
        selected = self.device_listbox.curselection()
        if not selected:
            self.log("Por favor, selecciona un dispositivo")
            return
            
        device_id = self.device_listbox.get(selected[0])
        try:
            # Detener scrcpy si está corriendo
            if self.scrcpy_process:
                self.scrcpy_process.terminate()
                self.scrcpy_process = None

            subprocess.run(['adb', 'disconnect', device_id], check=True)
            self.log(f"Desconectado {device_id}")
            self.refresh_devices()
        except subprocess.CalledProcessError as e:
            self.log(f"Error al desconectar: {str(e)}")
            
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def setup_wifi_debugging(self):
        """Configura la depuración Wi-Fi en el dispositivo conectado por USB"""
        try:
            # Verificar si hay dispositivos USB conectados
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = [line.split('\t')[0] for line in result.stdout.split('\n')[1:] if line.strip()]
            
            if not devices:
                self.log("No hay dispositivos USB conectados")
                return
                
            device = devices[0]  # Usar el primer dispositivo
            
            # Obtener la IP del dispositivo
            result = subprocess.run(['adb', 'shell', 'ip', 'route'], capture_output=True, text=True)
            ip_matches = re.findall(r'src (\d+\.\d+\.\d+\.\d+)', result.stdout)
            
            if not ip_matches:
                self.log("No se pudo obtener la IP del dispositivo")
                return
                
            device_ip = ip_matches[0]
            self.ip_address.set(device_ip)  # Actualizar el campo IP automáticamente
            
            # Primero desconectar cualquier conexión existente
            try:
                subprocess.run(['adb', 'disconnect'], check=True)
                self.log("Desconectando conexiones existentes...")
            except:
                pass

            # Habilitar el puerto TCP
            self.log(f"Configurando puerto TCP {self.port.get()}...")
            subprocess.run(['adb', 'tcpip', self.port.get()], check=True)
            self.log("Puerto TCP configurado correctamente")
            
            # Esperar un momento antes de intentar la conexión
            self.root.after(2000, lambda: self.try_wifi_connection(device_ip))
            
        except subprocess.CalledProcessError as e:
            self.log(f"Error al configurar Wi-Fi: {str(e)}")
        except Exception as e:
            self.log(f"Error inesperado: {str(e)}")

    def try_wifi_connection(self, ip):
        """Intenta establecer la conexión Wi-Fi después de un delay"""
        try:
            full_address = f"{ip}:{self.port.get()}"
            self.log(f"Intentando conectar a {full_address}...")
            
            result = subprocess.run(['adb', 'connect', full_address], 
                                 capture_output=True, text=True)
            self.log(result.stdout.strip())
            
            if "connected" in result.stdout.lower():
                self.log("Conexión Wi-Fi establecida correctamente")
                self.refresh_devices()  # Actualizar la lista de dispositivos
            else:
                self.log("Error al establecer la conexión Wi-Fi")
                
        except subprocess.CalledProcessError as e:
            self.log(f"Error al conectar: {str(e)}")
        except Exception as e:
            self.log(f"Error inesperado: {str(e)}")

    def on_closing(self):
        """Limpia las conexiones y procesos antes de cerrar"""
        try:
            # Detener scrcpy si está corriendo
            if self.scrcpy_process:
                self.scrcpy_process.terminate()
                self.scrcpy_process = None

            # Desconectar todos los dispositivos
            self.log("Cerrando conexiones...")
            subprocess.run(['adb', 'disconnect'], check=True)
            
            # Matar el servidor ADB
            self.log("Deteniendo servidor ADB...")
            subprocess.run(['adb', 'kill-server'], check=True)
            
        except Exception as e:
            self.log(f"Error durante la limpieza: {str(e)}")
        
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrcpyGUI(root)
    root.mainloop() 