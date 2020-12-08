<p align="center"><b>This Repo is still under heavy development!</b></p>      
      
# modelicaPost
modelicaPost ist eine Python-Bibliothek, um Resultate (.mat-Files) von Modelica-Simulationen weiterzuverarbeiten.
Innerhalb der Bibliothek befinden sich verschiedene Klassen, um verschiedene Funktionen abzudecken.
Folgende Klassen sind verfügbar:

- plotter     (Base-Klasse)
- linePlot  	(Klasse, um Modelica-Resultate als Linien-Plot auszugeben)
- piePlot		  (Klasse, um bestimmte Werte von Modelica-Resultaten als Kuchendiagramm auszugeben)
- stackPlot 	(Klasse, um Modelica-Resultate als gestapelte Linenplots auszugeben)

## Installation
Folgende Python-Bibliotheken müssen installiert sein, um modelicaPost verwenden zu können   
- numpy
- matplotlib
- scipy
- scimath
- modelicares

1. Öffne die Kommandozeile und wechsle das Arbeitsverzeichnis `/path/to/modelicaPost` 
2. Führe aus `python setup.py bdist_wheel`
3. Installiere mit dem Befahl `pip install /path/to/wheelfile.whl`

Nun ist die Bibliothek installiert und bereit zur Nutzung.
   
Um auf die Funktionalitäten von modelicaPost zugreifen zu können ist folgende Zeile notwendig:  
`from modelicaPost import modelicaPost`
   
## Verwendung
modelicaPost kann direkt in der Kommandozeile oder innerhalb eines Python-Scripts verwendet werden. Das Vorgehen ist immer das selbe:
1. Initialisieren einer neuen Instanz der gewünschten Klasse (Beispiel: `lp = modelicaPost.linePlot` )
2. Erfassen der auszuwertenden Variablen
3. Einstellungen für die Ausgaben tätigen
4. Ausgabe generieren lassen

### Erfassen der Variablen
Auszuwertende Variablen werden in einem Dictionary mit dem Namen `variables` gesammelt. Der Dictionary muss folgende Struktur aufweisen:  
`lp.variables = {'label_1': {'matFile': matfile-path, 'path': path_inside_matfile, 'origUnit': simulation_unit, 'displayUnit': unit_to_display}, 'label_2': {}, ...}`    
Für die Kommandozeile stehen die Methoden `add()`, `change()`, `remove()` und `showVars()` zur verfügung, mit welchen die Variablen direkt hinzugefügt, verändert, gelöscht oder eingesehen werden können.

### Einstellungen für die Ausgabe
Die aktuellen Einstellungen können über die Methode `settings()` eingesehen werden. Alle Einstellungen werden in Instanzvariablen gespeichert und können auch somit angepasst werden:
`lp.einstellung = neuer_Wert`

### Ausgabe generieren
Die Ausgabe wird mit der Methode `show()` oder `save()` generiert. Mit `show()` wird die Ausgabe in einem Fenster angezeigt wo sie noch weiter verändert und untersucht werden kann. Mit `save()` wird die Ausgabe direkt als SVG gespeichert. Als Argument kann noch ein Speicherpfad mitgegeben werden.

### Hilfe
Mit der Methode `help()` kann man sich jederzeit eine Übersicht über alle verfügbaren Methoden deraktuellen Kalsse anzeigen lassen.
