"""
Módulo: gui.py

Copyright (c) 2025 Demian Romero Bautista y Renata García Resendiz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.


Descripción: Interfaz gráfica de usuario para las calculadoras IP CIDR y VLSM
Grupo: 5CV1
Asignatura: Redes de Computadoras
Fecha: Diciembre 2025
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from cidr_calculator import CalculadoraCIDR
from vlsm_calculator import CalculadoraVLSM
from typing import List, Tuple


class CalculadoraIPGUI:
    """
    Clase principal de la interfaz gráfica.
    
    Descripción:
        Proporciona una interfaz amigable con pestañas para acceder
        a ambas calculadoras (CIDR y VLSM).

        - Usa Tkinter con ttk para widgets modernos
        - Diseño responsivo con dos pestañas principales
        - Permite exportar resultados a archivo de texto
    """
    
    def __init__(self, ventana):
        """
        Constructor de la interfaz gráfica.
        
        Entradas:
            ventana (tk.Tk): Ventana principal de Tkinter
        
        Observaciones:
            - Inicializa calculadoras
            - Configura ventana principal
            - Crea pestañas y componentes
        """
        self.ventana = ventana
        self.ventana.title("Calculadora IP - CIDR y VLSM")
        self.ventana.geometry("1000x700")
        self.ventana.resizable(True, True)
        
        # Instanciar calculadoras
        self.calc_cidr = CalculadoraCIDR()
        self.calc_vlsm = CalculadoraVLSM()
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Crear contenedor de pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_cidr()
        self.crear_pestana_vlsm()
        
        # Barra de estado
        self.crear_barra_estado()
    
    def configurar_estilos(self):
        
        """
        Configuración visual moderna azul/blanco
        """
        estilo = ttk.Style()
        estilo.theme_use('clam')

        # Colores
        azul_principal = "#1565C0"
        azul_secundario = "#1E88E5"
        azul_claro = "#E3F2FD"
        blanco = "#FFFFFF"

        self.ventana.configure(bg=azul_claro)

        # Labels
        estilo.configure(
            'TLabel',
            background=blanco,
            foreground="#0D47A1",
            font=('Segoe UI', 11)
        )

        # Títulos
        estilo.configure(
            'Title.TLabel',
            background=blanco,
            foreground=azul_principal,
            font=('Segoe UI', 18, 'bold')
        )

        estilo.configure(
            'Header.TLabel',
            background=blanco,
            foreground=azul_principal,
            font=('Segoe UI', 13, 'bold')
        )

        # Botones
        estilo.configure(
            'TButton',
            font=('Segoe UI', 11, 'bold'),
            padding=8,
            background=azul_principal,
            foreground='white'
        )

        estilo.map(
            'TButton',
            background=[('active', azul_secundario)]
        )

        estilo.configure(
            'TFrame',
            background=blanco
        )

        # Notebook (Pestañas)
        estilo.configure(
            'TNotebook',
            background=azul_claro,
            borderwidth=0
        )

        estilo.configure(
            'TNotebook.Tab',
            padding=[20, 10],
            font=('Segoe UI', 11, 'bold')
        )

        # Frames
        estilo.configure(
            'TLabelframe',
            background=blanco,
            borderwidth=2
        )

        estilo.configure(
            'TLabelframe.Label',
            foreground=azul_principal,
            font=('Segoe UI', 11, 'bold')
        )

        # Treeview
        estilo.configure(
            'Treeview',
            rowheight=28,
            font=('Segoe UI', 10)
        )

        estilo.configure(
            'Treeview.Heading',
            font=('Segoe UI', 10, 'bold')
        )
    # ================================================================
    # PESTAÑA CALCULADORA CIDR
    # ================================================================
    
    def crear_pestana_cidr(self):
        """
        Crea la pestaña de la Calculadora CIDR.
        
        Descripción:
            Incluye campos de entrada para IP/prefijo,
            botones de acción y área de resultados.
        
        Observaciones:
            - Layout organizado con frames
            - Validación en tiempo real opcional
            - Muestra resultados formateados
        """
        # Frame principal de CIDR 
        frame_cidr = ttk.Frame(self.notebook)
        self.notebook.add(frame_cidr, text='Calculadora CIDR')
        
        # Título
        titulo = ttk.Label(frame_cidr, text="Calculadora IP - CIDR", style='Title.TLabel')
        titulo.pack(pady=10)
        
        # Frame de entrada
        frame_entrada = ttk.LabelFrame(frame_cidr, text="Datos de Entrada", padding=15)
        frame_entrada.pack(fill='x', padx=20, pady=10)
        
        # Campo IP/Prefijo
        ttk.Label(frame_entrada, text="Dirección IP / Prefijo:").grid(row=0, column=0, sticky='w', pady=5)
        self.entrada_cidr = ttk.Entry(frame_entrada, width=40, font=('Courier New', 11))
        self.entrada_cidr.grid(row=0, column=1, padx=10, pady=5)
        self.entrada_cidr.insert(0, "192.168.1.0/24")
        
        ttk.Label(frame_entrada, text="Ejemplo: 192.168.1.0/24 o 192.168.1.0 255.255.255.0", 
                 foreground='gray').grid(row=1, column=1, sticky='w')
        
        # Checkbox para incluir binario
        self.incluir_binario_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame_entrada, text="Incluir representación binaria", 
                       variable=self.incluir_binario_var).grid(row=2, column=1, sticky='w', pady=5)
        
        # Frame de botones
        frame_botones_cidr = ttk.Frame(frame_cidr)
        frame_botones_cidr.pack(pady=10)
        
        ttk.Button(frame_botones_cidr, text="Calcular", 
                  command=self.calcular_cidr, width=15).pack(side='left', padx=5)
        ttk.Button(frame_botones_cidr, text="Limpiar", 
                  command=self.limpiar_cidr, width=15).pack(side='left', padx=5)
        ttk.Button(frame_botones_cidr, text="Exportar", 
                  command=self.exportar_cidr, width=15).pack(side='left', padx=5)
        
        # Frame de resultados
        frame_resultados_cidr = ttk.LabelFrame(frame_cidr, text="Resultados", padding=10)
        frame_resultados_cidr.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.texto_resultados_cidr = scrolledtext.ScrolledText(
            frame_resultados_cidr, 
            width=100, 
            height=20, 
            font=('Courier New', 10),
            wrap=tk.WORD
        )
        self.texto_resultados_cidr.pack(fill='both', expand=True)
    
    def calcular_cidr(self):
        """
        Ejecuta el cálculo CIDR y muestra los resultados.
        
        Observaciones:
            - Obtiene datos del campo de entrada
            - Llama a la calculadora CIDR
            - Formatea y muestra resultados
            - Maneja errores con mensajes claros
        """
        entrada = self.entrada_cidr.get().strip()
        
        if not entrada:
            messagebox.showwarning("Advertencia", "Por favor ingrese una dirección IP con prefijo")
            return
        
        # Actualizar barra de estado
        self.actualizar_estado("Calculando...")
        
        try:
            # Realizar cálculo
            incluir_binario = self.incluir_binario_var.get()
            resultado = self.calc_cidr.calcular(entrada, incluir_binario)
            
            # Mostrar resultados
            self.texto_resultados_cidr.delete(1.0, tk.END)
            
            if resultado['exito']:
                texto_formateado = self.calc_cidr.formatear_resultado(resultado)
                self.texto_resultados_cidr.insert(1.0, texto_formateado)
                self.actualizar_estado("Cálculo completado exitosamente")
            else:
                self.texto_resultados_cidr.insert(1.0, f"ERROR: {resultado['error']}")
                self.actualizar_estado("Error en el cálculo")
                messagebox.showerror("Error", resultado['error'])
        
        except Exception as e:
            self.texto_resultados_cidr.insert(1.0, f"ERROR INESPERADO: {str(e)}")
            self.actualizar_estado("Error inesperado")
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar_cidr(self):
        """Limpia los campos y resultados de la calculadora CIDR."""
        self.entrada_cidr.delete(0, tk.END)
        self.texto_resultados_cidr.delete(1.0, tk.END)
        self.incluir_binario_var.set(False)
        self.actualizar_estado("Listo")
    
    def exportar_cidr(self):
        """
        Exporta los resultados CIDR a un archivo de texto.
        
        Observaciones:
            - Abre diálogo para guardar archivo
            - Guarda contenido del área de resultados
        """
        contenido = self.texto_resultados_cidr.get(1.0, tk.END).strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar resultados CIDR"
        )
        
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("Éxito", f"Resultados exportados a:\n{archivo}")
                self.actualizar_estado("Resultados exportados")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    # ================================================================
    # PESTAÑA CALCULADORA VLSM
    # ================================================================
    
    def crear_pestana_vlsm(self):
        """
        Crea la pestaña de la Calculadora VLSM.
        
        Descripción:
            Incluye entrada de red base, tabla dinámica para requisitos
            de subredes, botones de acción y área de resultados.
        
        Observaciones:
            - Permite agregar/eliminar requisitos dinámicamente
            - Tabla editable para nombres y cantidades de hosts
            - Muestra resultados en tabla y texto
        """
        # Frame principal de VLSM
        frame_vlsm = ttk.Frame(self.notebook)
        self.notebook.add(frame_vlsm, text='Calculadora VLSM')
        
        # Título
        titulo = ttk.Label(frame_vlsm, text="Calculadora VLSM", style='Title.TLabel')
        titulo.pack(pady=10)
        
        # Frame de red base
        frame_red_base = ttk.LabelFrame(frame_vlsm, text="Red Base", padding=15)
        frame_red_base.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_red_base, text="Red Base (IP/Prefijo):").grid(row=0, column=0, sticky='w', pady=5)
        self.entrada_red_base = ttk.Entry(frame_red_base, width=40, font=('Courier New', 11))
        self.entrada_red_base.grid(row=0, column=1, padx=10, pady=5)
        self.entrada_red_base.insert(0, "192.168.0.0/24")
        
        ttk.Label(frame_red_base, text="Ejemplo: 192.168.0.0/24 o 10.0.0.0/16", 
                 foreground='gray').grid(row=1, column=1, sticky='w')
        
        # Frame de requisitos de subredes
        frame_requisitos = ttk.LabelFrame(frame_vlsm, text="Requisitos de Subredes", padding=15)
        frame_requisitos.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Instrucciones
        ttk.Label(frame_requisitos, text="Agregue las subredes que necesita con su cantidad de hosts:",
                 font=('Segoe UI', 9, 'italic')).pack(anchor='w', pady=5)
        
        # Frame para la tabla de requisitos
        frame_tabla = ttk.Frame(frame_requisitos)
        frame_tabla.pack(fill='both', expand=True)
        
        # Crear Treeview para mostrar requisitos
        columnas = ('nombre', 'hosts')
        self.tabla_requisitos = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=6)
        
        self.tabla_requisitos.heading('nombre', text='Nombre de Subred')
        self.tabla_requisitos.heading('hosts', text='Hosts Requeridos')
        
        self.tabla_requisitos.column('nombre', width=300)
        self.tabla_requisitos.column('hosts', width=150)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tabla_requisitos.yview)
        self.tabla_requisitos.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_requisitos.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame para agregar requisitos
        frame_agregar = ttk.Frame(frame_requisitos)
        frame_agregar.pack(fill='x', pady=10)
        
        ttk.Label(frame_agregar, text="Nombre:").pack(side='left', padx=5)
        self.entrada_nombre_subred = ttk.Entry(frame_agregar, width=25)
        self.entrada_nombre_subred.pack(side='left', padx=5)
        
        ttk.Label(frame_agregar, text="Hosts:").pack(side='left', padx=5)
        self.entrada_hosts = ttk.Entry(frame_agregar, width=15)
        self.entrada_hosts.pack(side='left', padx=5)
        
        ttk.Button(frame_agregar, text="Agregar Subred", 
                  command=self.agregar_requisito).pack(side='left', padx=5)
        ttk.Button(frame_agregar, text="Eliminar Seleccionado", 
                  command=self.eliminar_requisito).pack(side='left', padx=5)
        ttk.Button(frame_agregar, text="Limpiar Todo", 
                  command=self.limpiar_requisitos).pack(side='left', padx=5)
        
        # Frame de botones principales
        frame_botones_vlsm = ttk.Frame(frame_vlsm)
        frame_botones_vlsm.pack(pady=10)
        
        ttk.Button(frame_botones_vlsm, text="Calcular VLSM", 
                  command=self.calcular_vlsm, width=20).pack(side='left', padx=5)
        ttk.Button(frame_botones_vlsm, text="Limpiar Resultados", 
                  command=self.limpiar_vlsm, width=20).pack(side='left', padx=5)
        ttk.Button(frame_botones_vlsm, text="Exportar Resultados", 
                  command=self.exportar_vlsm, width=20).pack(side='left', padx=5)
        
        # Frame de resultados
        frame_resultados_vlsm = ttk.LabelFrame(frame_vlsm, text="Resultados VLSM", padding=10)
        frame_resultados_vlsm.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.texto_resultados_vlsm = scrolledtext.ScrolledText(
            frame_resultados_vlsm, 
            width=100, 
            height=15, 
            font=('Courier New', 9),
            wrap=tk.WORD
        )
        self.texto_resultados_vlsm.pack(fill='both', expand=True)
    
    def agregar_requisito(self):
        """
        Agrega un requisito de subred a la tabla.
        
        Observaciones:
            - Valida que el nombre no esté vacío
            - Valida que los hosts sean un número positivo
            - Agrega a la tabla de requisitos
        """
        nombre = self.entrada_nombre_subred.get().strip()
        hosts_str = self.entrada_hosts.get().strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese un nombre para la subred")
            return
        
        try:
            hosts = int(hosts_str)
            if hosts <= 0:
                raise ValueError("Debe ser positivo")
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingrese un número válido de hosts (mayor a 0)")
            return
        
        # Agregar a la tabla
        self.tabla_requisitos.insert('', 'end', values=(nombre, hosts))
        
        # Limpiar campos
        self.entrada_nombre_subred.delete(0, tk.END)
        self.entrada_hosts.delete(0, tk.END)
        self.entrada_nombre_subred.focus()
        
        self.actualizar_estado(f"Subred '{nombre}' agregada")
    
    def eliminar_requisito(self):
        """Elimina el requisito seleccionado de la tabla."""
        seleccion = self.tabla_requisitos.selection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un requisito para eliminar")
            return
        
        for item in seleccion:
            self.tabla_requisitos.delete(item)
        
        self.actualizar_estado("Requisito eliminado")
    
    def limpiar_requisitos(self):
        """Limpia todos los requisitos de la tabla."""
        for item in self.tabla_requisitos.get_children():
            self.tabla_requisitos.delete(item)
        
        self.actualizar_estado("Requisitos limpiados")
    
    def cargar_ejemplo_vlsm(self):
        """
        Carga un ejemplo predefinido de requisitos VLSM.
        
        Observaciones:
            - Útil para demostración y pruebas
            - Carga ejemplo del documento del proyecto
        """
        # Limpiar tabla actual
        self.limpiar_requisitos()
        
        # Ejemplo según el documento: A=100, B=50, C=25, D=10
        ejemplos = [
            ("Departamento Ventas", 100),
            ("Departamento IT", 50),
            ("Departamento Admin", 25),
            ("Sala de Reuniones", 10)
        ]
        
        for nombre, hosts in ejemplos:
            self.tabla_requisitos.insert('', 'end', values=(nombre, hosts))
        
        self.actualizar_estado("Ejemplo cargado")
        messagebox.showinfo("Ejemplo Cargado", 
                           "Se ha cargado un ejemplo con 4 subredes.\n"
                           "Red base sugerida: 192.168.0.0/24")
    
    def obtener_requisitos_desde_tabla(self) -> List[Tuple[str, int]]:
        """
        Extrae los requisitos de la tabla como lista de tuplas.
        
        Salidas:
            List[Tuple[str, int]]: Lista de (nombre, hosts)
        
        Observaciones:
            - Lee todos los items de la tabla
            - Convierte hosts a entero
        """
        requisitos = []
        
        for item in self.tabla_requisitos.get_children():
            valores = self.tabla_requisitos.item(item, 'values')
            nombre = valores[0]
            hosts = int(valores[1])
            requisitos.append((nombre, hosts))
        
        return requisitos
    
    def calcular_vlsm(self):
        """
        Ejecuta el cálculo VLSM y muestra los resultados.
        
        Observaciones:
            - Obtiene red base y requisitos
            - Llama a la calculadora VLSM
            - Formatea y muestra resultados
            - Maneja errores con mensajes claros
        """
        red_base = self.entrada_red_base.get().strip()
        
        if not red_base:
            messagebox.showwarning("Advertencia", "Por favor ingrese una red base")
            return
        
        requisitos = self.obtener_requisitos_desde_tabla()
        
        if not requisitos:
            messagebox.showwarning("Advertencia", 
                                 "Agregue al menos un requisito de subred.\n"
                                 "Puede usar el botón 'Cargar Ejemplo' para ver un ejemplo.")
            return
        
        # Actualizar barra de estado
        self.actualizar_estado("Calculando VLSM...")
        
        try:
            # Realizar cálculo
            resultado = self.calc_vlsm.calcular_vlsm(red_base, requisitos)
            
            # Mostrar resultados
            self.texto_resultados_vlsm.delete(1.0, tk.END)
            
            if resultado['exito']:
                texto_formateado = self.calc_vlsm.formatear_resultado(resultado)
                self.texto_resultados_vlsm.insert(1.0, texto_formateado)
                self.actualizar_estado("Cálculo VLSM completado exitosamente")
                
                # Mostrar mensaje de éxito con resumen
                messagebox.showinfo("Cálculo Exitoso", 
                                   f"VLSM calculado correctamente.\n\n"
                                   f"Subredes creadas: {len(resultado['subredes'])}\n"
                                   f"Eficiencia: {resultado['eficiencia']}%\n"
                                   f"Espacio libre: {resultado['espacio_libre']} direcciones")
            else:
                self.texto_resultados_vlsm.insert(1.0, f"ERROR: {resultado['error']}")
                self.actualizar_estado("Error en el cálculo VLSM")
                messagebox.showerror("Error", resultado['error'])
        
        except Exception as e:
            self.texto_resultados_vlsm.insert(1.0, f"ERROR INESPERADO: {str(e)}")
            self.actualizar_estado("Error inesperado")
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar_vlsm(self):
        """Limpia los resultados de la calculadora VLSM."""
        self.texto_resultados_vlsm.delete(1.0, tk.END)
        self.actualizar_estado("Resultados limpiados")
    
    def exportar_vlsm(self):
        """Exporta los resultados VLSM a un archivo de texto."""
        contenido = self.texto_resultados_vlsm.get(1.0, tk.END).strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay resultados para exportar")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar resultados VLSM"
        )
        
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("Éxito", f"Resultados exportados a:\n{archivo}")
                self.actualizar_estado("Resultados exportados")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    # ================================================================
    # BARRA DE ESTADO
    # ================================================================
    
    def crear_barra_estado(self):
        """
        Crea la barra de estado en la parte inferior de la ventana.
        
        Observaciones:
            - Muestra mensajes de estado
            - Información del equipo
        """
        self.barra_estado = tk.Label(
            self.ventana, 
            text="Listo", 
            bg="#1565C0",
            fg="white",
            anchor='w',
            padx=10,
            font=('Segoe UI', 10)
        )
        self.barra_estado.pack(side='bottom', fill='x')
    
    def actualizar_estado(self, mensaje: str):
        """
        Actualiza el mensaje de la barra de estado.
        
        Entradas:
            mensaje (str): Mensaje a mostrar
        """
        self.barra_estado.config(text=mensaje)
        self.ventana.update_idletasks()


def main():
    """
    Función principal para ejecutar la aplicación.
    
    Descripción:
        Crea la ventana principal y ejecuta el loop de eventos de Tkinter.
    
    Observaciones:
        - Punto de entrada de la aplicación
        - Configura el ícono si está disponible
    """
    ventana = tk.Tk()
    
    # Intentar establecer ícono (opcional)
    try:
        # ventana.iconbitmap('icono.ico')  # Descomentar si tiene ícono
        pass
    except:
        pass
    
    # Crear aplicación
    app = CalculadoraIPGUI(ventana)
    
    # Ejecutar loop de eventos
    ventana.mainloop()


if __name__ == "__main__":
    main()