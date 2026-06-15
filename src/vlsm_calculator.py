"""
Módulo: vlsm_calculator.py
"""

import math
from typing import List, Dict, Tuple, Optional
from ip_utils import (
    validar_direccion_ip,
    validar_prefijo,
    ip_a_entero,
    entero_a_ip,
    prefijo_a_mascara,
    calcular_broadcast,
    parsear_entrada_ip_cidr
)


class SubredVLSM:
    """
    Clase que representa una subred individual en el esquema VLSM.
    
    Observaciones:
        - Almacena todos los datos calculados para una subred
        - Facilita el manejo y visualización de resultados
    """
    
    def __init__(self, nombre: str, hosts_requeridos: int, red: str, 
                 prefijo: int, mascara: str, primera_host: str, 
                 ultima_host: str, broadcast: str, hosts_disponibles: int):
        """
        Constructor de SubredVLSM.
        
        Entradas:
            nombre (str): Nombre descriptivo de la subred
            hosts_requeridos (int): Cantidad de hosts solicitados
            red (str): Dirección de red asignada
            prefijo (int): Longitud del prefijo CIDR
            mascara (str): Máscara en formato decimal punteado
            primera_host (str): Primera IP utilizable
            ultima_host (str): Última IP utilizable
            broadcast (str): Dirección de broadcast
            hosts_disponibles (int): Hosts utilizables en esta subred
        """
        self.nombre = nombre
        self.hosts_requeridos = hosts_requeridos
        self.red = red
        self.prefijo = prefijo
        self.mascara = mascara
        self.primera_host = primera_host
        self.ultima_host = ultima_host
        self.broadcast = broadcast
        self.hosts_disponibles = hosts_disponibles
        self.espacio_desperdiciado = hosts_disponibles - hosts_requeridos
    
    def a_diccionario(self) -> Dict:
        """
        Convierte la subred a un diccionario.
        
        Salidas:
            Dict: Diccionario con todos los atributos de la subred
        
        Observaciones:
            - Útil para serialización y visualización
        """
        return {
            'nombre': self.nombre,
            'hosts_requeridos': self.hosts_requeridos,
            'red': self.red,
            'prefijo': self.prefijo,
            'mascara': self.mascara,
            'primera_host': self.primera_host,
            'ultima_host': self.ultima_host,
            'broadcast': self.broadcast,
            'hosts_disponibles': self.hosts_disponibles,
            'espacio_desperdiciado': self.espacio_desperdiciado
        }
    
    def __str__(self) -> str:
        """Representación en cadena de la subred."""
        return (f"{self.nombre}: {self.red}/{self.prefijo} "
                f"({self.hosts_disponibles} hosts, {self.espacio_desperdiciado} desperdiciados)")


class CalculadoraVLSM:
    """
    Clase para calcular subdivisión de redes usando VLSM.
    
    Descripción:
        Implementa el algoritmo VLSM que permite crear subredes de diferentes
        tamaños a partir de una red base, optimizando el uso del espacio de
        direcciones IP disponible.
    
    Observaciones:
        - Ordena subredes por tamaño (mayor a menor)
        - Asigna bloques contiguos sin solapamiento
        - Valida que haya espacio suficiente en la red base
        - Calcula espacio desperdiciado en cada subred
    """
    
    def __init__(self):
        """
        Constructor de la clase CalculadoraVLSM.
        
        Observaciones:
            - No requiere parámetros de inicialización
            - Cada cálculo es independiente
        """
        pass
    
    def calcular_prefijo_requerido(self, hosts_requeridos: int) -> int:
        """
        Calcula el prefijo CIDR mínimo necesario para acomodar los hosts requeridos.
        
        Entradas:
            hosts_requeridos (int): Número de hosts que se necesitan
        
        Salidas:
            int: Longitud del prefijo CIDR necesario
        
        Observaciones:
            - Se agregan 2 direcciones (red + broadcast)
            - Usa logaritmo base 2 para calcular bits necesarios
            - Redondea hacia arriba para asegurar espacio suficiente
        
        Descripción del algoritmo:
            1. hosts_totales = hosts_requeridos + 2
            2. bits_host = ceil(log2(hosts_totales))
            3. prefijo = 32 - bits_host
        """
        # Agregar direcciones de red y broadcast
        hosts_totales = hosts_requeridos + 2
        
        # Calcular bits de host necesarios
        bits_host = math.ceil(math.log2(hosts_totales))
        
        # Prefijo = 32 - bits_host
        prefijo = 32 - bits_host
        
        return prefijo
    
    def ordenar_subredes(self, requisitos: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """
        Ordena las subredes por número de hosts requeridos (mayor a menor).
        
        Entradas:
            requisitos (List[Tuple[str, int]]): Lista de tuplas (nombre, hosts_requeridos)
        
        Salidas:
            List[Tuple[str, int]]: Lista ordenada descendentemente por hosts
        
        Observaciones:
            - VLSM requiere asignar primero las subredes más grandes
            - Esto minimiza fragmentación y desperdicio
            - Mantiene los nombres asociados a cada requisito
        """
        return sorted(requisitos, key=lambda x: x[1], reverse=True)
    
    def calcular_vlsm(self, red_base: str, requisitos: List[Tuple[str, int]]) -> Dict:
        """
        Calcula la subdivisión VLSM de una red base según requisitos dados.
        
        Entradas:
            red_base (str): Red base en formato "IP/prefijo" (ej: "192.168.0.0/24")
            requisitos (List[Tuple[str, int]]): Lista de (nombre_subred, hosts_requeridos)
                Ejemplo: [("Ventas", 100), ("Administración", 50), ("IT", 25)]
        
        Salidas:
            Dict: Diccionario con:
                - exito (bool): True si el cálculo fue exitoso
                - error (str): Mensaje de error si exito = False
                - red_base (str): Red base utilizada
                - prefijo_base (int): Prefijo de la red base
                - subredes (List[SubredVLSM]): Lista de subredes asignadas
                - espacio_total (int): Total de direcciones disponibles
                - espacio_utilizado (int): Direcciones utilizadas por las subredes
                - espacio_libre (int): Direcciones sin asignar
                - eficiencia (float): Porcentaje de uso eficiente (0-100)
        
        Observaciones:
            - Valida que la red base sea suficiente para todos los requisitos
            - Asigna bloques contiguos sin solapamientos
            - Calcula estadísticas de uso de espacio
        
        Descripción del algoritmo (según especificación del proyecto):
            1. Parsear y validar red_base
            2. Calcular espacio total disponible
            3. Ordenar requisitos por tamaño (mayor → menor)
            4. Para cada requisito:
                a. Calcular prefijo necesario
                b. Calcular tamaño del bloque
                c. Asignar dirección de red actual
                d. Calcular primera host, última host, broadcast
                e. Avanzar puntero al siguiente bloque
            5. Validar que no se exceda el espacio disponible
            6. Calcular estadísticas
        """
        # ============================================================
        # PASO 1: Parsear y validar entrada
        # ============================================================
        datos_entrada = parsear_entrada_ip_cidr(red_base)
        
        if datos_entrada is None:
            return {
                'exito': False,
                'error': 'Formato de red base inválido. Use: IP/prefijo (ej: 192.168.0.0/24)'
            }
        
        ip_base, prefijo_base = datos_entrada
        
        if not validar_direccion_ip(ip_base) or not validar_prefijo(prefijo_base):
            return {
                'exito': False,
                'error': 'Dirección IP o prefijo inválidos'
            }
        
        # ============================================================
        # PASO 2: Calcular espacio total disponible
        # ============================================================
        red_base_entero = ip_a_entero(ip_base)
        bits_disponibles = 32 - prefijo_base
        espacio_total = 2 ** bits_disponibles
        limite_superior = red_base_entero + espacio_total
        
        # ============================================================
        # PASO 3: Validar requisitos
        # ============================================================
        if not requisitos or len(requisitos) == 0:
            return {
                'exito': False,
                'error': 'Debe proporcionar al menos un requisito de subred'
            }
        
        # Validar que todos los requisitos sean positivos
        for nombre, hosts in requisitos:
            if hosts <= 0:
                return {
                    'exito': False,
                    'error': f'Requisito inválido para "{nombre}": {hosts} hosts (debe ser > 0)'
                }
        
        # ============================================================
        # PASO 4: Ordenar subredes por tamaño (mayor → menor)
        # ============================================================
        requisitos_ordenados = self.ordenar_subredes(requisitos)
        
        # ============================================================
        # PASO 5: Asignar subredes usando algoritmo VLSM
        # ============================================================
        subredes_asignadas = []
        puntero_actual = red_base_entero  # Dirección actual de asignación
        
        for nombre_subred, hosts_requeridos in requisitos_ordenados:
            # Paso 5a: Calcular prefijo necesario
            prefijo_subred = self.calcular_prefijo_requerido(hosts_requeridos)
            
            # Paso 5b: Calcular tamaño del bloque
            bits_host = 32 - prefijo_subred
            tamano_bloque = 2 ** bits_host
            
            # Verificar si hay espacio suficiente
            if puntero_actual + tamano_bloque > limite_superior:
                return {
                    'exito': False,
                    'error': f'Espacio insuficiente en la red base para la subred "{nombre_subred}". '
                            f'Se requieren {hosts_requeridos} hosts pero solo quedan '
                            f'{limite_superior - puntero_actual} direcciones disponibles.'
                }
            
            # Paso 5c: Asignar dirección de red
            direccion_red = entero_a_ip(puntero_actual)
            
            # Paso 5d: Calcular primera host, última host y broadcast
            primera_host = entero_a_ip(puntero_actual + 1)
            broadcast_entero = puntero_actual + tamano_bloque - 1
            broadcast = entero_a_ip(broadcast_entero)
            ultima_host = entero_a_ip(broadcast_entero - 1)
            
            # Calcular hosts disponibles (total - red - broadcast)
            hosts_disponibles = tamano_bloque - 2
            
            # Obtener máscara en formato decimal
            mascara = prefijo_a_mascara(prefijo_subred)
            
            # Crear objeto SubredVLSM
            subred = SubredVLSM(
                nombre=nombre_subred,
                hosts_requeridos=hosts_requeridos,
                red=direccion_red,
                prefijo=prefijo_subred,
                mascara=mascara,
                primera_host=primera_host,
                ultima_host=ultima_host,
                broadcast=broadcast,
                hosts_disponibles=hosts_disponibles
            )
            
            subredes_asignadas.append(subred)
            
            # Paso 5e: Avanzar puntero al siguiente bloque
            puntero_actual += tamano_bloque
        
        # ============================================================
        # PASO 6: Calcular estadísticas de uso
        # ============================================================
        espacio_utilizado = puntero_actual - red_base_entero
        espacio_libre = espacio_total - espacio_utilizado
        
        # Calcular hosts totales requeridos vs disponibles
        hosts_totales_requeridos = sum(hosts for _, hosts in requisitos)
        hosts_totales_asignados = sum(sub.hosts_disponibles for sub in subredes_asignadas)
        
        # Eficiencia = (hosts requeridos / hosts asignados) * 100
        if hosts_totales_asignados > 0:
            eficiencia = (hosts_totales_requeridos / hosts_totales_asignados) * 100
        else:
            eficiencia = 0.0
        
        # ============================================================
        # PASO 7: Construir resultado exitoso
        # ============================================================
        return {
            'exito': True,
            'red_base': f"{ip_base}/{prefijo_base}",
            'prefijo_base': prefijo_base,
            'subredes': subredes_asignadas,
            'espacio_total': espacio_total,
            'espacio_utilizado': espacio_utilizado,
            'espacio_libre': espacio_libre,
            'hosts_totales_requeridos': hosts_totales_requeridos,
            'hosts_totales_asignados': hosts_totales_asignados,
            'eficiencia': round(eficiencia, 2)
        }
    
    def validar_requisitos(self, red_base: str, requisitos: List[Tuple[str, int]]) -> Dict:
        """
        Valida si una red base puede acomodar los requisitos dados sin hacer el cálculo completo.
        
        Entradas:
            red_base (str): Red base en formato "IP/prefijo"
            requisitos (List[Tuple[str, int]]): Lista de requisitos
        
        Salidas:
            Dict: Diccionario con:
                - valido (bool): True si es posible acomodar todos los requisitos
                - mensaje (str): Mensaje descriptivo
                - espacio_requerido (int): Direcciones necesarias mínimas
                - espacio_disponible (int): Direcciones disponibles en la red base
        
        Observaciones:
            - Más rápido que hacer el cálculo completo
            - Útil para validación previa en la UI
        """
        # Parsear red base
        datos_entrada = parsear_entrada_ip_cidr(red_base)
        
        if datos_entrada is None:
            return {
                'valido': False,
                'mensaje': 'Formato de red base inválido'
            }
        
        ip_base, prefijo_base = datos_entrada
        espacio_disponible = 2 ** (32 - prefijo_base)
        
        # Calcular espacio mínimo requerido
        espacio_requerido = 0
        for nombre, hosts in requisitos:
            if hosts <= 0:
                return {
                    'valido': False,
                    'mensaje': f'Requisito inválido para "{nombre}": debe ser > 0'
                }
            
            prefijo_necesario = self.calcular_prefijo_requerido(hosts)
            tamano_bloque = 2 ** (32 - prefijo_necesario)
            espacio_requerido += tamano_bloque
        
        if espacio_requerido > espacio_disponible:
            return {
                'valido': False,
                'mensaje': f'Espacio insuficiente: se requieren {espacio_requerido} direcciones '
                          f'pero solo hay {espacio_disponible} disponibles',
                'espacio_requerido': espacio_requerido,
                'espacio_disponible': espacio_disponible
            }
        
        return {
            'valido': True,
            'mensaje': 'Requisitos válidos',
            'espacio_requerido': espacio_requerido,
            'espacio_disponible': espacio_disponible
        }
    
    def formatear_resultado(self, resultado: Dict) -> str:
        """
        Formatea un resultado de cálculo VLSM como texto legible.
        
        Entradas:
            resultado (Dict): Diccionario retornado por calcular_vlsm()
        
        Salidas:
            str: Texto formateado con tabla de subredes y estadísticas
        
        Observaciones:
            - Crea tabla ASCII con todas las subredes
            - Incluye estadísticas de uso
            - Útil para exportar o mostrar en consola
        """
        if not resultado['exito']:
            return f"ERROR: {resultado['error']}"
        
        texto = "=" * 100 + "\n"
        texto += "CALCULADORA VLSM - RESULTADOS\n"
        texto += "=" * 100 + "\n\n"
        
        texto += f"Red Base: {resultado['red_base']}\n"
        texto += f"Espacio Total Disponible: {resultado['espacio_total']} direcciones\n\n"
        
        # Tabla de subredes
        texto += "-" * 100 + "\n"
        texto += f"{'Subred':<20} {'Red':<18} {'Máscara':<18} {'Rango Hosts':<30} {'Broadcast':<15}\n"
        texto += "-" * 100 + "\n"
        
        for subred in resultado['subredes']:
            rango = f"{subred.primera_host} - {subred.ultima_host}"
            texto += (f"{subred.nombre:<20} {subred.red + '/' + str(subred.prefijo):<18} "
                     f"{subred.mascara:<18} {rango:<30} {subred.broadcast:<15}\n")
        
        texto += "-" * 100 + "\n\n"
        
        # Detalles de cada subred
        texto += "DETALLES POR SUBRED:\n"
        texto += "=" * 100 + "\n"
        
        for i, subred in enumerate(resultado['subredes'], 1):
            texto += f"\n{i}. {subred.nombre}\n"
            texto += f"   Hosts requeridos:    {subred.hosts_requeridos}\n"
            texto += f"   Hosts disponibles:   {subred.hosts_disponibles}\n"
            texto += f"   Espacio desperdiciado: {subred.espacio_desperdiciado} hosts\n"
            texto += f"   Eficiencia: {((subred.hosts_requeridos/subred.hosts_disponibles)*100):.2f}%\n"
        
        # Estadísticas generales
        texto += "\n" + "=" * 70 + "\n"
        texto += "ESTADÍSTICAS\n"
        texto += "=" * 70 + "\n"
        texto += f"Espacio utilizado:        {resultado['espacio_utilizado']} direcciones\n"
        texto += f"Espacio libre:            {resultado['espacio_libre']} direcciones\n"
        texto += f"Hosts totales requeridos: {resultado['hosts_totales_requeridos']}\n"
        texto += f"Hosts totales asignados:  {resultado['hosts_totales_asignados']}\n"
        texto += f"Eficiencia global:        {resultado['eficiencia']}%\n"
        texto += "=" * 70 + "\n"
        
        return texto