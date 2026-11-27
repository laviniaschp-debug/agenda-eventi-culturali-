#!/usr/bin/env python3
"""Aggiornamento del 27/11/2026: nuovi eventi da biblioteche, circoli dei lettori,
librerie-bar e associazioni a Milano, Roma, Torino e Firenze."""
import json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "2026-11-27T09:00:00+01:00"


def E(date, time, title, venue, cat, desc, url, free=None, tags=None, why=None, geo=None, zona=None, verify=False, moods=None):
    e = {"date": date, "time": time, "title": title, "venue": venue, "cat": cat, "desc": desc,
         "url": url, "free": free, "tags": tags or [], "verify": verify}
    if why: e["why"] = why
    if geo: e["geo"], e["zona"] = geo, zona
    if moods: e["moods"] = moods
    return e


# ---------------- MILANO ----------------
VERSO = "Libreria Verso (corso di Porta Ticinese 40)"
VERSO_G = ([45.4565, 9.1815], "Navigli · Tortona · S. Ambrogio")
VERSO_U = "https://www.libreriaverso.com/appuntamenti/"
CDC = "Casa della Cultura (via Borgogna 3)"
CDC_U = "https://www.casadellacultura.it/"
FGF = "Fondazione Feltrinelli (viale Pasubio 5)"
MILANO = [
    E("2026-11-29", "10:15", "Filosofia sui Navigli: Vulnerabilità e guerra. Una lettura di Judith Butler",
      "Filosofia sui Navigli, viale Gorizia 12 (seminterrato)", "filosofia",
      "Conferenza della prof.ssa Valentina Surace (dottore di ricerca in Metodologie della Filosofia, Università di Messina), dalle 10:15 alle 12:30. La sala è nel seminterrato in fondo al cortile a destra: citofono sul cancello a nome Fumagalli.",
      "https://www.google.com/search?q=Filosofia+sui+Navigli+Milano", None, ["imperdibile"],
      "Una domenica mattina per chiedersi che cosa ci rende fragili, e perché questo potrebbe essere un punto di partenza invece che una debolezza.",
      [45.4545, 9.1738], "Navigli · Tortona · S. Ambrogio"),
    E("2026-12-01", "19:00", "Il giornalismo secondo García Márquez, con Mary Villalobos e Peter Gomez", VERSO, "talk",
      "Presentazione in libreria-bar, nel cuore del Ticinese.", VERSO_U, None, [], None, *VERSO_G),
    E("2026-12-01", "20:00", "Booknight: lo Spacciatore di Libri presenta Il capitalismo della sorveglianza",
      "Mare culturale urbano, Cascina Torrette (via Gabetti 15)", "tech",
      "Maurizio Afeltra racconta il saggio di Shoshana Zuboff: serata di libri in cascina.",
      "https://maremilano.org/", None, [], None, [45.4842, 9.1108], "Fuori centro", moods=["pensare", "gente"]),
    E("2026-12-01", "18:00", "La Chiesa e la sfida della pace. Da Leone XIII a Leone XIV", CDC, "geo",
      "Presentazione del volume a cura di Agostino Giovagnoli e Giorgio Del Zanna. Anche in streaming.", CDC_U, True),
    E("2026-12-02", "17:30", "Social Graces: etichetta e buone maniere britanniche", "Centro Culturale di Milano (largo Corsia dei Servi 4)", "storia",
      "Ciclo di quattro incontri a cura di Pietrangelo Falconi su una delle tradizioni più curiose del Regno Unito.",
      "https://www.centroculturaledimilano.it/"),
    E("2026-12-02", "18:00", "Festa 11: il compleanno di Verso", VERSO, "talk",
      "La libreria-bar del Ticinese compie 11 anni e festeggia con lettori e librai.", VERSO_U, None, [], None, *VERSO_G,
      moods=["gente"]),
    E("2026-12-03", "17:30", "Rossella Fabbrichesi: ermeneutica del soggetto atteggiato scientificamente",
      "Statale, Sala Martinetti (via Festa del Perdono 7)", "filosofia",
      "Seminario del Dipartimento di Filosofia Piero Martinetti, aperto al pubblico (anche su Teams).",
      "https://dipafilo.unimi.it/", True, [], None, [45.4600, 9.1940], "Centro"),
    E("2026-12-03", "19:00", "Le sussurratrici, con Giulia Paganelli e Carlotta Cossutta", VERSO, "talk",
      "Presentazione del libro (Edizioni E/O).", VERSO_U, None, [], None, *VERSO_G),
    E("2026-12-04", "18:00", "L'opera all'opera: l'Otello di Verdi raccontato da Enrico Reggiani", CDC, "classica",
      "Lezione sull'Otello del 1887 a pochi giorni dalla Prima della Scala. Anche in streaming.", CDC_U, True),
    E("2026-12-07", "17:00", "Prima Diffusa: Otello in diretta con la guida all'ascolto di Carlo Boccadoro", FGF, "classica",
      "Proiezione della Prima della Scala (regia di Damiano Michieletto) introdotta dal compositore Carlo Boccadoro. Ingresso libero, prenotazione consigliata.",
      "https://fondazionefeltrinelli.it/partecipa/prima-diffusa-2026-in-fondazione-feltrinelli/", True, ["imperdibile"],
      "La Prima della Scala senza smoking né biglietto: la si guarda insieme, con qualcuno che ti spiega cosa stai ascoltando."),
    E("2026-12-09", "19:00", "Il book club di Senza Rossetto: Pecorelle smarrite di Madeline Cash", VERSO, "talk",
      "Con Giulia Cuter, Giulia Perona e Ludovica Lugli: si discute del libro tutti insieme.", VERSO_U, None, [], None, *VERSO_G,
      moods=["gente", "pensare"]),
    E("2026-12-09", "21:00", "Emma Bonino: Europa è patria. Scegliamo: forti o sovranisti?", CDC, "geo",
      "Presentazione del libro con Emma Bonino. Anche in streaming.", CDC_U, True, ["imperdibile"]),
    E("2026-12-10", "", "Verso Cinema: Lynchiano, con John Higgs, Roberto Manassero e Alessandro Beretta", VERSO, "cinema",
      "Presentazione del libro su David Lynch (Nottetempo). Orario sul sito della libreria.", VERSO_U, None, [], None, *VERSO_G,
      verify=True),
    E("2026-12-11", "19:00", "Supernova book club: Il tempo e l'acqua di Andri Snær Magnason", VERSO, "scienza",
      "Gruppo di lettura sul clima con Gaia Tarini e Ferdinando Cotugno (Iperborea).", VERSO_U, None, [], None, *VERSO_G,
      moods=["gente", "pensare"]),
    E("2026-12-12", "18:30", "Spettrogramma book club: Retromania di Simon Reynolds", VERSO, "jazz",
      "Gruppo di lettura sulla musica pop e la nostalgia (minimum fax).", VERSO_U, None, [], None, *VERSO_G,
      moods=["gente"]),
    E("2026-12-13", "15:00", "La Traversata: la Fondazione Feltrinelli apre le porte alla città", FGF, "storia",
      "Dalle 15 alle 18 un pomeriggio aperto: spazi, archivi, pubblicazioni, parole, musica e immagini. Ingresso libero e gratuito.",
      "https://fondazionefeltrinelli.it/partecipa/la-traversata/", True),
    E("2026-12-15", "19:00", "Uno spritz con: Alfabeto milanese, con Alberto Saibene ed Emi Ligabue", VERSO, "storia",
      "Milano raccontata in ordine alfabetico, con firmacopie e uno spritz (Casagrande).", VERSO_U, None, [], None, *VERSO_G,
      moods=["gente"]),
]

# ---------------- ROMA ----------------
CDM = "Biblioteca Casa della Memoria e della Storia (via San Francesco di Sales 5)"
CDM_G = ([41.8935, 12.4662], "Trastevere · Testaccio · Ostiense")
ROMA = [
    E("2026-11-30", "17:30", "Vis à vis: Carlo Levi e Alberto Savinio, due pittori-scrittori del Novecento",
      "Biblioteca Casa delle Letterature (piazza dell'Orologio 3)", "storia",
      "Incontro a tema nella casa romana della letteratura contemporanea.",
      "https://www.bibliotechediroma.it/opac/library/biblioteca-casa-delle-letterature/RMBA7", True, [], None,
      [41.8990, 12.4703], "Centro storico"),
    E("2026-12-02", "17:00", "Odio. Un blues di Vittorio Pavoncello", CDM, "talk",
      "Presentazione del libro alla Casa della Memoria.", "https://www.bibliotechediroma.it/opac/.do", True, [], None, *CDM_G),
    E("2026-12-03", "18:00", "Gramsci, Togliatti, Longo, Berlinguer: Ai giovani", CDM, "storia",
      "Presentazione del libro: antifascismo, pace, democrazia, socialismo nelle parole rivolte ai giovani.",
      "https://www.bibliotechediroma.it/opac/.do", True, [], None, *CDM_G),
    E("2026-12-06", "17:30", "Geografie di lettura: Giancarlo De Cataldo con le letture di Massimo Popolizio",
      "La Nuvola (viale Asia 40), Più libri più liberi", "talk",
      "Ultimo incontro del ciclo per i 30 anni delle Biblioteche di Roma: lo scrittore apre la sua biblioteca personale. Gratuito, anche in streaming.",
      "https://www.informagiovaniroma.it/geografie-di-lettura-le-biblioteche-degli-autori/", True, ["imperdibile"],
      "Scoprire quali libri hanno formato uno scrittore è il modo più rapido per trovare il tuo prossimo libro."),
    E("2026-12-13", "11:00", "Lezioni di Storia · Maurizio Viroli: Il Principe di Machiavelli, il potere delle parole",
      "Auditorium Parco della Musica (viale Pietro de Coubertin 30)", "storia",
      "Ciclo Laterza Il potere dei classici: come un libro ha cambiato la storia della politica.",
      "https://www.auditorium.com/it/rassegne/lezioni-di-storia-2026-2027-il-potere-dei-classici/"),
    E("2026-12-17", "", "Spritzalibro: i giovedì della letteratura", "Teatro del Lido (via delle Sirene 22, Ostia)", "talk",
      "Letture di autori contemporanei, confronto aperto e spritz finale nel foyer, a cura di Cristina Cau e Lavinia Polzella.",
      "https://turismoroma.it/fr/node/179842", None, [], None, [41.7327, 12.2709], "EUR e sud", True, ["gente", "pensare"]),
    E("2026-12-18", "19:00", "Natale austriaco: Rafael Fingerlos, Sascha El Mouissi e Fabian Steindl",
      "Forum Austriaco di Cultura (viale Bruno Buozzi 113)", "classica",
      "Baritono, pianoforte e zither per un concerto di Natale. Ingresso gratuito su prenotazione: events.rom-kf@bmeia.gv.at",
      "https://www.austriacult.roma.it/", True, [], None, [41.9210, 12.4855], "Parioli · Villa Borghese · Nomentano"),
]

# ---------------- TORINO ----------------
CDL = "il Circolo dei lettori (via Bogino 9)"
FDC = "https://www.festivaldelclassico.it/"
ML = "https://www.mentelocale.it/torino/"


def fdc(date, time, title, cat, desc, url=FDC, tags=None, why=None):
    return E(date, time, "Festival del Classico: " + title, CDL, cat, desc, url, None, ["festivaldelclassico"] + (tags or []), why)


BCT = "https://bct.comune.torino.it/eventi-attivita/"
TORINO = [
    E("2026-12-02", "18:00", "MicroMega: presentazione del numero dedicato allo sport", CDL, "talk",
      "La rivista presenta il volume 6/2026.", "https://micromega.substack.com/p/prossimi-appuntamenti-firenze-e-torino"),
    fdc("2026-12-09", "17:00", "Luciano Canfora, Nel laboratorio di Aristotele", "filosofia",
        "Anteprima della nona edizione (Politeia/Convivenze) con Luciano Canfora e Ugo Cardinale: la raccolta delle Politeiai.",
        tags=["imperdibile"], why="Aristotele raccolse le costituzioni di 158 città per capire come si vive insieme: la stessa domanda che ci facciamo oggi."),
    fdc("2026-12-11", "16:00", "La convivenza difficile: barbari e no", "storia",
        "Con Mario Lentano (Università di Siena) e Raffaella Siracusa (Università di Torino): stranieri e barbari nel mondo antico.",
        ML + "148410-convivenza-difficile-barbari-no.htm"),
    fdc("2026-12-11", "16:30", "Aldo Schiavone, la res publica romana fra realtà e miti", "storia",
        "Lo storico racconta la repubblica romana tra quello che fu e quello che ne abbiamo immaginato.",
        ML + "148423-res-publica-romana-realta-miti-antichi-moderni.htm"),
    fdc("2026-12-11", "17:00", "Il teatro e la crisi di Atene", "storia",
        "Con Federico Condello (Università di Bologna) e Walter Lapini (Università di Genova).",
        ML + "148408-teatro-crisi-atene.htm"),
    fdc("2026-12-11", "17:30", "Memoria, oblio, comunità: una lezione ateniese", "filosofia",
        "Mauro Bonazzi (Università di Bologna) e lo scrittore Matteo Nucci.",
        ML + "148424-memoria-oblio-comunita-lezione-ateniese.htm"),
    fdc("2026-12-11", "18:00", "Agostino l'africano: uno sguardo decentrato sulla crisi dell'Impero", "storia",
        "Con Catherine Conybeare (Bryn Mawr College) e Giuseppe Pezzini (Oxford); modera Armando Buonaiuto.",
        ML + "148406-agostino-africano-sguardo-decentrato-crisi-impero-romano.htm"),
    fdc("2026-12-12", "10:30", "L'Iran poliedrico: convivenze di ieri e di oggi", "geo",
        "Con Chiara Barbati (Università di Pisa) e Farian Sabahi.", ML + "148409-iran-poliedrico-racconti-convivenze-ieri-oggi.htm"),
    fdc("2026-12-12", "11:00", "Abitare il conflitto, con Silvia Romani e Annalena Benini", "talk",
        "Furore, trasgressione e ordine della polis: la furia nel mito e nella storia.",
        ML + "148413-abitare-conflitto-furore-trasgressione-ordine-polis.htm"),
    fdc("2026-12-12", "11:30", "Seneca e il Tiranno", "storia",
        "Con Gianpiero Rosati (Scuola Normale) e Federica Bessone (Università di Torino).", ML + "148411-seneca-tiranno.htm"),
    fdc("2026-12-12", "15:00", "Gennaro Carillo, L'anima e le forme: nel laboratorio costituzionale di Platone", "filosofia",
        "Lezione su Platone e le forme della città.", ML + "148421-anima-forme-laboratorio-costituzionale-platone.htm"),
    fdc("2026-12-12", "15:30", "Come nasce una Repubblica", "storia",
        "Con Alfonso Celotto (Roma Tre) e Giulia Guerrini, a partire dal libro Viva il Re! Viva la Repubblica!",
        ML + "148407-come-nasce-repubblica.htm"),
    fdc("2026-12-12", "16:00", "Luciano Bossina, Come in cielo così in terra", "storia",
        "L'uomo antico tra due cittadinanze.", ML + "148416-come-cielo-cosi-terra-uomo-antico-due-cittadinanze.htm"),
    fdc("2026-12-12", "17:00", "Cittadini del mondo, con Mauro Bonazzi e Massimo Mori", "filosofia",
        "Il cosmopolitismo antico e le sue eredità.", ML + "148415-cittadini-mondo.htm"),
    fdc("2026-12-12", "18:00", "Ivano Dionigi e Luca Mercalli, Il nostro posto nel mondo", "scienza",
        "Il latinista e il climatologo sulla comunità dei viventi.", ML + "148420-nostro-posto-mondo-comunita-viventi.htm",
        tags=["imperdibile"], why="Un latinista e un climatologo sulla stessa domanda: siamo la misura del mondo o soltanto ospiti?"),
    E("2026-12-12", "21:00", "Festival del Classico: Telmo Pievani, tra cooperazione e conflitto", "Torino (sede sul sito del festival)", "scienza",
      "L'evoluzione della convivenza raccontata dal filosofo della biologia.", FDC, None, ["festivaldelclassico", "imperdibile"],
      None, [45.0703, 7.6869], "Centro", True),
    fdc("2026-12-13", "15:00", "Ciò che ci tiene insieme, con Giovanna Botteri e Michela Marzano", "talk",
        "Voci, legami e possibilità di convivenza, a partire da Soffiando nel vento e Qualcosa che brilla.",
        ML + "148414-cio-ci-tiene-insieme-voci-legami-possibilita-convivenza.htm", tags=["imperdibile"],
        why="Che cosa tiene insieme una comunità quando tutto spinge a dividerla: una giornalista e una filosofa provano a rispondere."),
    fdc("2026-12-13", "16:30", "Abitare il mondo, abitare l'umano: convivenze nell'era dell'IA", "tech",
        "Con Alessio Carciofi e Francesco Brucoli.", ML + "148405-abitare-mondo-abitare-umano-convivenze-era-tecnica-intelligenza-artificiale.htm"),
    fdc("2026-12-13", "17:00", "Politeia e convivenze: il maschile e il femminile nel mondo antico", "storia",
        "Con Laura Pepe (autrice di Storia non convenzionale delle donne di Grecia) e Marco Bonini.",
        ML + "148425-politeia-convivenze-ripensare-maschile-femminile-mondo-antico.htm"),
    # Biblioteche civiche torinesi (gratuite; orari sul sito BCT)
    E("2026-11-30", "", "Stefano Belingardi: Storie di Beaulard. L'attesa del Natale", "Biblioteca civica Passerin d'Entrèves (via Guido Reni 102)", "talk",
      "Incontro con l'autore in biblioteca.", BCT + "storie-di-beaulard-lattesa-del-natale", True, [], None, [45.0335, 7.6180], "Fuori centro", True),
    E("2026-12-02", "", "Il linguaggio sonoro delle cellule: Domenico Sciajno con Rossana Becarelli", "Biblioteca civica Villa Amoretti (corso Orbassano 200)", "scienza",
      "Suono e biologia in dialogo, in biblioteca.", BCT + "il-linguaggio-sonoro-delle-cellule", True, [], None, [45.0440, 7.6420], "Fuori centro", True),
    E("2026-12-03", "", "Leggermente incontra Anna Pavignano: La ragazza soldato", "Biblioteca civica Cesare Pavese (via Candiolo 79)", "talk",
      "La sceneggiatrice e scrittrice presenta il romanzo (Piemme, 2026).", BCT + "leggermente-incontra-anna-pavignano", True, [], None,
      [45.0245, 7.6265], "Fuori centro", True),
    E("2026-12-05", "", "Poesia in biblioteca: Angela Donna, Clochard. Poesie senza dimora", "Sala Molinari, Biblioteca Natalia Ginzburg (via Lombroso 16)", "talk",
      "Reading e incontro con l'autrice.", BCT + "poesia-in-biblioteca-1", True, [], None, [45.0560, 7.6830], "San Salvario", True),
    E("2026-12-09", "", "Anna Mastromarino: La Costituzione a pezzi", "Sala Molinari, Biblioteca Natalia Ginzburg (via Lombroso 16)", "geo",
      "Come cambiare la nostra Carta restando antifascisti (Bollati Boringhieri).",
      BCT + "la-costituzione-a-pezzi-come-cambiare-la-nostra-carta-restando-antifascisti", True, [], None, [45.0560, 7.6830], "San Salvario", True),
    E("2026-12-10", "", "Voci d'autore: incontro con Fabio Geda", "Biblioteca civica Passerin d'Entrèves (via Guido Reni 102)", "talk",
      "Letture teatrali di attori professionisti con l'autore presente, a cura di Assemblea Teatro.",
      BCT + "voci-dautore-incontro-con-fabio-geda", True, [], None, [45.0335, 7.6180], "Fuori centro", True),
]
TORINO_FIX = {  # completa due eventi del festival già presenti
    "Festival del Classico: Alberto Angela apre": {"time": "21:00"},
    "Festival del Classico: dialogo sulla pace": {"time": "18:00", "venue": "Teatro San Giuseppe (via Andrea Doria 18)",
                                                 "geo": [45.0641, 7.6829], "zona": "Centro"},
}

# ---------------- FIRENZE ----------------
VIE = "Gabinetto Vieusseux, Palazzo Strozzi, Sala Ferri"
VIE_U = "https://www.vieusseux.it/luogo/giardino-delle-rose/"
LUZI = "Biblioteca Mario Luzi (via Ugo Schiff 8)"
LUZI_G = ([43.7862, 11.2893], "Campo di Marte · Coverciano")
LUZI_U = "https://quartieri.comune.fi.it/dalle-redazioni/dicembre-2026-alle-biblioteche-del-quartiere-2"
FIRENZE = [
    E("2026-11-27", "17:30", "MicroMega: I nuovi padroni del mondo. Oligarchie digitali e democrazie sotto scacco",
      "Biblioteca delle Oblate, Sala Sibilla Aleramo (via dell'Oriuolo 24)", "geo",
      "Leggere per non dimenticare: con Cinzia Sciuto, Luca De Biase e Roberto Seghetti; letture di Massimo Tarducci.",
      "https://www.leggerepernondimenticare.com/", True),
    E("2026-12-01", "17:00", "Premio Carlo Betocchi – Città di Firenze: la cerimonia", "Palazzo Bastogi, Sala delle Feste (via Cavour 18)", "talk",
      "XXV edizione del premio di poesia del Gabinetto Vieusseux.", VIE_U, None, [], None, [43.7768, 11.2563], "Centro storico"),
    E("2026-12-02", "17:30", "ContempoartEnsemble: Okawango, conversazione e concerto", VIE, "classica",
      "XXIII Festival del ContempoartEnsemble: gli artisti raccontano e suonano.", VIE_U),
    E("2026-12-03", "17:00", "Oltre il manicomio, dentro la persona: dialogo su San Salvi", LUZI, "salute",
      "Rosaria Magni presenta San Salvi. Una nuova esperienza, con Veronica Boldi. Ingresso libero.", LUZI_U, True, [], None, *LUZI_G),
    E("2026-12-03", "17:30", "Raccontare il racconto: Francesco Colella legge Tomasi di Lampedusa", VIE, "talk",
      "Voci del Novecento italiano, ciclo a cura di Federico Tiezzi e Sandro Lombardi.", VIE_U),
    E("2026-12-03", "19:00", "Giochi e legami sociali: serata di giochi da tavolo", "Spazio Co-Stanza (via Ponte alle Mosse 32/38r)", "talk",
      "Dialoghi urbani: si gioca insieme con duepunti APS. Prenotazione: duepuntiassociazione@gmail.com",
      "https://cultura.comune.fi.it/system/files/2026-09/web-a5-programma_Dialoghi-urbani_2026_programma.pdf", True, [], None,
      [43.7818, 11.2402], "Cascine · Rifredi · Novoli", moods=["gente"]),
    E("2026-12-10", "17:30", "Raccontare il racconto: Federico Tiezzi legge Silvio D'Arzo", VIE, "talk",
      "Voci del Novecento italiano al Gabinetto Vieusseux.", VIE_U),
    E("2026-12-10", "17:30", "L'amore e le sue forme: racconti letti ad alta voce", LUZI, "talk",
      "Un anno di racconti, con il Collettivo Darsi Voce. Ingresso libero.", LUZI_U, True, [], None, *LUZI_G),
    E("2026-12-11", "17:30", "Letture migranti: Jallow's story", LUZI, "talk",
      "Ludovico Fededegni legge una storia dai diari migranti DiMMi, con Riccardo Massai. Ingresso libero.", LUZI_U, True, [], None, *LUZI_G),
    E("2026-12-16", "16:30", "Conversazioni musicali: I racconti di Hoffmann di Offenbach", LUZI, "classica",
      "Guida all'opera in scena al Maggio dal 20 dicembre, con gli Amici del Teatro del Maggio. Gratuito, prenotazione consigliata.",
      LUZI_U, True, [], None, *LUZI_G),
    E("2026-12-17", "17:00", "I Tempieri di Firenze: i Templari in città", LUZI, "storia",
      "Mario Pagni e Chiara Sacchetti presentano il libro. Ingresso libero.", LUZI_U, True, [], None, *LUZI_G),
    E("2026-12-17", "17:30", "Raccontare il racconto: Sandro Lombardi legge Dario Fo", VIE, "talk",
      "Ultimo appuntamento di dicembre con le Voci del Novecento italiano.", VIE_U),
]

NEW_VENUES = {
    "venues.json": [
        {"match": "Libreria Verso", "lat": 45.4565, "lng": 9.1815, "zona": "Navigli · Tortona · S. Ambrogio"},
        {"match": "viale Gorizia 12", "lat": 45.4545, "lng": 9.1738, "zona": "Navigli · Tortona · S. Ambrogio"},
        {"match": "Cascina Torrette", "lat": 45.4842, "lng": 9.1108, "zona": "Fuori centro"},
        {"match": "Festa del Perdono", "lat": 45.4600, "lng": 9.1940, "zona": "Centro"},
    ],
    "venues-roma.json": [
        {"match": "Casa delle Letterature", "lat": 41.8990, "lng": 12.4703, "zona": "Centro storico"},
        {"match": "Casa della Memoria e della Storia", "lat": 41.8935, "lng": 12.4662, "zona": "Trastevere · Testaccio · Ostiense"},
        {"match": "Teatro del Lido", "lat": 41.7327, "lng": 12.2709, "zona": "EUR e sud"},
        {"match": "Forum Austriaco", "lat": 41.9210, "lng": 12.4855, "zona": "Parioli · Villa Borghese · Nomentano"},
    ],
    "venues-torino.json": [
        {"match": "Teatro San Giuseppe", "lat": 45.0641, "lng": 7.6829, "zona": "Centro"},
        {"match": "Passerin d'Entrèves", "lat": 45.0335, "lng": 7.6180, "zona": "Fuori centro"},
        {"match": "Villa Amoretti", "lat": 45.0440, "lng": 7.6420, "zona": "Fuori centro"},
        {"match": "Cesare Pavese", "lat": 45.0245, "lng": 7.6265, "zona": "Fuori centro"},
        {"match": "Natalia Ginzburg", "lat": 45.0560, "lng": 7.6830, "zona": "San Salvario"},
    ],
    "venues-firenze.json": [
        {"match": "Biblioteca Mario Luzi", "lat": 43.7862, "lng": 11.2893, "zona": "Campo di Marte · Coverciano"},
        {"match": "Palazzo Bastogi", "lat": 43.7768, "lng": 11.2563, "zona": "Centro storico"},
        {"match": "Co-Stanza", "lat": 43.7818, "lng": 11.2402, "zona": "Cascine · Rifredi · Novoli"},
    ],
}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return set(w for w in re.findall(r"[a-z]{4,}", s))


def dup(e, events):
    a = norm(e["title"])
    for o in events:
        if o["date"] != e["date"]:
            continue
        b = norm(o["title"])
        a, b = a - {"festival", "classico"}, b - {"festival", "classico"}
        if a and b and len(a & b) / min(len(a), len(b)) >= 0.6:
            return o
    return None


def merge(fname, prefix, new, fixes=None):
    path = os.path.join(ROOT, fname)
    d = json.load(open(path, encoding="utf-8"))
    ev = d["events"]
    added, skipped = 0, []
    if fixes:
        for frag, patch in fixes.items():
            for o in ev:
                if o["title"].startswith(frag):
                    o.update(patch)
    n = max(int(o["id"][1:]) for o in ev) + 1
    for e in new:
        o = dup(e, ev)
        if o:
            skipped.append(f'{e["date"]} {e["title"]}  ~  {o["title"]}')
            continue
        e["id"] = f"{prefix}{n:03d}"
        n += 1
        ev.append(e)
        added += 1
    ev.sort(key=lambda x: (x["date"], x.get("time") or "99", x["title"]))
    d["updated"] = UPDATED
    last = max(x["date"] for x in ev)
    if "range" in d:
        d["range"] = [d["range"][0], max(d["range"][1], last)]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(fname, "aggiunti", added, "| saltati come doppioni:", len(skipped))
    for s in skipped:
        print("   -", s)


def venues():
    for fname, rows in NEW_VENUES.items():
        path = os.path.join(ROOT, "tools", fname)
        v = json.load(open(path, encoding="utf-8"))
        have = {r["match"].lower() for r in v}
        for r in rows:
            if r["match"].lower() not in have:
                v.insert(0, r)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    venues()
    merge("events.json", "e", MILANO)
    merge("roma.json", "r", ROMA)
    merge("torino.json", "t", TORINO, TORINO_FIX)
    merge("firenze.json", "f", FIRENZE)
