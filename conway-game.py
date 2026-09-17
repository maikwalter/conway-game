#!/usr/bin/env python3
import sys
import random
import pygame

### -----------------------------------------------
### --- Funktionen für die Spielmechanik
### -----------------------------------------------

def nachbarn_zaehlen(spielfeld, xpos, ypos):
	"""Zählt die lebenden Nachbarn einer Zelle.
	Es wird die spielfeld-matrix übergeben und die x- und y-position eines Feldes.
	Die Funktion übergibt die Anzahl der Nachbarn"""
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

def spielfeld_erzeugen(zeilen, spalten):
	""" es wird eine leere Spielfeld-Matrix erzeugt. 
	Die Funktion erwartet die Größe der Matrix und gibt das Spielfeld zurück
	"""
	spielfeld = []
	for i in range(zeilen): 	
		zeile = []					
		for j in range(spalten):
			zeile.append(0)		
		spielfeld.append(zeile)
	return spielfeld

def spielfeld_definiertfuellen(spielfeld, muster, location_x,location_y):
	""" füllt das Spielfeld mit bestimmten Figuren an bestimmten Positionen
	erwartet das Spielfeld, das Muster als String und die Position,
	Gibt das Spielfeld zurück
	"""
	### erster Job: Spielfeld leeren, d.h. mit 0 überschreiben
	spielfeld = spielfeld_löschen(spielfeld)
	### danach gemäß Parameter wieder füllen
	if muster == "blinker":
		spielfeld[location_x][location_y] = 1
		spielfeld[location_x+1][location_y] = 1
		spielfeld[location_x+2][location_y] = 1
	elif muster == "glider":
		spielfeld[location_x][location_y + 1] = 1
		spielfeld[location_x + 1][location_y + 2] = 1
		spielfeld[location_x + 2][location_y] = 1
		spielfeld[location_x + 2][location_y + 1] = 1
		spielfeld[location_x + 2][location_y + 2] = 1
	elif muster == "block":
		spielfeld[location_x][location_y] = 1
		spielfeld[location_x+1][location_y] = 1
		spielfeld[location_x][location_y+1] = 1
		spielfeld[location_x+1][location_y+1] = 1
	### fertig, Rückgabewert
	return spielfeld

def spielfeld_löschen(spielfeld):
	""" löscht das Spielfeld, d.h. überschreibt mit Nullen"""
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	for i in range(zeilen):
		for j in range(spalten):
			spielfeld[i][j] = 0
	return spielfeld

def spielfeld_random(spielfeld, wieviele):
	""" füllt das Spielfeld zufällig mit lebenden Zellen. 
	Die Anzahl der lebenden Zellen muss übergeben werden."""
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	for i in range(wieviele):
		spielfeld[random.randint(0,zeilen-1)][random.randint(0,spalten-1)] = 1
	return spielfeld

def spielfeld_mechanik(spielfeld):
	""" Diese Funktion ist die tatsächliche Conway Spielmechanik.
	Die Funktion erwartet die Spielfeld-Matrix und gibt die Spielfeld-Matrix
	der nächsten Generation zurück und die Anzahl der Zellen darin
	"""
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

### -----------------------------------------------
### --- Funktionen für die Darstellung
### -----------------------------------------------

def fenster_erzeugen(spielfeld, infohoehe):
	""" erzeugt das Darstellungsfenster. Die Funktion erwartet die 
	Spielfeld-Matrix und die Höhe des Info-Feldes als Parameter und 
	gibt das Fenster-Objekt zurück"""
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	zellgroesse = 500 / zeilen
	breite = spalten * zellgroesse
	hoehe = zeilen * zellgroesse
	fenster = pygame.display.set_mode((breite, hoehe+infohoehe))
	pygame.display.set_caption("Game of Life")
	return fenster

def spielfeld_anzeigen(spielfeld, fenster, infohoehe, gen, zell):
	""" Diese Funktion malt in das Fenster-Objekt die Zellen.
	Sie erwartet die folgenden Parameter:
	- Spielfeld-Matrix
	- Fenster-Objekt
	- Höhe des Info-Feldes
	- Generationenanzahl und Zellanzahl für die Darstellung
	"""
	fenster.fill((255,255,255))
	zeilen = len(spielfeld)
	spalten = len(spielfeld[0])
	zellgroesse = 500 / zeilen
	for i in range(zeilen):
		for j in range(spalten):
			x = j * zellgroesse
			y = i * zellgroesse + infohoehe
			### hier werden die lebenden Zellen gezeichnet
			if spielfeld[i][j] == 1:
				pygame.draw.rect(fenster,(0, 0, 0),(x, y, zellgroesse, zellgroesse))
			### und hier die grauen Rahmen
			pygame.draw.rect(fenster,(180, 180, 180),(x, y, zellgroesse, zellgroesse),1)
	schrift = pygame.font.Font(None, 28)
	text = f"Generation: {gen}   Zellen: {zell}"
	anzeige = schrift.render(text, True, (0, 0, 0))
	fenster.blit(anzeige, (10, 10))
	pygame.display.flip()
	
### -----------------------------------------------
### --- Main-Funktionen
### -----------------------------------------------

def main(args):
		startanzahl = 140
		myspielfeld = spielfeld_erzeugen(20,20)
		laeuft = True
		pause = False
		generationcount = 0
		pygame.init()
		myspielfeld = spielfeld_random(myspielfeld, startanzahl)
		#myspielfeld = spielfeld_definiertfuellen(myspielfeld,"glider")
		hoehe_infofeld = 40
		fenster = fenster_erzeugen(myspielfeld, hoehe_infofeld)
		while laeuft:
			# abfrage nach Ereignissen
			for ereignis in pygame.event.get():
				if ereignis.type == pygame.QUIT:
					laeuft = False
				elif ereignis.type == pygame.KEYDOWN:
					# wenn Tasten gedrückt werden:
					# SPACE - Pause / keine Pause
					# ESC - Ende
					if ereignis.key == pygame.K_SPACE:
						pause = not pause
					elif ereignis.key == pygame.K_ESCAPE:
						laeuft = False
			# spielen
			if not pause:
				myspielfeld, zellenanzahl = spielfeld_mechanik(myspielfeld)
				generationcount += 1
			spielfeld_anzeigen(myspielfeld,fenster,hoehe_infofeld,generationcount,zellenanzahl)
			pygame.time.wait(150)
		### Spiel beenden
		pygame.quit()	
		return 0
		
if __name__ == '__main__':
	    sys.exit(main(sys.argv[1:]))
