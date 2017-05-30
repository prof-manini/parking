README
======

Questo progetto consiste principalmente in una simulazione di un
parcheggio, in particolare di una serie di luci che indicano il percorso
per arrivare dall'entrata al posteggio più vicino all'uscita e viceversa.

Simulazione
-----------

Il comando `make sim` esegue il programma `parking_simulation.py` che fa
partire la simulazione visuale del parcheggio. Il programma si controlla
con i seguenti tasti:

1.  `q` termina l'esecuzione del programma,
2.  `s` aggiunge un sensore (posto per parcheggiare),
3.  `c` aggiunge una macchina,
4.  `p` parcheggia una macchina in un posto a caso (libero) seguendo le indicazioni delle luci che si sono accese, una volta parcheggiata l'auto si crea un percorso per i pedoni che arriva all'uscita,
5.  `u` "sparcheggia" una macchina a caso (parcheggiata) seguendo le indicazioni delle luci che si sono accese,
6.  `x` fa partire o arresta la modalità "automatica",
7.  `b` salva lo stato del sistema (posizioni di sensori e macchine),
8.  `r` ripristina lo stato dal file di cui sopra (`parking.state`).
9.  `l` mostra delle informazioni sullo stato del sistema.

Durante il funzionamento, il programma (se eseguito con l'opzione `-v`
come da *makefile*) fa il *logging* di vari eventi. Si ottiene

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

2.  `socket_client_cli.py` è simile al precedente ma invece che andare
    in automatico, apre una CLI (*command line interface*) da cui si
    possono dare dei comandi, ossia inviare delle richieste. Al momento
    l'unica richiesta possibile è `state` che fornisce la stesso
    informazione di `socket_client`.

