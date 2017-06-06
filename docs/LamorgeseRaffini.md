https://github.com/Lamorgese-Raffini/parking

PARKING-SIMULATION - PANNELLO ALL'INGRESSO POSTI LIBERI
=======================================================

Files
=====
    - creato il file panel.py, contenente la classe Panel per la gestione del
      pannello, la classe PanelSocketServer e la classe PanelSocketClient per la
      gestione della comunicazione via socket.
    - modificato il file car_sensor.py, è stato aggiunto l'attributo zone (un
      numero compreso tra 0 e 2) per differenziare le aree del parhceggio

Descrizione
===========

    Il pannello è suddiviso in tre sezioni, la prima (header) contiene il nome
    dell'istituto "La Rosa Bianca" di Cavalese; la seconda contiene tutte le
    informazioni per ogni zona: numero di posti liberi ed indicatore luminoso,
    rosso o verde; la terza ed ultima sezione (footer) contiene il luogo e l'ora
    corrente presa dal'ora di sistema.
    L'indicatore luminoso risulta verde se il numero di posti liberi è maggiore
    di zero, risulta invece rosso in caso contrario.
    Il pannello funziona tramite apposito processo, il quale comunica con il
    processo della simulazione del parcheggio ottenendo da questo una stringa
    contenete per ogni sensore la zona di appartenenza e "x" se il sensore è
    occupato.
    L'unica interazione con l'utente è tramite il pulsante "Q" che chiude la
    finestra pygame.
