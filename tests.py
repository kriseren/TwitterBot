# Check if a String contains a substring
string = "Hey @KriserenBot! Recomiéndame una canción porfa"
keywords1 = ["canción soy","canción sería"]
keywords2 = ["Recomiéndame","recomiendas"]


if keywords1[0] in string or keywords1[1] in string:
    print("Serías esta canción...")
elif keywords2[0] in string or keywords2[1] in string:
    print("Te recomiendo que oigas...")
else:
    print("No te he entendido, prueba a pedirme qué canción serías o qué canción te recomiendo")
