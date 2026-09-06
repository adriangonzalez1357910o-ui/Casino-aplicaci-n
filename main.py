import random
print("¡CASINO!")
d = int(input("Ingrese la cantidad de fichas que desea comprar: "))
w = (11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2)
q = 0
x = 0
t = 50
ñ = 0
puntos1 = 0
puntos2 = 0
puntos3 = 0
while True:
    print("Black Jack, Ruleta, Máquina Tragamonedas")
    k = str(input("Elija el juego en el que desea probar su suerte: "))
    if k == ("Black Jack"):
        g = int(input("Ingrese la cantidad de fichas que desea apostar: "))
        m = "Si"
        h = 0
        h1 = 0
        h2 = 0
        while h < 21:
            dealer = random.choice(w)
            h += dealer
            q += 1
            if q == 1:
                print("La carta que revela el dealer es: ", dealer)
        while h1 < 21:
            jugador1 = random.choice(w)
            h1 += jugador1
        for i in range(2):
            jugador2 = random.choice(w)
            h2 += jugador2
            print(jugador2)
        while m == "Si":
            m = str(input("Desea robar una carta más: "))
            if m == "Si":
                jugador2 = random.choice(w)
                h2 += jugador2
                print(jugador2)
        if h <= 21:
            puntos1 = h
        elif h1 <= 21:
            puntos2 = h1
        elif h2 <= 21:
            puntos3 = h2
        ganador = max(puntos1, puntos2, puntos3)
        if ganador == puntos1:
            print("¡El ganador es el dealer!")
            d -= g
        elif ganador == puntos2:
            print("¡Ha ganado la computadora!")
            d -= g
        elif ganador == puntos3:
            print("¡Has ganado y has duplicado tus fichas!")
            d += g
        print("Usted tiene", d, "fichas")
        if d >= ñ:
            print("Tiene la suficiente cantidad de fichas para pagar su deuda")
            r = str(input("¿Desea pagar su deuda?: "))
            if r == "Si":
                t += ñ
                d -= ñ
                print("¡Ha pagado exitosamente su deuda! Le quedan: ", d, "fichas")
    elif k == ("Ruleta"):
        g = int(input("Ingrese la cantidad de fichas que desea apostar: "))
        n  = random.randint(0, 36)
        a = int(input("Ingrese un número entre 0 y 36: "))
        if a == n:
            print("¡HAS GANADO EL GRAN PREMIO!")
            d += 50
        elif a % 2 == 0 and n % 2 == 0:
            print("¡Has ganado un premio menor!")
            d += 25
        elif a % 3 == 0 and n % 3 == 0:
            print("¡Has ganado un premio menor!")
            d += 25
        else:
            print("Has perdido")
            d -= g
        print("Usted tiene", d, "fichas")
        if d >= ñ:
            print("Tiene la suficiente cantidad de fichas para pagar su deuda")
            r = str(input("¿Desea pagar su deuda?: "))
            if r == "Si":
                t += ñ
                d -= ñ
                print("¡Ha pagado exitosamente su deuda! Le quedan: ", d, "fichas")
    elif k == ("Máquina Tragamonedas"):
        g = int(input("Ingrese la cantidad de fichas que desea apostar: "))
        opciones = ["Cereza", "Limón", "Estrella"]
        resultado1 = random.choice(opciones)
        resultado2 = random.choice(opciones)
        resultado3 = random.choice(opciones)
        if resultado1 and resultado2 == resultado3:
            print("¡Jackpot!")
            d += 60
        elif resultado1 == resultado2 or resultado2 == resultado3 or resultado1 == resultado3:
            print("¡Premio!")
            d += 30
        else:
            print("¡Has perdido!")
            d -= g
        print("Usted tiene", d, "fichas")
        if d >= ñ:
            print("Tiene la suficiente cantidad de fichas para pagar su deuda")
            r = str(input("¿Desea pagar su deuda?: "))
            if r == "Si":
                t += ñ
                d -= ñ
                print("¡Ha pagado exitosamente su deuda! Le quedan: ", d, "fichas")
    z = str(input("¿Desea dejar de jugar y salir del casino?: "))
    if z == "Si":
        if ñ > 0:
            print("Recuerde que tiene una deuda de: ", ñ, "fichas")
        print("Gracias por haber jugado y vuelva pronto")
        break
    while d <= 0:
        if  d == 0 and t == 0:
            print("¡Has sido expulsado del Casino por tus deudas!")
            break
        y = str(input("Se ha quedado sin fichas, ¿desea deberle al Casino para seguir jugando?: "))
        if y == "Si":
            print("La cantidad de fichas que el Casino tiene disponible para prestar es: ", t)
            d = int(input("Ingrese la cantidad de fichas que desea prestar del Casino: "))
            t -= d
            ñ += t
