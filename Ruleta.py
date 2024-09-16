import time
import threading
import random
import sys, io
import os

ELEMENTOS = ["⭐", "🍄", "🌼"]
PUNTAJES = [5, 3, 2]

tiros = 3
girar = True
puntos = 0

def main():
    global puntos, tiros, girar
    mostrar_puntajes(ELEMENTOS, PUNTAJES)
    
    if not iniciar_juego():
        return
    
    while True:
        inicio = threading.Event()
        hilo_girar = threading.Thread(target=girar_ruleta, daemon=False, args=(ELEMENTOS, inicio))
        hilo_tirar = threading.Thread(target=tirar, daemon=False, args=(inicio, ))
        hilo_girar.start()
        hilo_tirar.start()
        
        inicio.set()
        hilo_girar.join()
        hilo_tirar.join()
        
        print(f"Puntos acumulados: {puntos}")
        
        if not jugar_nuevamente():
            break
        
        tiros = 3
        girar = True
        inicio.clear()
        os.system('cls')

def girar_ruleta(elementos, inicio):
    global elemento_actual
    while girar:
        inicio.wait()
        elemento_actual = random.choice(elementos)
        sys.stdout.write(f'\r{elemento_actual}')
        sys.stdout.flush()
        time.sleep(.5)

def tirar(inicio):
    global tiros, girar, puntos
    elementos_tirados = []

    while tiros > 0:
        inicio.wait()
        input("    Presiona Enter...")
        tiros -= 1
        elementos_tirados.append(elemento_actual)
        if len(elementos_tirados) == 3:
            if elementos_tirados.count(elementos_tirados[0]) == len(elementos_tirados):
                puntos += obtener_puntos(elementos_tirados[0])
                print("Felicidades! Acertaste los 3")
            else:
                print("No coincidieron los 3 elementos. Intenta de nuevo.")
            elementos_tirados = []
    girar = False

def obtener_puntos(elemento):
    indice = ELEMENTOS.index(elemento)
    return PUNTAJES[indice]

def mostrar_puntajes(elementos, puntajes):
    for i in range(len(elementos)):
        print(f"{elementos[i]} = {puntajes[i]} pts")

def iniciar_juego():
    inicio = input("Deseas iniciar la ruleta (s/n)...")
    return inicio.lower() == "s"

def jugar_nuevamente():
    respuesta = input("¿Quieres volver a jugar? (s/n)...")
    return respuesta.lower() == "s"

if __name__ == "__main__":
    main()
    