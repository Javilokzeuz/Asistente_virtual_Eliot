from core.agent import EliotAgent


def main():
    print("=" * 50)
    print("        ELIOT - ASISTENTE VIRTUAL")
    print("=" * 50)
    print("Eliot está iniciando...")
    print("Escribe 'salir' para cerrar Eliot.")
    print()

    eliot = EliotAgent()

    while True:
        mensaje = input("Tú: ")

        if mensaje.lower().strip() == "salir":
            print("Eliot: Hasta luego, señor.")
            break

        respuesta = eliot.preguntar(mensaje)

        print(f"Eliot: {respuesta}")
        print()


if __name__ == "__main__":
    main()