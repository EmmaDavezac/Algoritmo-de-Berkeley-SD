import time

# --- CONFIGURACIÓN ---
# Tiempo de red simulado (segundos)
LATENCIA_RED = 2 

class Reloj:
    def __init__(self, id, hora_inicial):
        self.id = id
        self.hora = hora_inicial
        print(f"[{self.id}] Init. Hora: {self.formato_hora()}")

    def formato_hora(self):
        """Convierte hora en segundos a HH:MM:SS."""
        horas = int(self.hora // 3600)
        minutos = int((self.hora % 3600) // 60)
        segundos = int(self.hora % 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def obtener_hora(self):
        return self.hora

    def ajustar_hora(self, ajuste):
        """Aplica el ajuste (segundos)."""
        self.hora += ajuste
        print(f"[{self.id}] Ajuste: {ajuste:.2f} s.")
        print(f"[{self.id}] Nueva Hora: {self.formato_hora()}")

# Inicialización de las computadoras (horas en segundos)
# C1 (Maestro): 10:00:00
# C2 (Esclavo): 10:10:00
# C3 (Esclavo): 09:50:00

C1 = Reloj("C1 (Maestro)", 36000.0)
C2 = Reloj("C2 (Esclavo)", 36600.0)
C3 = Reloj("C3 (Esclavo)", 35400.0)

ESCLAVOS = [C2, C3]

def simular_envio_y_respuesta(coordinador, esclavo):
    """Simula solicitud/respuesta y retorna la hora corregida del esclavo."""
    
    hora_envio_c1 = coordinador.obtener_hora()
    print(f"\n[{coordinador.id}] Solicitud a {esclavo.id} @ {coordinador.formato_hora()}")

    # Avance del reloj del esclavo por la latencia de ida
    esclavo.hora += LATENCIA_RED
    
    hora_esclavo_respuesta = esclavo.obtener_hora()
    
    # Avance del reloj del coordinador por la latencia de vuelta
    coordinador.hora += LATENCIA_RED
    
    hora_recepcion_c1 = coordinador.obtener_hora()
    
    rtt = (hora_recepcion_c1 - hora_envio_c1)
    
    # Corrección de la hora: se resta la mitad del RTT al tiempo de respuesta del esclavo
    hora_corregida = hora_esclavo_respuesta - (rtt / 2)
    
    print(f"[{esclavo.id}] Responde con {esclavo.formato_hora()}.")
    print(f"[{coordinador.id}] Recibido @ {coordinador.formato_hora()}. RTT: {rtt:.2f}s.")
    
    return hora_corregida

def algoritmo_berkeley(coordinador, esclavos):
    """Lógica principal del Algoritmo de Berkeley."""
    
    horas_corregidas = []
    
    # 1. Recopilación de tiempos corregidos de los esclavos
    for esclavo in esclavos:
        hora_corregida = simular_envio_y_respuesta(coordinador, esclavo)
        horas_corregidas.append(hora_corregida)

    # 2. Agregar hora final del Coordinador
    hora_coordinador_final = coordinador.obtener_hora()
    horas_corregidas.append(hora_coordinador_final)
    
    print(f"\n--- CALCULO ---")
    
    # 3. Cálculo del Tiempo Promedio
    tiempo_promedio = sum(horas_corregidas) / len(horas_corregidas)
    
    print(f"Tiempo Promedio: {Reloj('', tiempo_promedio).formato_hora()}")

    # 4. Cálculo y Aplicación de Ajustes
    print(f"\n--- AJUSTES ---")
    
    # Ajuste del Coordinador
    ajuste_c1 = tiempo_promedio - hora_coordinador_final
    coordinador.ajustar_hora(ajuste_c1)

    # Ajuste de los Esclavos
    for i, esclavo in enumerate(esclavos):
        hora_corregida_esclavo = horas_corregidas[i]
        ajuste_esclavo = tiempo_promedio - hora_corregida_esclavo
        
        # Simular avance por la latencia de envío del ajuste
        esclavo.hora += LATENCIA_RED 
        coordinador.hora += LATENCIA_RED 
        
        esclavo.ajustar_hora(ajuste_esclavo)
        
    print("\n--- FIN SINCRONIZACIÓN ---")


# --- EJECUCIÓN ---

# Simular deriva inicial antes de la sincronización
C1.hora += 30 
C2.hora += 30
C3.hora += 30

print("Horas iniciales (después de deriva):")
print(f"C1: {C1.formato_hora()}")
print(f"C2: {C2.formato_hora()}")
print(f"C3: {C3.formato_hora()}")

algoritmo_berkeley(C1, ESCLAVOS)
