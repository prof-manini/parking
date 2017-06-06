CODE :=  car.py car_sensor.py game.py parking_simulation.py \
	settings.py socket_client.py socket_client_cli.py

all: sim

README.pdf: README.md
	pandoc $< -o $@

sim:  parking_simulation.py
	python $< -v

socket_client: socket_client.py
	python $<

repl_client: socket_client_cli.py
	python $<

clean:
	rm -f *~ *.pyc
	rm -f port.txt parking.log

cleaner: clean
	rm -f *.pdf *.state
	rm -rf _minted*
	rm -f
	rm -f TAGS
	rm -f *.txt

TAGS: $(CODE)
	etags --regex=/[A-Z_]+/ $(CODE)

.PHONY: all sim socket_client repl_client clean cleaner
