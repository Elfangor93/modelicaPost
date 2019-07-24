###################################
##    Readme von modelicaPost    ##
###################################

modelicaPost ist eine Python-Bibliothek, um Resultate (.mat-Files) von Modelica-Simulationen weiterzuverarbeiten.
Innerhalb der Bibliothek befinden sich verschiedene Klassen, um verschiedene Funktionen abzudecken.
Folgende Klassen sind verfügbar:

- plotter		(Base-Klasse)
- linePlot  	(Klasse, um Modelica-Resultate als Linien-Plot auszugeben)
- piePlot		(Klasse, um bestimmte Werte von Modelica-Resultaten als Kuchendiagramm auszugeben)
- stackPlot 	(Klasse, um Modelica-Resultate als gestapelte Linenplots auszugeben)
- sankeyPlot	(Klasse, um bestimmte Werte von Modelica-Resultaten als Sankey-Diagramm auszugeben)

weitere Klassen könnten folgen...


Verwendung
-----------

Um modelicaPost verwenden zu können, öffne ein Kommandozeilenprogramm im Ordner,
in dem das File modelicaPost.py liegt. Durch den import der Klasse erhälst du zugriff
auf die Funktionen der Klasse. z.B für plotter:

from modelicaPost import plotter


Info zur Verwendung in einem Script:
Die zu plottenden Variablen müssen im Dictionär mit namen "variables" angegeben werden

Beispiel:
instanz.variables = {'label1': {'matFile': matfile-path, 'path': path_inside_matfile, 'origUnit': simulation_unit, 'displayUnit': unit_to_display}, 'label2': {}, ...}



Wie benutze ich eine bestimmte Klasse?
--------------------------------------

Über klasse.help() erhälst du jeweils alle relevanten informationen zur jeweiligen
Klasse. z.B für plotter:

plotter.help()
