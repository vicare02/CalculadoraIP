"""
Módulo: cidr_calculator.py

"""

from typing import Dict, Optional
from ip_utils import (
    validar_direccion_ip,
    validar_prefijo,
    calcular_direccion_red,
    calcular_broadcast,
    calcular_numero_hosts,
    calcular_rango_hosts,
    prefijo_a_mascara,
    ip_a_binario,
    parsear_entrada_ip_cidr
)


class CalculadoraCIDR:
    """
    Clase para realizar cálculos de subredes usando notación CIDR.
    
    Descripción:
        Proporciona funcionalidad completa para analizar una red CIDR,
        incluyendo dirección de red, broadcast, rango de hosts,
        máscara de subred y representaciones binarias.
    
    Observaciones:
        - Soporta entrada en formato IP/prefijo o IP máscara
        - Valida todas las entradas antes de calcular
        - Retorna diccionarios con resultados estructurados
    """
    
    def __init__(self):
        """
        Constructor de la clase CalculadoraCIDR.
        
        Observaciones:
            - No requiere parámetros de inicialización
            - Todos los cálculos son métodos estáticos o de instancia sin estado
        """
        pass
    
    def calcular(self, entrada: str, incluir_binario: bool = False) -> Dict:
        """
        Realiza todos los cálculos CIDR para una entrada dada.
        
        Entradas:
            entrada (str): Dirección IP con prefijo (ej: "192.168.1.0/24")
            incluir_binario (bool): Si True, incluye representaciones binarias
        
        Salidas:
            Dict: Diccionario con todos los resultados del cálculo:
                - exito (bool): Indica si el cálculo fue exitoso
                - error (str): Mensaje de error si exito = False
                - ip_original (str): IP ingresada
                - prefijo (int): Longitud del prefijo
                - direccion_red (str): Dirección de red calculada
                - mascara_decimal (str): Máscara en formato decimal punteado
                - primera_host (str): Primera IP utilizable
                - ultima_host (str): Última IP utilizable
                - broadcast (str): Dirección de broadcast
                - total_hosts (int): Total de direcciones en el bloque
                - hosts_utilizables (int): Hosts utilizables (total - 2)
                - binario (dict, opcional): Representaciones binarias
        
        Observaciones:
            - Valida la entrada antes de realizar cálculos
            - Maneja errores y retorna mensajes descriptivos
            - El campo 'binario' solo se incluye si incluir_binario = True
        
        Descripción del algoritmo:
            1. Parsear y validar entrada
            2. Calcular dirección de red
            3. Calcular broadcast
            4. Calcular rango de hosts
            5. Obtener máscara de subred
            6. Calcular número de hosts
            7. (Opcional) Generar representaciones binarias
        """
        # Paso 1: Parsear entrada
        datos_entrada = parsear_entrada_ip_cidr(entrada)
        
        if datos_entrada is None:
            return {
                'exito': False,
                'error': 'Formato de entrada inválido. Use: IP/prefijo (ej: 192.168.1.0/24) o IP máscara'
            }
        
        ip, prefijo = datos_entrada
        
        # Paso 2: Validar IP y prefijo
        if not validar_direccion_ip(ip):
            return {
                'exito': False,
                'error': f'Dirección IP inválida: {ip}'
            }
        
        if not validar_prefijo(prefijo):
            return {
                'exito': False,
                'error': f'Prefijo inválido: {prefijo}. Debe estar entre 0 y 32'
            }
        
        # Paso 3: Calcular dirección de red
        direccion_red = calcular_direccion_red(ip, prefijo)
        
        # Paso 4: Calcular broadcast
        broadcast = calcular_broadcast(direccion_red, prefijo)
        
        # Paso 5: Calcular rango de hosts
        primera_host, ultima_host = calcular_rango_hosts(direccion_red, prefijo)
        
        # Paso 6: Obtener máscara
        mascara_decimal = prefijo_a_mascara(prefijo)
        
        # Paso 7: Calcular número de hosts
        hosts_utilizables = calcular_numero_hosts(prefijo)
        total_hosts = 2 ** (32 - prefijo)
        
        # Construir resultado
        resultado = {
            'exito': True,
            'ip_original': ip,
            'prefijo': prefijo,
            'mascara_decimal': mascara_decimal,
            'direccion_red': direccion_red,
            'primera_host': primera_host,
            'ultima_host': ultima_host,
            'broadcast': broadcast,
            'total_hosts': total_hosts,
            'hosts_utilizables': hosts_utilizables
        }
        
        # Paso 8: Agregar representaciones binarias si se solicitan
        if incluir_binario:
            resultado['binario'] = {
                'direccion_red': ip_a_binario(direccion_red),
                'mascara': ip_a_binario(mascara_decimal),
                'primera_host': ip_a_binario(primera_host),
                'ultima_host': ip_a_binario(ultima_host),
                'broadcast': ip_a_binario(broadcast)
            }
        
        return resultado
    
    def validar_entrada(self, entrada: str) -> Dict:
        """
        Valida una entrada sin realizar cálculos completos.
        
        Entradas:
            entrada (str): Cadena a validar
        
        Salidas:
            Dict: Diccionario con:
                - valida (bool): True si la entrada es válida
                - mensaje (str): Mensaje descriptivo
                - ip (str, opcional): IP extraída si es válida
                - prefijo (int, opcional): Prefijo extraído si es válido
        
        Observaciones:
            - Útil para validación en tiempo real en la UI
            - No realiza cálculos pesados
        """
        datos_entrada = parsear_entrada_ip_cidr(entrada)
        
        if datos_entrada is None:
            return {
                'valida': False,
                'mensaje': 'Formato inválido. Use: IP/prefijo o IP máscara'
            }
        
        ip, prefijo = datos_entrada
        
        if not validar_direccion_ip(ip):
            return {
                'valida': False,
                'mensaje': f'Dirección IP inválida: {ip}'
            }
        
        if not validar_prefijo(prefijo):
            return {
                'valida': False,
                'mensaje': f'Prefijo inválido: /{prefijo}'
            }
        
        return {
            'valida': True,
            'mensaje': 'Entrada válida',
            'ip': ip,
            'prefijo': prefijo
        }
    
    def obtener_informacion_clase(self, ip: str) -> str:
        """
        Determina la clase de una dirección IP (A, B, C, D, E).
        
        Entradas:
            ip (str): Dirección IP en formato decimal punteado
        
        Salidas:
            str: Clase de la IP ('A', 'B', 'C', 'D', 'E' o 'Desconocida')
        
        Observaciones:
            - Clase A: 1-126 (primer octeto)
            - Clase B: 128-191
            - Clase C: 192-223
            - Clase D: 224-239 (multicast)
            - Clase E: 240-255 (experimental)
            - 127.x.x.x es para pruebas y no se clasifica
    
        """
        if not validar_direccion_ip(ip):
            return 'Desconocida'
        
        primer_octeto = int(ip.split('.')[0])
        
        if 1 <= primer_octeto <= 126:
            return 'A'
        elif 128 <= primer_octeto <= 191:
            return 'B'
        elif 192 <= primer_octeto <= 223:
            return 'C'
        elif 224 <= primer_octeto <= 239:
            return 'D (Multicast)'
        elif 240 <= primer_octeto <= 255:
            return 'E (Experimental)'
        else:
            return 'Desconocida'
    
    def es_ip_privada(self, ip: str) -> bool:
        """
        Determina si una IP pertenece a un rango privado (RFC 1918).
        
        Entradas:
            ip (str): Dirección IP a verificar
        
        Salidas:
            bool: True si es privada, False si es pública
        
        Observaciones:
            - Rangos privados:
                * 10.0.0.0/8 (Clase A)
                * 172.16.0.0/12 (Clase B)
                * 192.168.0.0/16 (Clase C)
        
        """
        if not validar_direccion_ip(ip):
            return False
        
        octetos = [int(x) for x in ip.split('.')]
        
        # 10.0.0.0/8
        if octetos[0] == 10:
            return True
        
        # 172.16.0.0/12
        if octetos[0] == 172 and 16 <= octetos[1] <= 31:
            return True
        
        # 192.168.0.0/16
        if octetos[0] == 192 and octetos[1] == 168:
            return True
        
        return False
    
    def formatear_resultado(self, resultado: Dict) -> str:
        """
        Formatea un resultado de cálculo como texto legible.
        
        Entradas:
            resultado (Dict): Diccionario retornado por calcular()
        
        Salidas:
            str: Texto formateado con todos los datos
        
        Observaciones:
            - Útil para mostrar en consola o archivos de texto
            - Incluye representaciones binarias si están disponibles
        
        """
        if not resultado['exito']:
            return f"ERROR: {resultado['error']}"
        
        texto = "=" * 60 + "\n"
        texto += "CALCULADORA IP CIDR - RESULTADOS\n"
        texto += "=" * 60 + "\n\n"
        
        texto += f"IP Original:        {resultado['ip_original']}/{resultado['prefijo']}\n"
        texto += f"Máscara de Subred:  {resultado['mascara_decimal']} (/{resultado['prefijo']})\n"
        texto += f"Dirección de Red:   {resultado['direccion_red']}\n"
        texto += f"Primera Host:       {resultado['primera_host']}\n"
        texto += f"Última Host:        {resultado['ultima_host']}\n"
        texto += f"Broadcast:          {resultado['broadcast']}\n"
        texto += f"Total Direcciones:  {resultado['total_hosts']}\n"
        texto += f"Hosts Utilizables:  {resultado['hosts_utilizables']}\n"
        
        # Agregar información adicional
        clase = self.obtener_informacion_clase(resultado['ip_original'])
        es_privada = self.es_ip_privada(resultado['ip_original'])
        
        texto += f"Clase de IP:        {clase}\n"
        texto += f"Tipo de IP:         {'Privada' if es_privada else 'Pública'}\n"
        
        # Agregar representaciones binarias si existen
        if 'binario' in resultado:
            texto += "\n" + "-" * 60 + "\n"
            texto += "REPRESENTACIÓN BINARIA\n"
            texto += "-" * 60 + "\n"
            texto += f"Red:       {resultado['binario']['direccion_red']}\n"
            texto += f"Máscara:   {resultado['binario']['mascara']}\n"
            texto += f"1er Host:  {resultado['binario']['primera_host']}\n"
            texto += f"Últ Host:  {resultado['binario']['ultima_host']}\n"
            texto += f"Broadcast: {resultado['binario']['broadcast']}\n"
        
        texto += "\n" + "=" * 60 + "\n"
        
        return texto