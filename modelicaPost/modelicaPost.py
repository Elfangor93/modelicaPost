#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# title:        modelicaPost.py
# description:  This a module to postprocess modelica simulations (Dymola or OpenModelica)
# date:         July 2019
# author:       Manuel Häusler
# email:        manuel.haeusler@hslu.ch
# version:      1.0
#==============================================================================


#----------------------------------
# Base-Klasse der plotter-Klassen
#----------------------------------
class plotter:
    def __init__(self):
        self.delete = False

        # variables to plot
        # provide them as a dictionary {'label': {'matFile': matfile-path, 'path': path_inside_matfile, 'origUnit': simulation_unit, 'displayUnit': unit_to_display, 'customGain': gain}, 'label2': {}, ...}
        self.variables = {}

        # stylesheet
        self.style = 'custom.mplstyle'

        # dimension
        self.height = 15.24  # in cm

        self.title = ''

        self.timeUnit = 's'

        self.showLegend = False
        self.Legend_pos = 'bottom'
        self.Legend_ncol = 3


        # check if the correct python is used  --> buildingspy only works with 2.7
        import platform
        if (('2.7' in platform.python_version()) == False):
            print('Benutze python 2.7, um modelicaPost.plotter nutzen zu koennen.')
            self.delete = True
            return

        # check if all needed modules are installed
        import imp
        modules = ['matplotlib', 'numpy', 'scipy', 'modelicares', 'scimath']
        for m in modules:
            try:
                imp.find_module(m)
            except ImportError:
                print(m + ' wurde nicht gefunden. Bitte installiere ' + m + ', um modelicaPost.plotter nutzen zu koennen.')
                self.delete = True
                return

        # check if the right scimath is used
        exec('from scimath.units.power import *')
        try:
            kW
        except NameError:
            print('Es scheint, dass du eine inkompatible Version von scimath installiert hast.\nInstalliere "https://github.com/19leunam93/scimath", um modelicaPost.plotter nutzen zu koennen.')
            self.delete = True
            return

    # Help-Function
    @staticmethod
    def help():
        print('Dies ist die Base-Class fuer alle Plotter-Klassen. Verfuegbare Plotter-Klassen sind: linePlot, piePlot, stackPlot')
        return

    # Methode, um ein Resultat-File (Variablen-Struktur) zu untersuchen
    def showRes(self, file=''):
        if (file == ''):
            print('Kein .mat-File angegeben. Welches .mat-File soll untersucht werden? (Pfad zum .mat-File angeben)')
            file = raw_input()

        from modelicares import SimRes
        r = SimRes(file)

        try:
            print(r.names)
        except IOError:
            print('Das angegebene .mat-File scheint es nicht zu geben. Funktion "showRes()" wird beendet...')
            return

    # Methode, um neue Modelica-Variablen hinzuzufügen
    def add(self):
        if (self.delete == True):
            return
        print('Was ist der Name der Variable? (Dieser Name wird in der Legende angezeigt)')
        var = raw_input()
        if var in self.variables:
            print('Diese Variable existiert bereits. Funktion "add()" wird beendet...')
            return
        print('In welchem .mat-File ist diese Variable zu finden? (Pfad zum .mat-File angeben)')
        file = raw_input()
        print('Gib den Pfad zur Variable innerhalb des .mat-Files an')
        path = raw_input()

        from modelicares import SimRes
        r = SimRes(file)

        try:
            print('Diese Variable hat die Einheit ' + r[path].unit + '. Einheit aendern? -- Antwort: Y(es), N(o)')
        except LookupError:
            print('Der eingegebene Pfad zur Variable scheint nicht zu existieren. Funktion "add()" wird beendet...')
            return

        antw = raw_input()
        if (antw == 'Y' or antw == 'Yes' or antw == 'y' or antw == 'yes'):
            print('Welche Einheit soll es denn sein?')
            unit = raw_input()
            orig_unit = r[path].unit
        else:
            unit = r[path].unit
            orig_unit = r[path].unit

        print('Soll der Variable noch einen custom Gain hinzugefügt werden?')
        antw = raw_input()
        gain = 1
        if (antw == 'Y' or antw == 'Yes' or antw == 'y' or antw == 'yes'):
            print('Gib den gewünschten Gain ein.')
            gain = num(raw_input())

        self.variables[var] = {'matFile': file, 'path': path, 'origUnit': orig_unit, 'displayUnit': unit, 'customGain': gain}

        # Methode, um Anpassungen an Modelica-Variablen zu machen

    # Methode, um Modelica Variablen zu verändern
    def change(self, var=False):
        if (self.delete == True):
            return
        if (var == False):
            print(self.variables.keys())
            print('Welche Variable soll geaendert werden?')
            var = raw_input()

        print('Was soll geaendert werden: ' + self.variables[var])
        var_conf = raw_input()
        if (var_conf in self.variables[var]):
            print('Wie soll der neue Wert fuer ' + var_conf + ' lauten?')
            self.variables[var][var_conf] = raw_input()
        elif (var_conf in self.variables.keys()):
            old_key = var_conf
            print('Wie soll der neue Name fuer die Variable lauten?')
            new_key = raw_input()
            variables[new_key] = variables[old_key]
            del dictionary[old_key]
        else:
            print('Aenderung in Variable ' + var + ' kann nicht durchgefuehrt werden. Funktion "change()" wird beendet...')
            return

    # Methode, um importierte Modelica-Valiablen zu löschen
    def remove(self, alle=False):
        if (self.delete == True):
            return
        if (alle):
            print('Saemtliche Variablen werden geloescht. Fortfahren? -- Antwort: Y(es), N(o)')
            if (antw == 'Y' or antw == 'Yes' or antw == 'y' or antw == 'yes'):
                self.variables = {}
                print('Variablen wurden gelöscht.')
                return
        else:
            print(self.variables.keys())
            print('Welche Variable soll geloescht werden?')
            var = raw_input()
            if var in self.variables:
                del self.variables[var]
                print('Variable ' + var + ' wurde geloescht...')
            else:
                print('Variable ' + var + ' existiert nicht. Funktion "remove()" wird beendet...')
            return

    # Methode, um alle existierenden Variablen anzuzeigen
    def showVars(self, detailed=False):
        if (self.delete == True):
            return
        if detailed:
            print(self.variables)
        else:
            print(self.variables.keys())
        return

    # Methode, um Einheiten zu konvertieren
    def convertUnit(self, value, unit_from, unit_to):
        if (self.delete == True):
            return
        exec('from scimath.units.SI import *')
        exec('from scimath.units.pressure import *')
        exec('from scimath.units.acceleration import *')
        exec('from scimath.units.angle import *')
        exec('from scimath.units.area import *')
        exec('from scimath.units.density import *')
        exec('from scimath.units.electromagnetism import *')
        exec('from scimath.units.energy import *')
        exec('from scimath.units.force import *')
        exec('from scimath.units.frequency import *')
        exec('from scimath.units.length import *')
        exec('from scimath.units.mass import *')
        exec('from scimath.units.power import *')
        exec('from scimath.units.pressure import *')
        exec('from scimath.units.speed import *')
        exec('from scimath.units.substance import *')
        exec('from scimath.units.temperature import *')
        exec('from scimath.units.time import *')
        exec('from scimath.units.volume import *')
        from scimath.units.api import convert

        try:
            value = convert(value, eval(unit_from), eval(unit_to))
        except:
            print('Einheit "' + unit_from + '" oder "' + unit_to + '" wird nicht unterstuetzt von scimath. Funktion wird beendet...')
            return(False)

        return(value)

    # Methode zur Ausgabe eines standard Plots
    def plot(self):
        if (self.delete == True):
            return(False)

        import matplotlib.pyplot as plt
        import random
        x = [random.randint(0, 20) for p in range(0, 6)]
        plt.plot([0, 1, 2, 3, 4, 5], x)
        return(plt)

    # Methode zum anzeigen einer Ausgabe
    def show(self):
        if (self.delete == True):
            return
        plt = self.plot()
        if (plt == False):
            return
        else:
            plt.show()

    # Methode zum speichern einer Ausgabe
    def save(self, path=''):
        if (self.delete == True):
            return
        if (path == ''):
            print('Gib den Dateinamen des zu speichernden Plot-Images ein.')
            fileName = raw_input() + '.svg'
        else:
            fileName = path + '.svg'
        plt = self.plot()
        if (plt == False):
            return
        else:
            plt.savefig(fileName, format='svg')

    # Methode um Werte einer Variable zu holen
    # Get the recorded values between 0 and 20 seconds: time=(0, 20)
    # Get the interpolated values at 2 and 17 seconds: time=[2, 17]
    # return values
    def getVals(self, varName, time=None):
        if varName in self.variables.keys():
            from modelicares import SimRes
            r = SimRes(self.variables[varName]['matFile'])
            variable = r[self.variables[varName]['path']]
            return variable.values(t=time)
        else:
            print('Die Variable '+varName+' existiert nicht.')

    # Methode um den maximalen Wert einer Variable zu holen
    # return values
    def getMax(self, varName):
        if varName in self.variables.keys():
            from modelicares import SimRes
            r = SimRes(self.variables[varName]['matFile'])
            variable = r[self.variables[varName]['path']]
            return variable.max()
        else:
            print('Die Variable '+varName+' existiert nicht.')

    # Methode um den minimalen Wert einer Variable zu holen
    # return values
    def getMin(self, varName):
        if varName in self.variables.keys():
            from modelicares import SimRes
            r = SimRes(self.variables[varName]['matFile'])
            variable = r[self.variables[varName]['path']]
            return variable.min()
        else:
            print('Die Variable '+varName+' existiert nicht.')
        


#-------------------------------------
# Klasse, um Linen-Plots zu erstellen
#-------------------------------------
class linePlot(plotter):

    def __init__(self):
        # settings
        self.xLabel = 'Time [s]'
        self.yLabel1 = ''
        self.yLabel2 = ''

        self.xLim_upper = None
        self.xLim_bottom = 0
        self.yLim1_upper = None
        self.yLim1_bottom = 0
        self.yLim2_upper = None
        self.yLim2_bottom = 0

        self.yGrid = True

        self.xLog = False
        self.yLog1 = False
        self.yLog2 = False

        plotter.__init__(self)

    # Help-Function
    @staticmethod
    def help():
        txt = '\n\nmodelicaPost.linePlot - HELP\n===============================\n\n'
        txt = txt + 'modelicaPost.linePlot ist eine Klasse, um Resultate von Modelica-Simulationen als Line-Plots mit matplotlib zu plotten.\n\n\n'
        txt = txt + 'Verfuegbare Funktionen:\n-----------------------\n\n'
        txt = txt + '- settings():\t\tEinstellungen fuer den Plot einsehen\n\n'
        txt = txt + '- showRes():\t\tUntersuchen eines .mat-Files. Zeigt alle vorhandenen Variablennamen.\n\n'
        txt = txt + '- add():\t\tLaedt eine neue Modelica-Variable in den Plotter\n\n'
        txt = txt + '- change(var):\t\tAendert einen Eintrag einer Modelica-Variable im Plotter. Um direkt\n\t\t\teine bestimmte Variable zu aendern, setze den Variablennamen als Argument.\n\n'
        txt = txt + '- remove(alle):\t\tLoescht eine existierende Modelica-Variable im Plotter. Um alle\n\t\t\tVariablen miteinander zu loeschen, setzte das Argument "alle" auf True.\n\n'
        txt = txt + '- showVars(detailed):\tZeigt alle geladenen Modelica-Variablen. Setze das Argument "detailed"\n\t\t\tauf true, um eine detailierte Ansicht zu erhalten.\n\n'
        txt = txt + '- show():\t\tAusgabe eines Plots mit allen geladenen Modelica-Variablen in einem Fenster.\n\n'
        txt = txt + '- save(path):\t\tSpeichern eines Plots mit allen geladenen Modelica-Variablen als SVG-Datei\n\t\t\tins aktuelle Verzeichnis. Mit "path" kann ein alternatives Zielverzeichnis\n\t\t\tdefiniert werden.\n'
        txt = txt + '\n\nUm eine Einstellung zu aendern: Instanz.Einstellung = neuer Wert\n\nBeispiel:\n>>> p = linePlot()\t\t\tinitialisieren einer linePlot Instanz\n>>> p.style = "custom.mplstyle"\t\tAendern der Einstellung "style"'
        txt = txt + '\n\n==========END HELP============='
        print(txt)
        return

    # Methode, um die Einstellungen des Plots anzuzeigen
    def settings(self):
        if (self.delete == True):
            return
        txt = '\n\nmodelicaPost.linePlot - EINSTELLUNGEN\n======================================\n\n'
        txt = txt + 'Aktuelle Einstellungen:\n\n'
        txt = txt + 'Einstellung\t\takt. Wert\t\tBeschreibung\n'
        txt = txt + '------------\t\t---------\t\t---------------\n'
        txt = txt + '(1)  style\t\t' + str(self.style) + '\t\tAussehen des Plots. Es koennen eigene Stylesheets geladen werden\n'
        txt = txt + '(2)  height\t\t' + str(self.height) + '\t\t\tPlot groesse - Hoehe in cm. Die Laenge wird daraus berechnet\n'
        txt = txt + '(3)  title\t\t' + str(self.title) + '\t\t\tPlot-Titel. Leer = kein Titel\n'
        txt = txt + '(4)  xLabel\t\t' + str(self.xLabel) + '\t\tLabel der x-Achse. Leer = kein Label\n'
        txt = txt + '(5)  yLabel1\t\t' + str(self.yLabel1) + '\t\t\tLabel der linken y-Achse. Leer = kein Label\n'
        txt = txt + '(6)  yLabel2\t\t' + str(self.yLabel2) + '\t\t\tLabel der rechten y-Achse. Leer = kein Label *\n'
        txt = txt + '(7)  xLim_upper\t\t' + str(self.xLim_upper) + '\t\t\tObere Limite der x-Achse. None = kein Limit\n'
        txt = txt + '(8)  xLim_bottom\t' + str(self.xLim_bottom) + '\t\t\tUntere Limite der x-Achse.\n'
        txt = txt + '(9)  yLim1_upper\t' + str(self.yLim1_upper) + '\t\t\tObere Limite der linken y-Achse. None = kein Limit\n'
        txt = txt + '(10) yLim1_bottom\t' + str(self.yLim1_bottom) + '\t\t\tUntere Limite der linken y-Achse.\n'
        txt = txt + '(11) yLim2_upper\t' + str(self.yLim2_upper) + '\t\t\tObere Limite der rechten y-Achse. None = kein Limit *\n'
        txt = txt + '(12) yLim2_bottom\t' + str(self.yLim2_bottom) + '\t\t\tUntere Limite der rechten y-Achse. *\n'
        txt = txt + '(13) xLog\t\t' + str(self.xLog) + '\t\t\tLogarithmische x-Achse.\n'
        txt = txt + '(14) yLog1\t\t' + str(self.yLog1) + '\t\t\tLogarithmische, linke y-Achse.\n'
        txt = txt + '(15) yLog2\t\t' + str(self.yLog2) + '\t\t\tLogarithmische, rechte y-Achse. *\n'
        txt = txt + '(16) yGrid\t\t' + str(self.yGrid) + '\t\t\tSoll das Hilfsgitter der y-Achse angezeicht werden?\n'
        txt = txt + '(17) showLegend\t\t' + str(self.showLegend) + '\t\t\tSoll eine Legende angezeigt werden?\n'
        txt = txt + '(18) Legend_pos\t\t' + str(self.Legend_pos) + '\t\t\tPositionierung der Legende. Moegliche Positionen: bottom, right, left\n'
        txt = txt + '(19) Legend_ncol\t' + str(self.Legend_ncol) + '\t\t\tAnzahl Kolonnen in der Legende.\n'
        txt = txt + '(20) timeUnit\t' + str(self.timeUnit) + '\t\t\tEinheit der Zeit-Achse.\n'
        txt = txt + '\n*: Nur, falls Variabeln mit zwei verschiedenen Einheiten geladen und dadurch zwei Achsen notwendig sind.\n'
        txt = txt + '\n\nUm eine Einstellung zu aendern: Instanz.Einstellung = neuer Wert\n\nBeispiel:\n>>> p = linePlot()\t\t\tinitialisieren einer linePlot Instanz\n>>> p.style = "custom.mplstyle"\t\tAendern der Einstellung "style"'
        txt = txt + '\n\n==========END EINSTELLUNGEN============='
        print(txt)
        return

    # Methode zur Ausgabe eines Linienplots mit allen Variabeln
    def plot(self):
        if (self.delete == True):
            return(False)
        import matplotlib.pyplot as plt
        plt.style.use(self.style)
        height_inch = float(self.height) / 2.54

        # initialize axis
        axis_name = []
        for key in self.variables:
            if (self.variables[key]['displayUnit'] not in axis_name):
                axis_name.append(self.variables[key]['displayUnit'])
        if (len(axis_name) < 1):
            print('Keine Variabelen zum plotten vorhanden. Fuege zuerst mit add() einige Variablen hinzu!')
            return(False)
        elif (len(axis_name) == 1):
            if (self.Legend_pos == 'bottom' or self.showLegend == False):
                width_inch = (height_inch / 3) * 4
                fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))
            else:
                width_inch = (height_inch / 10) * 16
                fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))
        elif (len(axis_name) == 2):
            width_inch = (height_inch / 9) * 16
            fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))
            ax2 = ax1.twinx()
            ax1.set_prop_cycle(color=['e41a1c', '981a1c', 'c9333e', 'b81d38', 'b32d26'])
            ax2.set_prop_cycle(color=['377eb8', '255585', '3c5dc9', '2c4391', '3698e3'])
            ax1.tick_params(axis='y', labelcolor='#e41a1c')
            ax2.tick_params(axis='y', labelcolor='#377eb8')
        else:
            print('Zu viele Variablen vorhanden. Der Plot kann Variablen mit maximal zwei Einheiten (für zwei Achsen darstellen). Loesche zuerst mit remove() einige Variablen!')
            return(False)

        from modelicares import SimRes

        n = 0
        # Loop through all the variables
        for key in self.variables:
            # Read the result Files
            r = SimRes(self.variables[key]['matFile'])
            variable = r[self.variables[key]['path']]
            # Get the values of the variables
            t = variable.times()
            y = variable.values()

            # calculate the correct units
            if (self.timeUnit != 's'):
                t = self.convertUnit(t, 's', self.timeUnit)
            y = self.convertUnit(y, self.variables[key]['origUnit'], self.variables[key]['displayUnit'])

            try:
                if (y == False):
                    return(False)
            except ValueError:
                pass

            # calculate the custom gain
            if 'customGain' in self.variables[key]:
                y = self.variables[key]['customGain'] * y

            # Plot the variables
            if (self.variables[key]['displayUnit'] == axis_name[0]):
                ax1.plot(t, y, label=str(key))
            elif (self.variables[key]['displayUnit'] == axis_name[1]):
                ax2.plot(t, y, label=str(key))
            n = n + 1

        # apply the settings
        #----------------------
        if (self.title != ''):
            plt.title(str(self.title))

        # Label settings
        ax1.set_xlabel(self.xLabel)
        if (self.yLabel1 != ''):
            ax1.set_ylabel(str(self.yLabel1))
        if (self.yLabel1 != '' and len(axis_name) == 2):
            ax1.set_ylabel(str(self.yLabel1), color='#e41a1c')
        if (self.yLabel2 != '' and len(axis_name) == 2):
            ax2.set_ylabel(str(self.yLabel2), color='#377eb8')

        # Axis limits settings
        if (self.xLim_upper != None):
            ax1.set_xlim((self.xLim_bottom, self.xLim_upper))
        if (self.yLim1_upper != None):
            ax1.set_ylim((self.yLim1_bottom, self.yLim1_upper))
        else:
            ax1.set_xlim(left=self.xLim_bottom)
            ax1.set_ylim(bottom=self.yLim1_bottom)
        if (self.yLim2_upper != None and len(axis_name) == 2):
            ax2.set_ylim((self.yLim2_bottom, self.yLim2_upper))
        elif (len(axis_name) == 2):
            ax2.set_ylim(bottom=self.yLim2_bottom)

        # Axis Scales
        if (self.xLog):
            ax1.set_xscale('symlog', linthreshx=1)
        if (self.yLog1):
            ax1.set_yscale('symlog', linthreshy=1)
        if (self.yLog2):
            ax2.set_yascale('symlog', linthreshy=1)

        # legend settings
        if (self.showLegend):

            if (len(axis_name) == 1):
                if (self.yGrid == False):
                    ax1.yaxis.grid(False)
                if (self.Legend_pos == 'bottom'):
                    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=self.Legend_ncol)
                    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.9, wspace=None, hspace=None)
                elif (self.Legend_pos == 'right'):
                    ax1.legend(loc='upper center', bbox_to_anchor=(1.15, 0.5), fancybox=True, shadow=True, ncol=self.Legend_ncol)
                    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.8, top=0.9, wspace=None, hspace=None)
                elif (self.Legend_pos == 'left'):
                    ax1.legend(loc='upper center', bbox_to_anchor=(-0.2, 0.5), fancybox=True, shadow=True, ncol=self.Legend_ncol)
                    plt.subplots_adjust(left=0.22, bottom=0.1, right=0.95, top=0.9, wspace=None, hspace=None)

            if (len(axis_name) == 2):
                if (self.yGrid == False):
                    ax1.yaxis.grid(False)
                    ax2.yaxis.grid(False)
                ax1.legend(loc='upper center', bbox_to_anchor=(-0.2, 0.5), ncol=self.Legend_ncol)
                ax2.legend(loc='upper center', bbox_to_anchor=(1.2, 0.5), ncol=self.Legend_ncol)
                plt.subplots_adjust(left=0.2, bottom=0.1, right=0.8, top=0.9, wspace=None, hspace=None)

        # creating the two axis layout
        if (len(axis_name) == 2):
            fig.tight_layout()

        return(plt)


#----------------------------------------------------------
# Klasse, um Grafiken für Grössenverhältnisse zu erstellen
#----------------------------------------------------------
class piePlot(plotter):
    def __init__(self):
        # settings
        self.total = 100
        self.startangle = 0
        self.evalValue = 'mean'
        self.explode = False

        plotter.__init__(self)

        self.Legend_pos = 'right'
        self.Legend_ncol = 1

    # Help-Function
    @staticmethod
    def help():
        txt = '\n\nmodelicaPost.piePlot - HELP\n===============================\n\n'
        txt = txt + 'modelicaPost.piePlot ist eine Klasse, um Resultate von Modelica-Simulationen als Pie-Plots mit matplotlib zu plotten.\n\n\n'
        txt = txt + 'Verfuegbare Funktionen:\n-----------------------\n\n'
        txt = txt + '- settings():\t\tEinstellungen fuer den Plot einsehen\n\n'
        txt = txt + '- showRes():\t\tUntersuchen eines .mat-Files. Zeigt alle vorhandenen Variablennamen.\n\n'
        txt = txt + '- add():\t\tLaedt eine neue Modelica-Variable in den Plotter\n\n'
        txt = txt + '- change(var):\t\tAendert einen Eintrag einer Modelica-Variable im Plotter. Um direkt\n\t\t\teine bestimmte Variable zu aendern, setze den Variablennamen als Argument.\n\n'
        txt = txt + '- remove(alle):\t\tLoescht eine existierende Modelica-Variable im Plotter. Um alle\n\t\t\tVariablen miteinander zu loeschen, setzte das Argument "alle" auf True.\n\n'
        txt = txt + '- showVars(detailed):\tZeigt alle geladenen Modelica-Variablen. Setze das Argument "detailed"\n\t\t\tauf true, um eine detailierte Ansicht zu erhalten.\n\n'
        txt = txt + '- show():\t\tAusgabe eines Plots mit allen geladenen Modelica-Variablen in einem Fenster.\n\n'
        txt = txt + '- save(path):\t\tSpeichern eines Plots mit allen geladenen Modelica-Variablen als SVG-Datei\n\t\t\tins aktuelle Verzeichnis. Mit "path" kann ein alternatives Zielverzeichnis\n\t\t\tdefiniert werden.\n'
        txt = txt + '\n\nUm eine Einstellung zu aendern: Instanz.Einstellung = neuer Wert\n\nBeispiel:\n>>> p = piePlot()\t\t\tinitialisieren einer piePlot Instanz\n>>> p.style = "custom.mplstyle"\t\tAendern der Einstellung "style"'
        txt = txt + '\n\n==========END HELP============='
        print(txt)
        return

    # Methode, um die Einstellungen des Plots anzuzeigen
    def settings(self):
        if (self.delete == True):
            return
        txt = '\n\nmodelicaPost.piePlot - EINSTELLUNGEN\n======================================\n\n'
        txt = txt + 'Aktuelle Einstellungen:\n\n'
        txt = txt + 'Einstellung\t\takt. Wert\t\tBeschreibung\n'
        txt = txt + '------------\t\t---------\t\t---------------\n'
        txt = txt + '(1)  style\t\t' + str(self.style) + '\t\tAussehen des Plots. Es koennen eigene Stylesheets geladen werden\n'
        txt = txt + '(2)  height\t\t' + str(self.height) + '\t\t\tPlot groesse - Hoehe in cm. Die Laenge wird daraus berechnet\n'
        txt = txt + '(3)  title\t\t' + str(self.title) + '\t\t\tPlot-Titel. Leer = kein Titel\n'
        txt = txt + '(4)  total\t\t' + str(self.total) + '\t\t\tVerhaeltnisvariable. (z.B  fuer Prozent: 100 / Promille: 1000)\n'
        txt = txt + '(5)  startangle\t\t' + str(self.startangle) + '\t\t\tDrehung des Pie-Plots\n'
        txt = txt + '(6)  evalValue\t\t' + str(self.evalValue) + '\t\t\tWelcher Wert soll zum plotten verwendet werden?\n\t\t\t\t\t\t(Verfuegbar: t=10, mean, max, min, rms, ini, final)*\n'
        txt = txt + '(7)  showLegend\t\t' + str(self.showLegend) + '\t\t\tSoll eine Legende angezeigt werden?\n'
        txt = txt + '(8)  Legend_pos\t\t' + str(self.Legend_pos) + '\t\t\tPositionierung der Legende. Moegliche Positionen: right, left\n'
        txt = txt + '(9)  Legend_ncol\t' + str(self.Legend_ncol) + '\t\t\tAnzahl Kolonnen in der Legende.\n'
        txt = txt + '(10) explode\t\t' + str(self.explode) + '\t\t\tName der hervorgehobenen Variable. False = Keine hervorgehobene Variable\n'
        txt = txt + '\n*: Falls ein Wert bei einer bestimmten Simulationszeit verwendet werden soll: z.B Wert bei 10 sekunden -> t=10'
        txt = txt + '\n\nUm eine Einstellung zu aendern: Instanz.Einstellung = neuer Wert\n\nBeispiel:\n>>> p = piePlot()\t\t\tinitialisieren einer piePlot Instanz\n>>> p.style = "custom.mplstyle"\t\tAendern der Einstellung "style"'
        txt = txt + '\n\n==========END EINSTELLUNGEN============='
        print(txt)
        return

    def plot(self):
        labels = []
        data = []
        from array import array
        explode = array('f', [0] * len(self.variables))

        if (len(self.variables) < 1):
            print('Keine Variabelen zum plotten vorhanden. Fuege zuerst mit add() einige Variablen hinzu!')
            return(False)

        from modelicares import SimRes

        n = 0
        # Loop through all the variables
        for key in self.variables:
            # Read the result Files
            r = SimRes(self.variables[key]['matFile'])
            variable = r[self.variables[key]['path']]
            # Get the values of the variables
            if (self.evalValue == 'max'):
                y = variable.max()
            elif (self.evalValue == 'mean'):
                y = variable.mean()
            elif (self.evalValue == 'min'):
                y = variable.min()
            elif (self.evalValue == 'rms'):
                y = variable.RMS()
            elif (self.evalValue == 'ini'):
                y = variable.IV()
            elif (self.evalValue == 'final'):
                y = variable.FV()
            else:
                time = self.evalValue.split('=')
                y = variable.values(t=time[1])

            # calculate the correct units
            y = self.convertUnit(y, self.variables[key]['origUnit'], self.variables[key]['displayUnit'])

            try:
                if (y == False):
                    return(False)
            except ValueError:
                pass

            # calculate the custom gain
            if 'customGain' in self.variables[key]:
                y = self.variables[key]['customGain'] * y

            # Append the variable data to the data-Array
            data.append(y)

            # Append the labels to the lables-Array
            labels.append(key)

            # Change value for exploded slices
            if (self.explode != False and key == self.explode):
                explode[n] = 0.1

            n = n + 1

        import matplotlib.pyplot as plt
        plt.style.use(self.style)
        height_inch = float(self.height) / 2.54
        width_inch = (height_inch / 3) * 4

        fig, ax = plt.subplots(figsize=(width_inch, height_inch), subplot_kw=dict(aspect="equal"))

        def func(pct, allvals):
            import numpy as np
            if (self.total == 1000):
                absolute = int(pct / 1000. * np.sum(allvals))
                return "{:.1f}".format(pct, absolute) + u"\u2030"
            else:
                absolute = int(pct / 100. * np.sum(allvals))
                return "{:.1f}".format(pct, absolute) + u"\u0025"

        wedges, texts, autotexts = ax.pie(data, explode=explode, autopct=lambda pct: func(pct, data), shadow=True, startangle=self.startangle)

        if (self.title != ''):
            ax.set_title(self.title)

        if (self.showLegend):
            if (self.Legend_pos == 'left'):
                ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(-0.28, 0, 0.5, 1), fancybox=True, shadow=True, ncol=self.Legend_ncol)
            else:
                ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fancybox=True, shadow=True, ncol=self.Legend_ncol)

        return(plt)


#----------------------------------------------------------
# Klasse, um Grafiken für Grössenverhältnisse zu erstellen
#----------------------------------------------------------
class stackPlot(plotter):
    def __init__(self):
        # settings
        self.xLabel = 'Time [s]'
        self.yLabel = ''

        self.xLim_upper = None
        self.xLim_bottom = 0
        self.yLim_upper = None
        self.yLim_bottom = 0

        self.xLog = False
        self.yLog = False

        self.yGrid = True

        plotter.__init__(self)

    # Help-Function
    @staticmethod
    def help():
        txt = '\n\nmodelicaPost.stackPlot - HELP\n===============================\n\n'
        txt = txt + 'modelicaPost.stackPlot ist eine Klasse, um Resultate von Modelica-Simulationen als Stack-Plots mit matplotlib zu plotten.\n\n\n'
        txt = txt + 'Verfuegbare Funktionen:\n-----------------------\n\n'
        txt = txt + '- settings():\t\tEinstellungen fuer den Plot einsehen\n\n'
        txt = txt + '- showRes():\t\tUntersuchen eines .mat-Files. Zeigt alle vorhandenen Variablennamen.\n\n'
        txt = txt + '- add():\t\tLaedt eine neue Modelica-Variable in den Plotter\n\n'
        txt = txt + '- change(var):\t\tAendert einen Eintrag einer Modelica-Variable im Plotter. Um direkt\n\t\t\teine bestimmte Variable zu aendern, setze den Variablennamen als Argument.\n\n'
        txt = txt + '- remove(alle):\t\tLoescht eine existierende Modelica-Variable im Plotter. Um alle\n\t\t\tVariablen miteinander zu loeschen, setzte das Argument "alle" auf True.\n\n'
        txt = txt + '- showVars(detailed):\tZeigt alle geladenen Modelica-Variablen. Setze das Argument "detailed"\n\t\t\tauf true, um eine detailierte Ansicht zu erhalten.\n\n'
        txt = txt + '- show():\t\tAusgabe eines Plots mit allen geladenen Modelica-Variablen in einem Fenster.\n\n'
        txt = txt + '- save(path):\t\tSpeichern eines Plots mit allen geladenen Modelica-Variablen als SVG-Datei\n\t\t\tins aktuelle Verzeichnis. Mit "path" kann ein alternatives Zielverzeichnis\n\t\t\tdefiniert werden.\n'
        txt = txt + '\n\nUm eine Einstellung zu aendern: Instanz.Einstellung = neuer Wert\n\nBeispiel:\n>>> p = stackPlot()\t\t\tinitialisieren einer stackPlot Instanz\n>>> p.style = "custom.mplstyle"\t\tAendern der Einstellung "style"'
        txt = txt + '\n\n==========END HELP============='
        print(txt)
        return

    # Methode, um die Einstellungen des Plots anzuzeigen
    def settings(self):
        if (self.delete == True):
            return
        txt = '\n\nmodelicaPost.stackPlot - EINSTELLUNGEN\n======================================\n\n'
        txt = txt + 'Aktuelle Einstellungen:\n\n'
        txt = txt + 'Einstellung\t\takt. Wert\t\tBeschreibung\n'
        txt = txt + '------------\t\t---------\t\t---------------\n'
        txt = txt + '(1)  style\t\t' + str(self.style) + '\t\tAussehen des Plots. Es koennen eigene Stylesheets geladen werden\n'
        txt = txt + '(2)  height\t\t' + str(self.height) + '\t\t\tPlot groesse - Hoehe in cm. Die Laenge wird daraus berechnet\n'
        txt = txt + '(3)  title\t\t' + str(self.title) + '\t\t\tPlot-Titel. Leer = kein Titel\n'
        txt = txt + '(4)  xLabel\t\t' + str(self.xLabel) + '\t\tLabel der x-Achse. Leer = kein Label\n'
        txt = txt + '(5)  yLabel\t\t' + str(self.yLabel) + '\t\t\tLabel der y-Achse. Leer = kein Label\n'
        txt = txt + '(7)  xLim_upper\t\t' + str(self.xLim_upper) + '\t\t\tObere Limite der x-Achse. None = kein Limit\n'
        txt = txt + '(8)  xLim_bottom\t' + str(self.xLim_bottom) + '\t\t\tUntere Limite der x-Achse.\n'
        txt = txt + '(9)  yLim_upper\t\t' + str(self.yLim_upper) + '\t\t\tObere Limite der y-Achse. None = kein Limit\n'
        txt = txt + '(10) yLim_bottom\t' + str(self.yLim_bottom) + '\t\t\tUntere Limite der y-Achse.\n'
        txt = txt + '(11) xLog\t\t' + str(self.xLog) + '\t\t\tLogarithmische x-Achse.\n'
        txt = txt + '(12) yLog\t\t' + str(self.yLog) + '\t\t\tLogarithmische y-Achse.\n'
        txt = txt + '(13) yGrid\t\t' + str(self.yGrid) + '\t\t\tSoll das Hilfsgitter der y-Achse angezeicht werden?\n'
        txt = txt + '(14) showLegend\t\t' + str(self.showLegend) + '\t\t\tSoll eine Legende angezeigt werden?\n'
        txt = txt + '(15) Legend_pos\t\t' + str(self.Legend_pos) + '\t\t\tPositionierung der Legende. Moegliche Positionen: bottom, right, left\n'
        txt = txt + '(16) Legend_ncol\t' + str(self.Legend_ncol) + '\t\t\tAnzahl Kolonnen in der Legende.\n'
        txt = txt + '(17) timeUnit\t\t' + str(self.timeUnit) + '\t\t\tEinheit der Zeit-Achse.\n'
        txt = txt + '\n\nUm eine Einstellung zu aendern: Instanz.Einstellung = neuer Wert\n\nBeispiel:\n>>> p = stackPlot()\t\t\tinitialisieren einer stackPlot Instanz\n>>> p.style = "custom.mplstyle"\t\tAendern der Einstellung "style"'
        txt = txt + '\n\n==========END EINSTELLUNGEN============='
        print(txt)
        return

    # Method zur Ausgabe eines Linienplots mit allen Variabeln
    def plot(self):
        if (self.delete == True):
            return(False)

        if (len(self.variables) < 1):
            print('Keine Variabelen zum plotten vorhanden. Fuege zuerst mit add() einige Variablen hinzu!')
            return(False)

        import matplotlib.pyplot as plt
        plt.style.use(self.style)
        height_inch = float(self.height) / 2.54

        # initialize axis
        if (self.Legend_pos == 'bottom' or self.showLegend == False):
            width_inch = (height_inch / 3) * 4
            fig, ax = plt.subplots(figsize=(width_inch, height_inch))
        else:
            width_inch = (height_inch / 10) * 16
            fig, ax = plt.subplots(figsize=(width_inch, height_inch))

        from modelicares import SimRes

        n = 0
        values = []
        time = []
        labels = []
        # Loop through all the variables
        for key in self.variables:
            # Read the result Files
            r = SimRes(self.variables[key]['matFile'])
            variable = r[self.variables[key]['path']]
            # Get the values of the variables
            t = variable.times()
            y = variable.values()

            # calculate the correct units
            if (self.timeUnit != 's'):
                t = self.convertUnit(t, 's', self.timeUnit)
            y = self.convertUnit(y, self.variables[key]['origUnit'], self.variables[key]['displayUnit'])

            try:
                if (y == False):
                    return(False)
            except ValueError:
                pass

            # calculate the custom gain
            if 'customGain' in self.variables[key]:
                y = self.variables[key]['customGain'] * y

            # save the variables
            if (n == 0):
                time = t
            values.append(y)
            labels.append(key)

            n = n + 1

        # create the plot
        ax.stackplot(time, values, labels=labels)

        # apply the settings
        #----------------------
        if (self.title != ''):
            plt.title(str(self.title))

        # Label settings
        ax.set_xlabel(self.xLabel)
        if (self.yLabel != ''):
            ax.set_ylabel(str(self.yLabel))

        # Axis limits settings
        if (self.xLim_upper != None):
            ax.set_xlim((self.xLim_bottom, self.xLim_upper))
        if (self.yLim_upper != None):
            ax.set_ylim((self.yLim_bottom, self.yLim_upper))
        else:
            ax.set_xlim(left=self.xLim_bottom)
            ax.set_ylim(bottom=self.yLim_bottom)

        # Axis Scales
        if (self.xLog):
            ax.set_xscale('symlog', linthreshx=1)
        if (self.yLog):
            ax.set_yscale('symlog', linthreshy=1)

        # legend settings
        if (self.showLegend):

            if (self.yGrid == False):
                ax.yaxis.grid(False)
            if (self.Legend_pos == 'bottom'):
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=self.Legend_ncol)
                plt.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.9, wspace=None, hspace=None)
            elif (self.Legend_pos == 'right'):
                ax.legend(loc='upper center', bbox_to_anchor=(1.15, 0.5), fancybox=True, shadow=True, ncol=self.Legend_ncol)
                plt.subplots_adjust(left=0.1, bottom=0.1, right=0.8, top=0.9, wspace=None, hspace=None)
            elif (self.Legend_pos == 'left'):
                ax.legend(loc='upper center', bbox_to_anchor=(-0.2, 0.5), fancybox=True, shadow=True, ncol=self.Legend_ncol)
                plt.subplots_adjust(left=0.22, bottom=0.1, right=0.95, top=0.9, wspace=None, hspace=None)

        return(plt)
