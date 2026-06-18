import os

# Het pad naar het CSV-bestand met serverdata, in dezelfde map als dit script.
BESTAND = os.path.join(os.path.dirname(__file__), "serverdata.csv")


def lees_regels():
    # Opent het CSV-bestand, leest de headerregel en zet elke volgende regel
    # om naar een dictionary {kolomnaam: waarde}. Geeft een lijst van die
    # dictionaries terug — één per rij in het bestand.
    with open(BESTAND, "r") as f:
        headers = f.readline().strip().split(";")
        return [dict(zip(headers, r.strip().split(";"))) for r in f if r.strip()]


def servertype(server):
    # Haalt alleen de letters uit een servernaam (bijv. "web01" → "web").
    # Wordt gebruikt om servers te groeperen op type.
    return ''.join(filter(str.isalpha, server))


def aantallen_per_server(regels):
    # Telt hoeveel rijen er per unieke servernaam in de data staan
    # en print het resultaat gesorteerd op servernaam.
    telling = {}
    for r in regels:
        telling[r["server"]] = telling.get(r["server"], 0) + 1
    print("\nAantallen per server:")
    for s in sorted(telling):
        print(f"  {s}: {telling[s]}")


def fouten_per_servertype(regels):
    # Telt het totale aantal fouten (kolom "errors") per servertype
    # en print het als een opgemaakte tabel.
    fouten = {}
    for r in regels:
        t = servertype(r["server"])
        fouten[t] = fouten.get(t, 0) + int(r["errors"])
    print(f"\n{'servertype':<12}| fouten\n{'-'*11}-|-------")
    for t in sorted(fouten):
        print(f"  {t:<10}| {fouten[t]}")


def bestand_per_servertype(regels):
    # Maakt voor elk servertype een apart CSV-bestand aan (bijv. "web.csv")
    # en schrijft de bijbehorende rijen daarin. Sluit alle bestanden netjes
    # af via een finally-blok, ook als er een fout optreedt.
    bestanden = {}
    try:
        for r in regels:
            t = servertype(r["server"])
            if t not in bestanden:
                pad = os.path.join(os.path.dirname(__file__), f"{t}.csv")
                bestanden[t] = open(pad, "w")
                bestanden[t].write("date;server;minload;maxload;errors\n")
            bestanden[t].write(f"{r['date']};{r['server']};{r['minload']};{r['maxload']};{r['errors']}\n")
        print(f"\n  Bestanden aangemaakt: {', '.join(sorted(bestanden))}")
    finally:
        for f in bestanden.values():
            f.close()


def menu():
    # Laadt de data eenmalig in en toont daarna een herhalend menu totdat
    # de gebruiker kiest voor optie 4 (Quit). Bij een ongeldige invoer
    # wordt een foutmelding getoond en het menu opnieuw weergegeven.
    regels = lees_regels()
    opties = {"1": aantallen_per_server, "2": fouten_per_servertype, "3": bestand_per_servertype}
    while True:
        print("\n--- Serverdata menu ---\n  1 - Aantallen per server\n  2 - Fouten per server\n  3 - Bestand per server\n  4 - Quit")
        keuze = input("Keuze: ").strip()
        if keuze == "4":
            print("Tot ziens!")
            break
        elif keuze in opties:
            opties[keuze](regels)
        else:
            print("  Ongeldige keuze, probeer opnieuw.")


if __name__ == "__main__":
    # Startpunt van het script. Roept het menu aan en wacht daarna op een
    # Enter-druk zodat het venster niet meteen sluit (bijv. bij dubbelklikken).
    menu()
    input("\nDruk op Enter om af te sluiten...")
