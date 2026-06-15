"""
Módulo: ip_utils.py

Copyright (c) 2025 Demian Romero Bautista y Renata García Resendiz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.


Descripción: Libreria de funciones utilitarias para el manejo y conversión de direcciones IP
Grupo: 5CV1
Asignatura: Redes de Computadoras
Fecha: Diciembre 2025
"""

import re
from typing import Tuple, Optional


def validar_direccion_ip(ip: str) -> bool:
    """
    Valida si una cadena es una dirección IP válida en formato decimal punteado.
    
    Entradas:
        ip (str): Dirección IP en formato "x.x.x.x"
    
    Salidas:
        bool: True si es válida, False en caso contrario
    
    Observaciones:
        - Verifica que tenga 4 octetos
        - Cada octeto debe estar entre 0 y 255
        - No permite espacios ni caracteres especiales
    
    """
    patron = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    coincidencia = re.match(patron, ip)
    
    if not coincidencia:
        return False
    
    octetos = [int(x) for x in coincidencia.groups()]
    
    # Verificar que cada octeto esté en el rango válido
    return all(0 <= octeto <= 255 for octeto in octetos)


def validar_prefijo(prefijo: int) -> bool:
    """
    Valida si un prefijo de red es válido.
    
    Entradas:
        prefijo (int): Longitud del prefijo (notación CIDR)
    
    Salidas:
        bool: True si está entre 0 y 32, False en caso contrario
    
    Observaciones:
        - El prefijo representa la cantidad de bits de red
        - Debe estar en el rango [0, 32] para IPv4

    """
    return 0 <= prefijo <= 32


def ip_a_entero(ip: str) -> int:
    """
    Convierte una dirección IP en formato decimal punteado a su representación entera.
    
    Entradas:
        ip (str): Dirección IP en formato "x.x.x.x"
    
    Salidas:
        int: Representación entera de 32 bits de la IP
    
    Observaciones:
        - Facilita operaciones aritméticas con IPs
        - Usa desplazamiento de bits para la conversión
        - No valida la IP (debe validarse antes)
    
    Descripción del algoritmo:
        1. Divide la IP en octetos
        2. Cada octeto se desplaza según su posición
        3. Se suman todos los valores desplazados
    
    """
    octetos = ip.split('.')
    valor_entero = 0
    
    for i, octeto in enumerate(octetos):
        # Desplazar cada octeto a su posición correspondiente
        desplazamiento = (3 - i) * 8
        valor_entero += int(octeto) << desplazamiento
    
    return valor_entero


def entero_a_ip(numero: int) -> str:
    """
    Convierte un número entero de 32 bits a formato IP decimal punteado.
    
    Entradas:
        numero (int): Número entero representando una IP (0 a 4294967295)
    
    Salidas:
        str: Dirección IP en formato "x.x.x.x"
    
    Observaciones:
        - Inverso de ip_a_entero()
        - Usa máscaras y desplazamiento de bits
        - Asume que el número está en rango válido
    
    Descripción del algoritmo:
        1. Extrae cada octeto con máscara 0xFF
        2. Desplaza 8 bits para obtener el siguiente octeto
        3. Formatea como cadena con puntos
    """
    octetos = []
    
    for i in range(4):
        # Extraer octeto de derecha a izquierda
        desplazamiento = (3 - i) * 8
        octeto = (numero >> desplazamiento) & 0xFF
        octetos.append(str(octeto))
    
    return '.'.join(octetos)


def prefijo_a_mascara(prefijo: int) -> str:
    """
    Convierte una longitud de prefijo CIDR a máscara de subred decimal punteada.
    
    Entradas:
        prefijo (int): Longitud del prefijo (0-32)
    
    Salidas:
        str: Máscara en formato decimal punteado
    
    Observaciones:
        - Genera máscara con 'prefijo' bits en 1 seguidos de 0s
        - /24 = 255.255.255.0
        - /16 = 255.255.0.0
    
    Descripción del algoritmo:
        1. Crea máscara con todos los bits en 1
        2. Desplaza a la derecha (32 - prefijo) posiciones
        3. Invierte para obtener los bits de red
        4. Aplica máscara de 32 bits
    """
    # Crear máscara: llenar 'prefijo' bits con 1s desde la izquierda
    mascara = (0xFFFFFFFF << (32 - prefijo)) & 0xFFFFFFFF
    return entero_a_ip(mascara)


def mascara_a_prefijo(mascara: str) -> int:
    """
    Convierte una máscara de subred decimal punteada a longitud de prefijo CIDR.
    
    Entradas:
        mascara (str): Máscara en formato "x.x.x.x"
    
    Salidas:
        int: Longitud del prefijo (cantidad de bits en 1)
    
    Observaciones:
        - Cuenta los bits consecutivos en 1 desde la izquierda
        - Asume máscara válida (bits contiguos)
    """
    mascara_entero = ip_a_entero(mascara)
    
    # Contar bits en 1 desde la izquierda
    prefijo = 0
    for i in range(32):
        if mascara_entero & (1 << (31 - i)):
            prefijo += 1
        else:
            break
    
    return prefijo


def ip_a_binario(ip: str) -> str:
    """
    Convierte una dirección IP a su representación binaria.
    
    Entradas:
        ip (str): Dirección IP en formato decimal punteado
    
    Salidas:
        str: Representación binaria con formato "xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx"
    
    Observaciones:
        - Cada octeto se representa con 8 bits
        - Útil para visualización y aprendizaje
        - Incluye puntos para facilitar lectura
    """
    octetos = ip.split('.')
    binarios = [format(int(octeto), '08b') for octeto in octetos]
    return '.'.join(binarios)


def calcular_direccion_red(ip: str, prefijo: int) -> str:
    """
    Calcula la dirección de red aplicando la máscara a la IP dada.
    
    Entradas:
        ip (str): Dirección IP en formato decimal punteado
        prefijo (int): Longitud del prefijo CIDR
    
    Salidas:
        str: Dirección de red en formato decimal punteado
    
    Observaciones:
        - Aplica operación AND bit a bit entre IP y máscara
        - Pone a 0 todos los bits de host
        - Es la primera dirección del bloque de red
    
    Descripción del algoritmo:
        1. Convierte IP a entero
        2. Genera máscara desde prefijo
        3. Aplica AND bit a bit
        4. Convierte resultado a formato IP
    """
    ip_entero = ip_a_entero(ip)
    mascara_entero = (0xFFFFFFFF << (32 - prefijo)) & 0xFFFFFFFF
    
    direccion_red = ip_entero & mascara_entero
    
    return entero_a_ip(direccion_red)


def calcular_broadcast(ip_red: str, prefijo: int) -> str:
    """
    Calcula la dirección de broadcast para una red dada.
    
    Entradas:
        ip_red (str): Dirección de red
        prefijo (int): Longitud del prefijo CIDR
    
    Salidas:
        str: Dirección de broadcast
    
    Observaciones:
        - Es la última dirección del bloque de red
        - Todos los bits de host están en 1
        - Se usa para enviar mensajes a todos los hosts de la red
    
    Descripción del algoritmo:
        1. Convierte dirección de red a entero
        2. Calcula tamaño del bloque (2^bits_host)
        3. Suma (tamaño - 1) a la dirección de red
    """
    ip_entero = ip_a_entero(ip_red)
    bits_host = 32 - prefijo
    tamano_bloque = 2 ** bits_host
    
    broadcast = ip_entero + tamano_bloque - 1
    
    return entero_a_ip(broadcast)


def calcular_numero_hosts(prefijo: int) -> int:
    """
    Calcula el número de hosts utilizables en una red.
    
    Entradas:
        prefijo (int): Longitud del prefijo CIDR
    
    Salidas:
        int: Número de hosts utilizables
    
    Observaciones:
        - Se restan 2 direcciones: red y broadcast
        - Fórmula: 2^(32-prefijo) - 2
        - Para /32 el resultado es 1 host (caso especial)
        - Para /31 son 2 hosts (RFC 3021 - enlaces punto a punto)
    """
    bits_host = 32 - prefijo
    
    if prefijo == 32:
        return 1  # Host único
    elif prefijo == 31:
        return 2  # Enlace punto a punto (RFC 3021)
    else:
        return (2 ** bits_host) - 2


def calcular_rango_hosts(ip_red: str, prefijo: int) -> Tuple[str, str]:
    """
    Calcula el rango de direcciones IP utilizables para hosts.
    
    Entradas:
        ip_red (str): Dirección de red
        prefijo (int): Longitud del prefijo CIDR
    
    Salidas:
        Tuple[str, str]: Tupla con (primera_ip_host, última_ip_host)
    
    Observaciones:
        - Primera IP: dirección_red + 1
        - Última IP: dirección_broadcast - 1
        - Para /31 y /32 hay casos especiales
    """
    ip_entero = ip_a_entero(ip_red)
    
    primera_host = ip_entero + 1
    
    broadcast_entero = ip_a_entero(calcular_broadcast(ip_red, prefijo))
    ultima_host = broadcast_entero - 1
    
    return (entero_a_ip(primera_host), entero_a_ip(ultima_host))


def parsear_entrada_ip_cidr(entrada: str) -> Optional[Tuple[str, int]]:
    """
    Parsea una entrada en formato "IP/prefijo" o "IP máscara".
    
    Entradas:
        entrada (str): Cadena con formato "192.168.1.0/24" o "192.168.1.0 255.255.255.0"
    
    Salidas:
        Optional[Tuple[str, int]]: Tupla (ip, prefijo) o None si es inválida
    
    Observaciones:
        - Soporta notación CIDR (/) y máscara decimal
        - Valida tanto IP como prefijo/máscara
        - Retorna None en caso de error
    """
    entrada = entrada.strip()
    
    # Intentar formato CIDR (IP/prefijo)
    if '/' in entrada:
        partes = entrada.split('/')
        if len(partes) != 2:
            return None
        
        ip = partes[0].strip()
        try:
            prefijo = int(partes[1].strip())
        except ValueError:
            return None
        
        if not validar_direccion_ip(ip) or not validar_prefijo(prefijo):
            return None
        
        return (ip, prefijo)
    
    # Intentar formato IP + máscara
    elif ' ' in entrada:
        partes = entrada.split()
        if len(partes) != 2:
            return None
        
        ip = partes[0].strip()
        mascara = partes[1].strip()
        
        if not validar_direccion_ip(ip) or not validar_direccion_ip(mascara):
            return None
        
        prefijo = mascara_a_prefijo(mascara)
        return (ip, prefijo)
    
    return None