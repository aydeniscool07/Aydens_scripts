import os


BESTAND = os.path.join(os.path.dirname(__file__), "serverdata.csv")


def lees_regels():
   
    with open(BESTAND, "r") as f:
        headers = f.readline().strip().split(";")
        return [dict(zip(headers, r.strip().split(";"))) for r in f if r.strip()]


def servertype(server):
    
    return ''.join(filter(str.isalpha, server))


def aantallen_per_server(regels):
    
    telling = {}
    for r in regels:
        telling[r["server"]] = telling.get(r["server"], 0) + 1
    print("\nAantallen per server:")
    for s in sorted(telling):
        print(f"  {s}: {telling[s]}")


def fouten_per_servertype(regels):
   
    fouten = {}
    for r in regels:
        t = servertype(r["server"])
        fouten[t] = fouten.get(t, 0) + int(r["errors"])
    print(f"\n{'servertype':<12}| fouten\n{'-'*11}-|-------")
    for t in sorted(fouten):
        print(f"  {t:<10}| {fouten[t]}")


def bestand_per_servertype(regels):
    
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
   
    menu()
    input("\nDruk op Enter om af te sluiten...")
