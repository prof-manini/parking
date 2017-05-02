README
======

Questo progetto consiste principalmente in una simulazione di un
parcheggio, in particolare di una serie di sensori di presenza delle
macchine, del sistema di controllo dell'ingresso e forse della gestione
dell'illuminazione.

In una eventuale implementazione vera del sistema, sensori e attuatori
saranno dei dispositivi elettronici reali, magari con un loro
funzionamento indipendente ed una propria logica, che saranno però
interrogabili e controllabili anche da un sistema remoto.

Il software di simulazione, e quindi anche di eventuale futuro controllo
e gestione, è scritto in Python e c'è quindi il problema
dell'interfacciamento con l'hardware che si può risolvere in vari modi:

1.  l'hardware è di per sé in grado di comunicare in qualche modo
    (seriale, wi-fi, etc.) con un "sistema Python" (es: beagle bone,
    macchina Linux, etc.);
2.  l'hardware è connesso ad un Arduino (o simile) che poi comunica con
    il sistema Python;
3.  il programma Pyton gira nativamente su un sistema in grado di
    controllare l'hardware, ad esempio un ESP8266 Huzzah.

Prerequisiti
============

Installazione di `Python` e della libreria `pygame`. Con `Debian` e
simili `sudo apt-get install python-pygame`, con altri sistemi buon
divertimento.

Estrazione del codice
=====================

Il originale codice del progetto era contenuto tutto in un file
`parking-simulation.org` da venivano vengono generati, via *tangling*
molti altri file, tra cui i sorgenti Python. Per fare questa
estrazione serve `Emacs` e la relativa libreria `org-mode` (che adesso
fa comunque parte di una installazione standard di `Emacs`). Questa è
ovviamente una dipendenza un po' forte ed avere un unico file
"sorgente" non facilita la condivisione.  Per questo il progetto in
questa versione "condivisa con gli studenti" è stato modificato nel
senso che adesso il file org non è più utilizzato (almeno non per il
*tangling*) e i file sorgente *Python* sono separati.

Stato del codice
================

Questo progetto è evidentemente un *work in progress*.  Questa
sezione, che dovrà essere aggiornata frequentemente, serve quindi per
documentare quali parti sono funzionanti, cosa si può fare e
come. Notare che il progetto include un *makefile* con alcuni *target*
che servono proprio a lanciare i programmi principali.

Simulazione
-----------

Il comando `make sim` esegue il programma `parking_simulation.py` che fa
partire la simulazione visuale del parcheggio. Il programma si controlla
con i seguenti tasti:

1.  `q` termina l'esecuzione del programma,
2.  `s` aggiunge un sensore (posto per parcheggiare),
3.  `c` aggiunge una macchina,
4.  `p` parcheggia una macchina in un posto a caso (libero),
5.  `u` "sparcheggia" una macchina a caso (parcheggiata),
6.  `x` fa partire o arresta la modalità "automatica",
7.  `b` salva lo stato del sistema (posizioni di sensori e macchine),
8.  `r` ripristina lo stato dal file di cui sopra (`parking.state`).
9.  `l` mostra delle informazioni sullo stato del sistema.

Durante il funzionamento, il programma (se eseguito con l'opzione `-v`
come da *makefile*) fa il *logging* di vari eventi. Si ottie

``` {.example}
$ python parking_simulation.py -v
SocketServer running on port 6520
root : DEBUG Adding sensor n. 0 at (100, 100)
root : DEBUG Adding sensor n. 1 at (100, 150)
root : DEBUG Adding sensor n. 2 at (100, 200)
root : DEBUG Adding sensor n. 3 at (100, 250)
root : DEBUG Adding sensor n. 4 at (100, 300)
root : DEBUG Adding car n. 0 at (500, 100)
root : DEBUG Adding car n. 1 at (500, 150)
root : DEBUG Adding car n. 2 at (500, 200)
root : DEBUG Adding car n. 3 at (500, 250)
root : DEBUG Car 0 arrived at sensor 2
root : DEBUG Car 1 arrived at sensor 3
root : DEBUG Car 2 arrived at sensor 1
root : DEBUG Car 3 arrived at sensor 0
root : DEBUG Car 2 left sensor 1
root : DEBUG Car 2 arrived at sensor 4
root : DEBUG Car 1 left sensor 3
root : DEBUG Car 0 left sensor 2
root : DEBUG Car 2 left sensor 4
```

Controllo dall'esterno
----------------------

Il programma di simulazione include un semplice *server* `TCP` che apre
una *socket* su *localhost* e su una porta *random* (il *port number*
viene scritto ogni volta nel file `port.txt` così i *client* lo possono
leggere).

Al momento ci sono due semplicissimi *client*:

1.  `socket_client.py` si connette alla simulazione e ad intervalli di
    un secondo (di solito) apre una connessione, "legge" lo stato dei
    sensori e stampa una riga con delle `X` per i sensori occupati degli
    *underscore* per quelli liberi. Si ottiene quindi un *log* del tipo:

``` {.example}
$ python socket_client.py
X X _ X _
X X _ X X
X X X _ X
_ X _ _ X
_ _ _ _ X
X _ _ _ _
```

1.  `socket_client_cli.py` è simile al precedente ma invece che andare
    in automatico, apre una CLI (*command line interface*) da cui si
    possono dare dei comandi, ossia inviare delle richieste. Al momento
    l'unica richiesta possibile è `state` che fornisce la stesso
    informazione di `socket_client`.
