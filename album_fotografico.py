def carica_da_file(file_path):
    """1. CARICA ALBUM DA FILE
    Apre il file CSV, legge le righe e raggruppa le foto per anno.
    Se il file non esiste, restituisce None (gestione eccezione FileNotFoundError).
    """
    try:
        f = open(file_path, "r", encoding="utf-8")
        righe = f.readlines()
        f.close()
    except FileNotFoundError:
        return None

    album = []

    # Se il file ha solo l'intestazione o è vuoto, restituiamo un album vuoto
    if len(righe) <= 1:
        return album

    # Saltiamo la prima riga di intestazione (codice,titolo,autore,mese,anno)
    for riga in righe[1:]:
        riga = riga.strip()
        if riga == "":
            continue  # Salta righe vuote

        # Separiamo i dati divisa da virgola
        parti = riga.split(",")
        codice = parti[0].strip()
        titolo = parti[1].strip()
        autore = parti[2].strip()
        mese = int(parti[3].strip())
        anno = int(parti[4].strip())

        # Creiamo il dizionario per la singola foto
        foto = {
            "codice": codice,
            "titolo": titolo,
            "autore": autore,
            "mese": mese,
            "anno": anno
        }

        # Cerchiamo se l'anno della foto esiste già nell'album
        anno_trovato = False
        for elemento in album:
            if elemento[0] == anno:
                elemento[1].append(foto)
                anno_trovato = True
                break

        # Se l'anno non esiste ancora, lo creiamo: [anno, [lista_foto]]
        if not anno_trovato:
            album.append([anno, [foto]])

    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """2. AGGIUNGI UNA NUOVA FOTO
    Controlla che il mese sia valido e che il codice non sia duplicato.
    Scrive la foto in coda al file CSV e aggiorna l'album in memoria.
    """
    # Controllo 1: il mese deve essere tra 1 e 12
    if mese < 1 or mese > 12:
        return None

    # Controllo 2: l'album deve esistere
    if album is None:
        return None

    # Controllo 3: il codice non deve essere già presente
    for elemento in album:
        for foto in elemento[1]:
            if foto["codice"] == codice:
                return None  # Codice duplicato!

    # Scrittura in coda al file CSV (modalità "a" = append)
    try:
        f = open(file_path, "a", encoding="utf-8")
        f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
        f.close()
    except FileNotFoundError:
        return None

    # Aggiornamento della struttura dati in memoria
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

    # Se l'anno non c'era, lo crea al volo
    if not anno_trovato:
        album.append([anno, [nuova_foto]])

    return nuova_foto


def cerca_foto(album, codice):
    """3. CERCA UNA FOTO PER CODICE
    Restituisce la stringa formattata con i dettagli della foto, oppure None.
    """
    if album is None:
        return None

    for elemento in album:
        for foto in elemento[1]:
            if foto["codice"] == codice:
                # Ritorna la stringa nel formato richiesto
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """4. ELENCO FOTO DI UN ANNO (ORDINATO PER TITOLO)
    Estrae i titoli delle foto di quell'anno e li ordina alfabeticamente.
    """
    if album is None:
        return None

    for elemento in album:
        if elemento[0] == anno:
            titoli = []
            for foto in elemento[1]:
                titoli.append(foto["titolo"])

            # Ordina i titoli in ordine alfabetico
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