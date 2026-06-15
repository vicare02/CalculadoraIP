"""
Archivo: main.py
Proyecto: Calculadora IP - CIDR y VLSM
Instituto Politécnico Nacional - Escuela Superior de Cómputo
Grupo: 5CM1
Redes de Computadoras
"""

import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar la interfaz gráfica
from gui import main as ejecutar_gui


def mostrar_banner():
    """
    Muestra la bienvenida en consola.
    """
    banner = """
    ═════════════════════════════════════════════════════════════
                Instituto Politécnico Nacional                        
                Escuela Superior de Cómputo
     
                CALCULADORA IP - CIDR Y VLSM                   
                Aparicio Arenas Victor Eduardo  
                                                                                                                                                                   
                Proyecto 3: Calculadora IP                        
                                                                  
    ═════════════════════════════════════════════════════════════
    
    Iniciando aplicación...
    """
    print(banner)


def verificar_requisitos():
    """
    Verifica que todos los requisitos estén instalados.
    
    Salidas:
        bool: True si todos los requisitos están presentes
    
    Observaciones:
        - Verifica módulos necesarios
        - Muestra mensajes de error si falta algo
    """
    try:
        import tkinter
        return True
    except ImportError:
        print("ERROR: Tkinter no está instalado.")
        print("Tkinter viene incluido con Python en la mayoría de las instalaciones.")
        print("Si usa Linux, instale con: sudo apt-get install python3-tk")
        return False


def main():
    """
    Función principal de la aplicación.
    
    Descripción:
        - Muestra banner
        - Verifica requisitos
        - Inicia la interfaz gráfica
    
    Observaciones:
        - Maneja errores de inicialización
        - Proporciona mensajes claros al usuario
    """
    # Mostrar banner
    mostrar_banner()
    
    # Verificar requisitos
    if not verificar_requisitos():
        print("\nNo se puede iniciar la aplicación. Resuelva los problemas anteriores.")
        sys.exit(1)
    
    try:
        # Iniciar interfaz gráfica
        print("Abriendo interfaz gráfica...")
        ejecutar_gui()
        
    except KeyboardInterrupt:
        print("\n\nAplicación cerrada por el usuario.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n\nERROR FATAL: {str(e)}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()