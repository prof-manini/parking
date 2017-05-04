PARKING-SIMULATION - PANNELLO ALL'INGRESSO POSTI LIBERI
=======================================================

Descrizione
===========

    L'obiettivo finale è realizzare un pannello (posto in una finestra pygame
    indipendente) visualizzante il numero di posti liberi per ogni zona del
    parcheggio, rispettivamente zona 1, 2 e 3.
    A lato di tale numero sarà presente un indicatore luminoso, di colore verde,
    giallo o rosso.
    l'indicatore risulterà di colore verde quando i posti liberi saranno
    superiori al 15% del totale, giallo se inferiore e rosso a 0.
    Nel lato inferiore del pannello sarà presente una sezione riservata alla
    comunicazione di messaggi speciali. Il messaggio di default sarà una stringa
    contenente la località e l'ora attuale, per esempio: "CAVALESE - 08:58".

Indicazioni per la realizzazione
================================

    Per raggiungere tale obiettivo verrà creato un file "panel.py" contenente la
    classe Panel, che gestisce il pannello. Verrà aggiunto un attributo alla
    classe Car-sensor per indicare la zona di appartenenza del parcheggio ed
    infine verrà predisposto un comando "i" per l'interazione con il pannello.
