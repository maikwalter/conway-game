#!/usr/bin/env python3
import sys
import random
import pygame

### hilfsfunktion für die spielmechanik
def nachbarn_zaehlen(spielfeld, xpos, ypos):
	anzahl = 0
	for x in range(xpos - 1, xpos + 2):
		for y in range(ypos - 1, ypos + 2):
			if x == xpos and y == ypos:
				continue
			if x >= 0 and x < len(spielfeld):
				if y >= 0 and y < len(spielfeld[0]):
					if spielfeld[x][y] == 1:
						anzahl += 1
	return anzahl

#spielmechanik

def spielfeld_erzeugen(zeilen, spalten):
	spielfeld = []
	for i in range(zeilen): 	# i von 1 bis zeilenzahl
		zeile = []				# leere zeilen schaffen
		for j in range(spalten):	# j von 1 bis spaltenzahl
			zeile.append(0)			# an zeile eine 0 anhängen
		spielfeld.append(zeile)		# jetzt an spielfeld die zeile anhängen
	return spielfeld

def spielfeld_definiertfuellen(spielfeld):
	spielfeld[1][1] = 1
	spielfeld[1][2] = 1
	spielfeld[2][1] = 1
	spielfeld[2][2] = 1
	return spielfeld


def spielfeld_löschen(spielfeld):
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	for i in range(zeilen):
		for j in range(spalten):
			spielfeld[i][j] = 0

def spielfeld_random(spielfeld, wieviele):
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	for i in range(wieviele):
		spielfeld[random.randint(0,zeilen-1)][random.randint(0,spalten-1)] = 1

def spielfeld_mechanik(spielfeld):
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	neues_spielfeld = spielfeld_erzeugen(zeilen, spalten)
	anzahl = 0
	for i in range(zeilen):
		for j in range(spalten):
			nachbarn = nachbarn_zaehlen(spielfeld, i, j)
			if spielfeld[i][j] == 1:
				if nachbarn < 2:
					neues_spielfeld[i][j] = 0
				elif nachbarn == 2:
					neues_spielfeld[i][j] = 1
					anzahl += 1
				elif nachbarn == 3:
					neues_spielfeld[i][j] = 1
					anzahl += 1
				else:
					neues_spielfeld[i][j] = 0
			if spielfeld[i][j] == 0:
				if nachbarn == 3:
					neues_spielfeld[i][j] = 1
					anzahl += 1
	return neues_spielfeld, anzahl


	
### von hier aus grafik
def fenster_erzeugen(spielfeld):
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	zellgroesse = 500 / zeilen
	breite = spalten * zellgroesse
	hoehe = zeilen * zellgroesse
	fenster = pygame.display.set_mode((breite, hoehe))
	pygame.display.set_caption("Game of Life")
	return fenster

def spielfeld_anzeigen(spielfeld, fenster):
	fenster.fill((255,255,255))
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	zellgroesse = 500 / zeilen
	for i in range(zeilen):
		for j in range(spalten):
			x = j * zellgroesse
			y = i * zellgroesse
			if spielfeld[i][j] == 1:
				pygame.draw.rect(fenster,(0, 0, 0),(x, y, zellgroesse, zellgroesse))
			pygame.draw.rect(fenster,(180, 180, 180),(x, y, zellgroesse, zellgroesse),1)
	pygame.display.flip()
    
#### und hier ist main

def main(args):
		startanzahl = 50
		myspielfeld = spielfeld_erzeugen(10,10)
		laeuft = True
		generationcount = 0
		pygame.init()
		spielfeld_random(myspielfeld, startanzahl)
		fenster = fenster_erzeugen(myspielfeld)
		while laeuft:
			for ereignis in pygame.event.get():
				if ereignis.type == pygame.QUIT:
					laeuft = False
			myspielfeld, zellenanzahl = spielfeld_mechanik(myspielfeld)
			spielfeld_anzeigen(myspielfeld,fenster)
			generationcount += 1
			print("Generationen: ", generationcount, "Zellen: ", zellenanzahl)
			pygame.time.wait(150)
		pygame.quit()
	
	
		return 0
		
if __name__ == '__main__':
	    sys.exit(main(sys.argv[1:]))
