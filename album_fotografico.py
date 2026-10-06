def carica_da_file(file_path):

    try:
        f = open(file_path, "r")
        righe = f.readlines()
        f.close()
    except FileNotFoundError:
        return None

    album = []

    if len(righe) <= 1:
        return album

    for riga in righe[1:]:
        riga = riga.strip()
        if riga == "":
            continue

        parti = riga.split(",")
        codice = parti[0].strip()
        titolo = parti[1].strip()
        autore = parti[2].strip()
        mese = int(parti[3].strip())
        anno = int(parti[4].strip())

        foto = {
            "codice": codice,
            "titolo": titolo,
            "autore": autore,
            "mese": mese,
            "anno": anno
        }

        anno_trovato = False
        for elemento in album:
            if elemento[0] == anno:
                elemento[1].append(foto)
                anno_trovato = True
                break

        if not anno_trovato:
            album.append([anno, [foto]])

    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """2. AGGIUNGI UNA NUOVA FOTO
    """
    if mese < 1 or mese > 12:
        return None

    if album is None:
        return None

    for elemento in album:
        for foto in elemento[1]:
            if foto["codice"] == codice:
                return None

    try:
        f = open(file_path, "a")
        f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
        f.close()
    except FileNotFoundError:
        return None

    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    anno_trovato = False
    for elemento in album:
        if elemento[0] == anno:
            elemento[1].append(nuova_foto)
            anno_trovato = True
            break

    if not anno_trovato:
        album.append([anno, [nuova_foto]])

    return nuova_foto


def cerca_foto(album, codice):
    """3. CERCA UNA FOTO PER CODICE
    """
    if album is None:
        return None

    for elemento in album:
        for foto in elemento[1]:
            if foto["codice"] == codice:

                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """4. ELENCO FOTO DI UN ANNO (ORDINATO PER TITOLO)
    """
    if album is None:
        return None

    for elemento in album:
        if elemento[0] == anno:
            titoli = []
            for foto in elemento[1]:
                titoli.append(foto["titolo"])

            titoli.sort()
            return titoli

    return None


def main():
    album = None
    # Nome predefinito del file CSV
    file_path = "album_foto.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            input_file = input(f"Inserisci il nome del file [premi INVIO per usare '{file_path}']: ").strip()
            if input_file != "":
                file_path = input_file

            album = carica_da_file(file_path)

            if album is not None:
                print(f"--> SUCESSO: Album caricato da '{file_path}'!")
            else:
                print(
                    f"--> ERRORE: File '{file_path}' non trovato! Controlla che sia nella stessa cartella del programma Python.")

        elif scelta == "2":
            if album is None:
                print("--> PRIMA devi caricare l'album da file (Seleziona l'opzione 1).")
                continue

            codice = input("Codice (es. P016): ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()

            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("--> ERRORE: Mese e Anno devono essere numeri interi!")
                continue

            risultato = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if risultato:
                print("--> FOTO AGGIUNTA CON SUCCESSO!")
            else:
                print("--> ERRORE: Impossibile aggiungere la foto (codice già presente o mese non valido).")

        elif scelta == "3":
            if album is None:
                print("--> PRIMA devi caricare l'album da file (Seleziona l'opzione 1).")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)

            if risultato:
                print(f"\nRisultato: {risultato}")
            else:
                print("--> FOTO NON TROVATA.")

        elif scelta == "4":
            if album is None:
                print("--> PRIMA devi caricare l'album da file (Seleziona l'opzione 1).")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("--> ERRORE: L'anno deve essere un numero intero!")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)

            if titoli is not None:
                print(f"\nFoto del {anno} (in ordine alfabetico per titolo):")
                for t in titoli:
                    print(f"- {t}")
            else:
                print(f"--> Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma. Ciao!")
            break

        else:
            print("--> Opzione non valida! Scegli un numero tra 1 e 5.")


if __name__ == "__main__":
    main()