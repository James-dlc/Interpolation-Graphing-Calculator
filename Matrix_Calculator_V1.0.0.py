"""
Team Matrix
CSc 191 - Senior Project
Version 2.0.0

Matrix Calculator
"""
import tkinter as tk                      # GUI library
import matplotlib.pyplot as plt           # graphing library
import numpy as np                        # numerical processing
import webbrowser                         # webbrowsing library
import xlrd                               # excel library
import Pmw                                # information for widgets

from tkinter import filedialog            # dialog to save a file
from tkinter.commondialog import Dialog   # dialog to confirm save
from tkinter import messagebox            # messagebox for about info
from tkinter import ttk                   # scrollbars for frame
from tkinter import Frame                 # tkinter frames
from tkinter import Canvas                # tkinter canvas
from PIL import Image, ImageTk            # image library
from prettytable import PrettyTable       # table for x-y points

mainWindow = None

class MatrixCalculator:
    def __init__(self, parent):
        self.parent = parent
        self.mainMenuGUI(parent)

        global mainWindow
        mainWindow = self.parent

    def mainMenuGUI(self, parent):
        frame = setFrame(parent) #Setting frame size and settings

        self.titleText = tk.Label(frame, text="Matrix Calculator", font=("Cooper Black", 75), fg = "navy", bg="white")
        self.approximationButton = tk.Button(frame, text = "Approximation", fg = "navy", bg = "wheat", highlightbackground = "yellow",
                                             font=("Georgia Pro Black", 40), height=1, width=20, borderwidth=15, overrelief = "groove",
                                             command = lambda: self.controlWindow(Approximation))
        self.interpolationButton = tk.Button(frame, text = "Interpolation", fg = "navy", bg = "wheat", highlightbackground = "yellow",
                                             font=("Georgia Pro Black", 40), height=1, width=20, borderwidth=15, overrelief = "groove",
                                             command = lambda: self.controlWindow(Interpolation))
        self.graphingButton = tk.Button(frame, text = "Graphing", fg = "navy", bg = "wheat", highlightbackground = "yellow",
                                        font=("Georgia Pro Black", 40), height=1, width=20, borderwidth=15, overrelief = "groove",
                                        command = lambda: self.controlWindow(Graphing))
        self.xyTableButton = tk.Button(frame, text = "X-Y Table", fg = "navy", bg = "wheat", highlightbackground = "yellow",
                                       font=("Georgia Pro Black", 40), height=1, width=20, borderwidth=15, overrelief = "groove",
                                       command = lambda: self.controlWindow(XY_Table))

        #Displaying texts and buttons as geometry grid
        self.titleText.place(x=40, y=40)
        self.approximationButton.place(x=175, y=200)
        self.interpolationButton.place(x=175, y=400)
        self.graphingButton.place(x=175, y=600)
        self.xyTableButton.place(x=175, y=800)


    def controlWindow(self, _class):
        hideWindow()
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self.parent)
            _class(self.new)

class Approximation:
    def __init__(self, parent):
        #Pairs (X & Y) input store
        self.x1 = tk.StringVar()
        self.y1 = tk.StringVar()
        self.x2 = tk.StringVar()
        self.y2 = tk.StringVar()
        self.x3 = tk.StringVar()
        self.y3 = tk.StringVar()

        #Imported data values
        self.xData = []
        self.yData = []

        #X-Window input store
        self.xLow = tk.IntVar(parent, -10)
        self.xHigh = tk.IntVar(parent, 10)

        #Checkbox input store
        self.gridVal = tk.IntVar()
        self.highlightVal = tk.IntVar()
        self.darkVal = tk.IntVar()

        #Radio button input store
        self.equationVal = tk.IntVar()
        self.equationVal.set(1)

        #Store polynomial degree value
        self.degree = tk.IntVar()

        #Graph name store
        self.graphTitle = tk.StringVar()
        self.xAxisTitle = tk.StringVar()
        self.yAxisTitle = tk.StringVar()

        self.approximationGUI(parent)

        #Set initial window
        self.setWindow(parent)
        self.setWindowData(parent)
        
        #Call when attempt to close window
        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(parent))

    def setWindow(self, parent):
        file = open("ApproximationSaved.txt","r")
        lines = file.readlines()
        state = int(float(lines[0]))

        if(state == -1):
            try:
                self.x1.set(lines[1])
                self.y1.set(lines[2])
                self.x2.set(lines[3])
                self.y2.set(lines[4])
                self.x3.set(lines[5])
                self.y3.set(lines[6])
                self.xLow.set(int(lines[7]))
                self.xHigh.set(int(lines[8]))
                self.equationVal.set(int(lines[9]))
                self.degree.set(int(lines[10]))
                self.gridVal.set(int(lines[11]))
                self.darkVal.set(int(lines[12]))
                self.highlightVal.set(int(lines[13]))
                self.graphTitle.set(str(lines[14].strip()))
                self.xAxisTitle.set(str(lines[15].strip()))
                self.yAxisTitle.set(str(lines[16].strip()))
            except:
                pass

    def closeWindow(self, parent):
        answer = tk.messagebox.askyesnocancel("Matrix Calculator", "Do you want to save the data?", icon = "warning")
        if answer:
            self.closeWindowData(parent)
            data = ("-1\n%g\n%g\n" % (float(self.x1.get()), float(self.y1.get())))
            data += ("%g\n%g\n" % (float(self.x2.get()), float(self.y2.get())))
            data += ("%g\n%g\n" % (float(self.x3.get()), float(self.y3.get())))
            data += ("%d\n%d\n" % (int(self.xLow.get()), int(self.xHigh.get())))
            data += ("%d\n%d\n" % (int(self.equationVal.get()), int(self.degree.get())))
            data += ("%d\n%d\n" % (int(self.gridVal.get()), int(self.darkVal.get())))
            data += ("%d\n" % (int(self.highlightVal.get())))
            
            file = open("ApproximationSaved.txt","w")
            file.writelines(data)
            file.write(str(self.graphTitle.get()))
            file.write("\n")
            file.write(str(self.xAxisTitle.get()))
            file.write("\n")
            file.write(str(self.yAxisTitle.get()))
            file.close()
            
            self.parent.destroy()
            showWindow()

        elif answer is None:
            pass

        else:
            self.parent.destroy()
            showWindow()

    def setWindowData(self, parent):
        try:
            if(float(self.x1.get()) == 0.0001):
                self.x1.set("")
            if(float(self.x2.get()) == 0.0001):
                self.x2.set("")
            if(float(self.x3.get()) == 0.0001):
                self.x3.set("")

            if(float(self.y1.get()) == 0.0001):
                self.y1.set("")
            if(float(self.y2.get()) == 0.0001):
                self.y2.set("")
            if(float(self.y3.get()) == 0.0001):
                self.y3.set("")
        except:
            pass

    def closeWindowData(self, parent):
        if(self.x1.get() == ""):
            self.x1.set("0.0001")
        if(self.x2.get() == ""):
            self.x2.set("0.0001")
        if(self.x3.get() == ""):
            self.x3.set("0.0001")

        if(self.y1.get() == ""):
            self.y1.set("0.0001")
        if(self.y2.get() == ""):
            self.y2.set("0.0001")
        if(self.y3.get() == ""):
            self.y3.set("0.0001")

    def approximationGUI(self, parent):
        self.parent = parent      #Initial
        setWindow(parent)         #Setting window size and settings
        frame = setFrame(parent)  #Setting frame size and settings

        #Title and information labels
        parent.titleText = tk.Label(frame, text="Approximation", font=("Cooper Black", 45))
        parent.accuracyImage = ImageTk.PhotoImage(Image.open("accuracyImage.png"))
        parent.accuracyImageLabel = tk.Label(frame, image = parent.accuracyImage)

        #Graph text labels
        parent.graphTitleText = tk.Label(frame, text="Graph Title:", font=("Times New Roman", 22))
        parent.xAxisTitleText = tk.Label(frame, text="X-axis Title:", font=("Times New Roman", 22))
        parent.yAxisTitleText = tk.Label(frame, text="Y-axis Title:", font=("Times New Roman", 22))

        #Graph text entries
        parent.graphTitleEntry = tk.Entry(frame, width=20, fg="purple", font=("Times New Roman", 22), textvariable=self.graphTitle)
        parent.xAxisTitleEntry = tk.Entry(frame, width=20, fg="purple", font=("Times New Roman", 22), textvariable=self.xAxisTitle)
        parent.yAxisTitleEntry = tk.Entry(frame, width=20, fg="purple", font=("Times New Roman", 22), textvariable=self.yAxisTitle)

        #Buttons for function
        parent.approximateButton = tk.Button(frame, text = "Approximate", overrelief = "groove", borderwidth=7, bg = "thistle", fg = "purple", font=("Times New Roman", 24), command=self.approximate)
        parent.importDataButton = tk.Button(frame, text = "Import Data", overrelief = "groove", borderwidth=7, bg = "thistle", fg = "purple", font=("Times New Roman", 24), command=self.importData)
        parent.viewPointsButton = tk.Button(frame, text = "View Points", overrelief = "groove", borderwidth=7, bg = "thistle", fg = "purple", font=("Times New Roman", 24), command=self.viewPoints)
        parent.clearButton = tk.Button(frame, text = "Clear", overrelief = "groove", borderwidth=7, bg = "purple", fg = "thistle", font=("Times New Roman", 24), command=self.clear)
        parent.helpButton = tk.Button(frame, bitmap = "question", width = 40, height = 60, borderwidth=3, overrelief = "groove", fg = "purple", bg = "thistle", command=self.help)

        #Check buttons and Radio Buttons
        parent.equationTypeText = tk.Label(frame, text="Select Equation Type:", font=("Times New Roman", 28))
        parent.chkHighlight = tk.Checkbutton(frame, text="Highlight Data Points", font=("Times New Roman", 25), variable=self.highlightVal)
        parent.chkGrid = tk.Checkbutton(frame, text="Grid", font=("Times New Roman", 25), variable=self.gridVal)
        parent.radioPolynomial = tk.Radiobutton(frame, text="Polynomial", font=("Times New Roman", 25), variable=self.equationVal, value=1)
        parent.radioLogarithmic = tk.Radiobutton(frame, text="Logarithmic", font=("Times New Roman", 25), variable=self.equationVal, value=2)
        parent.radioExponential = tk.Radiobutton(frame, text="Exponential", font=("Times New Roman", 25), variable=self.equationVal, value=3)
        parent.chkDark = tk.Checkbutton(frame, text="Dark Mode", font=("Times New Roman", 25), variable=self.darkVal)

        #X range text labels
        parent.xLowText = tk.Label(frame, text="X Low:", font=("Times New Roman", 22))
        parent.xHighText = tk.Label(frame, text="X High:", font=("Times New Roman", 20))

        #X range text entries
        parent.xLowEntry = tk.Entry(frame, width=6, fg="purple", font=("Times New Roman", 22), textvariable=self.xLow)
        parent.xHighEntry = tk.Entry(frame, width=6, fg="purple", font=("Times New Roman", 22), textvariable=self.xHigh)

        #Degree text label
        parent.degreeText = tk.Label(frame, text="Degree: ", font=("Times New Roman", 24))

        #Degree text entry
        parent.degreeEntry = tk.Entry(frame, width=4, fg="purple", font=("Times New Roman", 24), textvariable=self.degree)

        #Pairs (X & Y)text labels
        parent.x1Text = tk.Label(frame, text="X1: ", font=("Times New Roman", 24))
        parent.x2Text = tk.Label(frame, text="X2: ", font=("Times New Roman", 24))
        parent.x3Text = tk.Label(frame, text="X3: ", font=("Times New Roman", 24))
        parent.y1Text = tk.Label(frame, text="Y1: ", font=("Times New Roman", 24))
        parent.y2Text = tk.Label(frame, text="Y2: ", font=("Times New Roman", 24))
        parent.y3Text = tk.Label(frame, text="Y3: ", font=("Times New Roman", 24))

        #Pairs (X & Y) text entries
        parent.x1Entry = tk.Entry(frame, width=8, fg="purple", font=("Times New Roman", 24), textvariable=self.x1)
        parent.x2Entry = tk.Entry(frame, width=8, fg="purple", font=("Times New Roman", 24), textvariable=self.x2)
        parent.x3Entry = tk.Entry(frame, width=8, fg="purple", font=("Times New Roman", 24), textvariable=self.x3)
        parent.y1Entry = tk.Entry(frame, width=8, fg="purple", font=("Times New Roman", 24), textvariable=self.y1)
        parent.y2Entry = tk.Entry(frame, width=8, fg="purple", font=("Times New Roman", 24), textvariable=self.y2)
        parent.y3Entry = tk.Entry(frame, width=8, fg="purple", font=("Times New Roman", 24), textvariable=self.y3)

        #Display of all labels, entries, and buttons
        parent.titleText.place(x=275, y=15)
        parent.accuracyImageLabel.place(x=110, y=115)

        parent.x1Text.place(x=50, y=500)
        parent.x1Entry.place(x=110, y=500)

        parent.y1Text.place(x=250, y=500)
        parent.y1Entry.place(x=310, y=500)

        parent.x2Text.place(x=50, y=575)
        parent.x2Entry.place(x=110, y=575)

        parent.y2Text.place(x=250, y=575)
        parent.y2Entry.place(x=310, y=575)

        parent.x3Text.place(x=50, y=650)
        parent.x3Entry.place(x=110, y=650)

        parent.y3Text.place(x=250, y=650)
        parent.y3Entry.place(x=310, y=650)

        parent.xLowText.place(x=50, y=725)
        parent.xHighText.place(x=250, y=725)
        parent.xLowEntry.place(x=150, y=725)
        parent.xHighEntry.place(x=350, y=725)

        parent.graphTitleText.place(x=50, y=800)
        parent.graphTitleEntry.place(x=200, y=800)

        parent.xAxisTitleText.place(x=50, y=860)
        parent.xAxisTitleEntry.place(x=200, y=860)

        parent.yAxisTitleText.place(x=50, y=920)
        parent.yAxisTitleEntry.place(x=200, y=920)

        parent.degreeText.place(x=740, y=525)
        parent.degreeEntry.place(x=850, y=527)

        parent.equationTypeText.place(x=500,y=460)
        parent.radioPolynomial.place(x=550,y=520)
        parent.radioLogarithmic.place(x=550,y=570)
        parent.radioExponential.place(x=550,y=620)
        parent.chkGrid.place(x=550, y=670)
        parent.chkHighlight.place(x=650, y=670)
        parent.chkDark.place(x=550, y=720)

        parent.approximateButton.place(x=550, y=775)
        parent.importDataButton.place(x=550, y=880)
        parent.viewPointsButton.place(x=770, y=775)
        parent.clearButton.place(x=770, y=880)

        parent.helpButton.place(x=910, y=420)

    def help(self):
        helpWindow = tk.Tk()
        helpWindow.title("Matrix Calculator")
        ScrollBar = tk.Scrollbar(helpWindow)
        textBox = tk.Text(helpWindow, height=20, width=100, font=("Times New Roman", 16))
        ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        textBox.pack(side=tk.LEFT, fill=tk.Y)
        ScrollBar.config(command=textBox.yview)
        textBox.config(yscrollcommand=ScrollBar.set)
        with open("ApproximationInfo.txt", "r", encoding="utf8") as f:
            text = f.read()
        textBox.insert(tk.END, text)

    def importData(self):
        self.xData = []
        self.yData = []

        fileName = filedialog.askopenfilename(title="Matrix Calculator")

        try:
            excelFile = xlrd.open_workbook(fileName)
            sheet = excelFile.sheet_by_index(0)

            tk.messagebox.showinfo(title="Matrix Calculator", message="Import successful!")

            for value in sheet.col_values(0):
                if isinstance(value, float):
                    self.xData.append(value)

            for value in sheet.col_values(1):
                if isinstance(value, float):
                    self.yData.append(value)

        except FileNotFoundError:
            pass

        except:
            tk.messagebox.showerror(title="Matrix Calculator", message="Unexpected error. Try again!")
            self.importData()
            pass

        if(len(self.xData) != len(self.yData)):
            tk.messagebox.showerror(parent=self.parent, title="Matrix Calculator", message="Unbalanced number of X's and Y's. Try again!")
            self.importData()

    def addPoints(self):
        try:
            float(self.x1.get())
        except:
            if self.x1.get() =="" and self.y1.get() !="":
                tk.messagebox.showwarning(title="Error in 'X1 & Y1' entry box", message="Please do not leave the 'X1' entry box emtpy.")
                pass
            elif self.x1.get()=="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X1' entry box", message="Please enter a number into entry box 'X1'")
                pass

        try:
            float(self.y1.get())
        except:
            if self.y1.get() =="" and self.x1.get() !="":
                tk.messagebox.showwarning(title="Error in 'X1 & Y1' entry box", message="Please do not leave the 'Y1' entry box emtpy.")
                pass
            elif self.y1.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y1' entry box", message="Please enter a number into entry box 'Y1'")
                pass

        try:
            float(self.x2.get())
        except:
            if self.x2.get() =="" and self.y2.get() !="":
                tk.messagebox.showwarning(title="Error in 'X2 & Y2' entry box", message="Please do not leave the 'X2' entry box emtpy.")
                pass
            elif self.x2.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X2' entry box", message="Please enter a number into entry box 'X2'")
                pass

        try:
            float(self.y2.get())
        except:
            if self.y2.get() =="" and self.x2.get() !="":
                tk.messagebox.showwarning(title="Error in 'X2 & Y2' entry box", message="Please do not leave the 'Y2' entry box emtpy.")
                pass
            elif self.y2.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y2' entry box", message="Please enter a number into entry box 'Y2'")
                pass

        try:
            float(self.x3.get())
        except:
            if self.x3.get() =="" and self.y3.get() !="":
                tk.messagebox.showwarning(title="Error in 'X3 & Y3' entry box", message="Please do not leave the 'X3' entry box emtpy.")
                pass
            elif self.x3.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X3' entry box", message="Please enter a number into entry box 'X3'")
                pass

        try:
            float(self.y3.get())
        except:
            if self.y3.get() =="" and self.x3.get() !="":
                tk.messagebox.showwarning(title="Error in 'X3 & Y3' entry box", message="Please do not leave the 'Y3' entry box emtpy.")
                pass
            elif self.y3.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y3' entry box", message="Please enter a number into entry box 'Y3'")
                pass

        x = []
        y = []

        if self.x1.get() != "":
            x.append(float (self.x1.get()))
        if self.x2.get() != "":
            x.append(float (self.x2.get()))
        if self.x3.get() != "":
            x.append(float (self.x3.get()))

        if self.y1.get() != "":
            y.append(float (self.y1.get()))
        if self.y2.get() != "":
            y.append(float (self.y2.get()))
        if self.y3.get() != "":
            y.append(float (self.y3.get()))

        if(len(self.xData) > 0):
            return self.xData, self.yData
        else:
            return x, y

    def clear(self):
        answer = tk.messagebox.askquestion ('Matrix Calculator','Are you sure you want to clear all data?',icon = 'warning')
        if answer == 'yes':
            self.x1.set("")
            self.y1.set("")
            self.x2.set("")
            self.y2.set("")
            self.x3.set("")
            self.y3.set("")
            self.darkVal.set(0)
            self.xLow.set(-10)
            self.xHigh.set(10)
            self.gridVal.set(0)
            self.highlightVal.set(0)
            self.equationVal.set(1)
            self.graphTitle.set("")
            self.xAxisTitle.set("")
            self.yAxisTitle.set("")
            self.xData = []
            self.yData = []

        # if answer is 'no' then does nothing

    def viewPoints(self):
        xMin = 1
        xMax = -1
        yMin = 1
        yMax = -1

        x, y = self.addPoints()

        for i in range(0, len(x)):
            if(x[i] < xMin):
                xMin = x[i]
            if(x[i] > xMax):
                xMax = x[i]
            if(y[i] < yMin):
                yMin = y[i]
            if(y[i] > yMax):
                yMax = y[i]

        xMin = xMin - 5
        xMax = xMax + 5
        yMin = yMin - 5
        yMax = yMax + 5

        # Create the plot
        plt.close(1)
        if(self.darkVal.get() == 1):
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        plt.title(self.graphTitle.get())
        plt.xlabel(self.xAxisTitle.get())
        plt.ylabel(self.yAxisTitle.get())
        plt.plot(x, y, 'bo')
        if(self.gridVal.get() == 1):
            plt.grid(True)
        else:
            plt.grid(False)
        plt.axis([xMin, xMax, yMin, yMax])
        plt.pause(0.00001)

    def approximate(self):
        if(self.equationVal.get() == 1):
            self.polynomialDataFitting()
        elif(self.equationVal.get() == 2):
            self.logarithmicDataFitting()
        elif(self.equationVal.get() == 3):
            self.exponentialDataFitting()

    def xyDataArrayProcessor(self):
        x, y = self.addPoints()
        xNP = np.zeros(shape=(len(x),1), dtype=float)
        yNP = np.zeros(shape=(len(y),1), dtype=float)

        xLowVal = int (self.xLow.get())
        xHighVal = int (self.xHigh.get())

        for i in range(0, len(x)):
            xNP = np.insert(xNP, i, x[i])
            xNP = np.delete(xNP, len(x))

        for i in range(0, len(y)):
            yNP = np.insert(yNP, i, y[i])
            yNP = np.delete(yNP, len(y))

        return xNP, yNP

    def logarithmicDataFitting(self):
        xNP, yNP = self.xyDataArrayProcessor()

        xValue = np.linspace(int (self.xLow.get()), int (self.xHigh.get()), 1000)
        a, b = np.polyfit(np.log(xNP), yNP, 1)

        # Create the plot
        plt.close(1)
        if(self.darkVal.get() == 1):
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        plt.title(self.graphTitle.get())
        plt.xlabel(self.xAxisTitle.get())
        plt.ylabel(self.yAxisTitle.get())
        if(self.highlightVal.get() == 1):
            plt.plot(xNP, yNP, 'bo', xValue, (a*np.log(xValue) + b), 'g-')
            plt.legend(['Point', 'Logarithm: F(X)'], loc="upper left")
        else:
            plt.plot(xValue, (a*np.log(xValue) + b), 'b-')
            plt.legend("Logarithm: F(X)", loc="upper left")
        if(self.gridVal.get() == 1):
            plt.grid(True)
        else:
            plt.grid(False)
        plt.pause(0.00001)

    def exponentialDataFitting(self):
        xNP, yNP = self.xyDataArrayProcessor()
        xValue = np.linspace(int (self.xLow.get()), int (self.xHigh.get()), 1000)

        #Taking natural log of both sides of our data points
        xData = np.log(xNP)
        yData = np.log(yNP)

        #Solving for a and b using numpy polynomial fit
        a, b = np.polyfit(xNP, yData, 1)

        # Create the plot
        plt.close(1)
        if(self.darkVal.get() == 1):
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        plt.title(self.graphTitle.get())
        plt.xlabel(self.xAxisTitle.get())
        plt.ylabel(self.yAxisTitle.get())
        if(self.highlightVal.get() == 1):
            plt.plot(xNP, yNP, 'bo', xValue, np.exp(b) * np.exp(a*xValue), 'g-')
            plt.legend(['Point', 'Exponential: F(X)'], loc="upper left")
        else:
            plt.plot(xValue, (a*np.exp(b*xValue)), 'b-')
            plt.legend("Exponential: F(X)", loc="upper left")
        if(self.gridVal.get() == 1):
            plt.grid(True)
        else:
            plt.grid(False)
        plt.pause(0.00001)

    def polynomialDataFitting(self):
        xNP, yNP = self.xyDataArrayProcessor()
        xValue = np.linspace(int (self.xLow.get()), int (self.xHigh.get()), 1000)

        coefficients = np.polyfit(xNP, yNP, int (self.degree.get()))

        yValue = 0
        for i in range(len(coefficients)):
            yValue += coefficients[(len(coefficients)-1) - i]*xValue**i

        print("Coefficents: ", coefficients)

        # Create the plot
        plt.close(1)
        if(self.darkVal.get() == 1):
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        plt.title(self.graphTitle.get())
        plt.xlabel(self.xAxisTitle.get())
        plt.ylabel(self.yAxisTitle.get())
        if(self.highlightVal.get() == 1):
            plt.plot(xNP, yNP, 'bo', xValue, yValue, 'g-')
            plt.legend(['Point', 'Polynomial: F(X)'], loc="upper left")
        else:
            plt.plot(xValue, yValue, 'b-')
            plt.legend("Polynomial: F(X)", loc="upper left")
        if(self.gridVal.get() == 1):
            plt.grid(True)
        else:
            plt.grid(False)
        plt.pause(0.00001)

class Interpolation:
    def __init__(self, parent):
        #Pairs (X & Y) input store
        self.x1 = tk.StringVar(parent,"")
        self.y1 = tk.StringVar(parent,"")
        self.x2 = tk.StringVar(parent,"")
        self.y2 = tk.StringVar(parent,"")
        self.x3 = tk.StringVar(parent,"")
        self.y3 = tk.StringVar(parent,"")
        self.x4 = tk.StringVar(parent,"")
        self.y4 = tk.StringVar(parent,"")
        self.x5 = tk.StringVar(parent,"")
        self.y5 = tk.StringVar(parent,"")

        #Imported data values
        self.xData = []
        self.yData = []

        #X-Window input store
        self.xLow = tk.StringVar(parent, -10)
        self.xHigh = tk.StringVar(parent, 10)

        #Checkbox input store
        self.gridVal = tk.IntVar()
        self.highlightVal = tk.IntVar()
        self.darkVal = tk.IntVar()

        #Graph and axis title input store
        self.graphTitle = tk.StringVar()
        self.xAxisTitle = tk.StringVar()
        self.yAxisTitle = tk.StringVar()

        self.interpolationGUI(parent)

        #Set initial window
        self.setWindow(parent)
        self.setWindowData(parent)
        
        #Call when attempt to close window
        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(parent))

    def setWindow(self, parent):
        file = open("InterpolationSaved.txt","r")
        lines = file.readlines()
        state = int(float(lines[0]))

        if(state == -1):
            try:
                self.x1.set(lines[1])
                self.y1.set(lines[2])
                self.x2.set(lines[3])
                self.y2.set(lines[4])
                self.x3.set(lines[5])
                self.y3.set(lines[6])
                self.x4.set(lines[7])
                self.y4.set(lines[8])
                self.x5.set(lines[9])
                self.y5.set(lines[10])
                self.xLow.set(int(lines[11]))
                self.xHigh.set(int(lines[12]))
                self.gridVal.set(int(lines[13]))
                self.darkVal.set(int(lines[14]))
                self.highlightVal.set(int(lines[15]))
                self.graphTitle.set(str(lines[16].strip()))
                self.xAxisTitle.set(str(lines[17].strip()))
                self.yAxisTitle.set(str(lines[18].strip()))
            except:
                pass

    def closeWindow(self, parent):
        answer = tk.messagebox.askyesnocancel("Matrix Calculator", "Do you want to save the data?", icon = "warning")
        if answer:
            self.closeWindowData(parent)
            data = ("-1\n%g\n%g\n" % (float(self.x1.get()), float(self.y1.get())))
            data += ("%g\n%g\n" % (float(self.x2.get()), float(self.y2.get())))
            data += ("%g\n%g\n" % (float(self.x3.get()), float(self.y3.get())))
            data += ("%g\n%g\n" % (float(self.x4.get()), float(self.y4.get())))
            data += ("%g\n%g\n" % (float(self.x5.get()), float(self.y5.get())))
            data += ("%d\n%d\n" % (int(self.xLow.get()), int(self.xHigh.get())))
            data += ("%d\n%d\n" % (int(self.gridVal.get()), int(self.darkVal.get())))
            data += ("%d\n" % (int(self.highlightVal.get())))
            
            file = open("InterpolationSaved.txt","w")
            file.writelines(data)
            file.write(str(self.graphTitle.get()))
            file.write("\n")
            file.write(str(self.xAxisTitle.get()))
            file.write("\n")
            file.write(str(self.yAxisTitle.get()))
            file.close()
            
            self.parent.destroy()
            showWindow()

        elif answer is None:
            pass

        else:
            self.parent.destroy()
            showWindow()

    def setWindowData(self, parent):
        try:
            if(float(self.x1.get()) == 0.0001):
                self.x1.set("")
            if(float(self.x2.get()) == 0.0001):
                self.x2.set("")
            if(float(self.x3.get()) == 0.0001):
                self.x3.set("")
            if(float(self.x4.get()) == 0.0001):
                self.x4.set("")
            if(float(self.x5.get()) == 0.0001):
                self.x5.set("")

            if(float(self.y1.get()) == 0.0001):
                self.y1.set("")
            if(float(self.y2.get()) == 0.0001):
                self.y2.set("")
            if(float(self.y3.get()) == 0.0001):
                self.y3.set("")
            if(float(self.y4.get()) == 0.0001):
                self.y4.set("")
            if(float(self.y5.get()) == 0.0001):
                self.y5.set("")
        except:
            pass

    def closeWindowData(self, parent):
        if(self.x1.get() == ""):
            self.x1.set("0.0001")
        if(self.x2.get() == ""):
            self.x2.set("0.0001")
        if(self.x3.get() == ""):
            self.x3.set("0.0001")
        if(self.x4.get() == ""):
            self.x4.set("0.0001")
        if(self.x5.get() == ""):
            self.x5.set("0.0001")

        if(self.y1.get() == ""):
            self.y1.set("0.0001")
        if(self.y2.get() == ""):
            self.y2.set("0.0001")
        if(self.y3.get() == ""):
            self.y3.set("0.0001")
        if(self.y4.get() == ""):
            self.y4.set("0.0001")
        if(self.y5.get() == ""):
            self.y5.set("0.0001")

    def interpolationGUI(self, parent):
        self.parent = parent      #Initial
        setWindow(parent)         #Setting window size and settings
        frame = setFrame(parent)  #Setting frame size and settings

        #Title and information labels
        parent.titleText = tk.Label(frame, text="Interpolation Graphing", font=("Cooper Black", 45))
        parent.interpolationImage = ImageTk.PhotoImage(Image.open("interpolationImage.png"))
        parent.interpolationImageLabel = tk.Label(frame, image = parent.interpolationImage)
        parent.enterPairsText = tk.Label(frame, text="Enter the X & Y Pairs to be Plotted:", font=("Times New Roman", 20))

        #Graph text labels
        parent.graphTitleText = tk.Label(frame, text="Graph Title:", font=("Times New Roman", 22))
        parent.xAxisTitleText = tk.Label(frame, text="X-axis Title:", font=("Times New Roman", 22))
        parent.yAxisTitleText = tk.Label(frame, text="Y-axis Title:", font=("Times New Roman", 22))

        #Graph text entries
        parent.graphTitleEntry = tk.Entry(frame, width=20, fg="navy", font=("Times New Roman", 22), textvariable=self.graphTitle)
        parent.xAxisTitleEntry = tk.Entry(frame, width=20, fg="navy", font=("Times New Roman", 22), textvariable=self.xAxisTitle)
        parent.yAxisTitleEntry = tk.Entry(frame, width=20, fg="navy", font=("Times New Roman", 22), textvariable=self.yAxisTitle)

        #Buttons for function
        parent.interpolateButton = tk.Button(frame, text = "Interpolate", overrelief = "groove", borderwidth=7, bg = "lavender", fg = "navy", font=("Times New Roman", 24), command=self.interpolate)
        parent.clearButton = tk.Button(frame, text = "Clear", overrelief = "groove", borderwidth=7, bg = "navy", fg = "lavender", font=("Times New Roman", 24), command=self.clear)
        parent.viewPointsButton = tk.Button(frame, text = "View Points", overrelief = "groove", borderwidth=7, fg = "navy", bg = "lavender", font=("Times New Roman", 24), command=self.viewPoints)
        parent.importDataButton = tk.Button(frame, text = "Import Data", overrelief = "groove", borderwidth=7, fg = "navy", bg = "lavender", font=("Times New Roman", 24), command=self.importData)
        parent.helpButton = tk.Button(frame, bitmap = "question", width = 40, height = 60, borderwidth=3, overrelief = "groove", fg = "navy", bg = "lavender", command=self.help)

        #Check buttons
        parent.chkGrid = tk.Checkbutton(frame, text="Grid", font=("Times New Roman", 25), variable=self.gridVal)
        parent.chkHighlight = tk.Checkbutton(frame, text="Highlight Data Points", font=("Times New Roman", 25), variable=self.highlightVal)
        parent.chkDark = tk.Checkbutton(frame, text="Dark Mode", font=("Times New Roman", 25), variable=self.darkVal)

        #X range text labels
        parent.xLowText = tk.Label(frame, text="X Low:", font=("Times New Roman", 22))
        parent.xHighText = tk.Label(frame, text="X High:", font=("Times New Roman", 20))

        #X range text entries
        parent.xLowEntry = tk.Entry(frame, width=6, fg="navy", font=("Times New Roman", 22), textvariable=self.xLow)
        parent.xHighEntry = tk.Entry(frame, width=6, fg="navy", font=("Times New Roman", 22), textvariable=self.xHigh)

        #Pairs (X & Y)text labels
        parent.x1Text = tk.Label(frame, text="X1: ", font=("Times New Roman", 24))
        parent.x2Text = tk.Label(frame, text="X2: ", font=("Times New Roman", 24))
        parent.x3Text = tk.Label(frame, text="X3: ", font=("Times New Roman", 24))
        parent.x4Text = tk.Label(frame, text="X4: ", font=("Times New Roman", 24))
        parent.x5Text = tk.Label(frame, text="X5: ", font=("Times New Roman", 24))
        parent.y1Text = tk.Label(frame, text="Y1: ", font=("Times New Roman", 24))
        parent.y2Text = tk.Label(frame, text="Y2: ", font=("Times New Roman", 24))
        parent.y3Text = tk.Label(frame, text="Y3: ", font=("Times New Roman", 24))
        parent.y4Text = tk.Label(frame, text="Y4: ", font=("Times New Roman", 24))
        parent.y5Text = tk.Label(frame, text="Y5: ", font=("Times New Roman", 24))

        #Pairs (X & Y) text entries
        parent.x1Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.x1)
        parent.x2Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.x2)
        parent.x3Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.x3)
        parent.x4Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.x4)
        parent.x5Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.x5)
        parent.y1Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.y1)
        parent.y2Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.y2)
        parent.y3Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.y3)
        parent.y4Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.y4)
        parent.y5Entry = tk.Entry(frame, width=8, fg="royalblue", font=("Times New Roman", 24), textvariable=self.y5)

        #Display of all labels, entries, and buttons
        parent.titleText.place(x=175, y=15)
        parent.interpolationImageLabel.place(x=110, y=115)
        parent.enterPairsText.place(x=50, y=450)

        parent.x1Text.place(x=50, y=500)
        parent.x1Entry.place(x=110, y=500)

        parent.y1Text.place(x=250, y=500)
        parent.y1Entry.place(x=310, y=500)

        parent.x2Text.place(x=50, y=575)
        parent.x2Entry.place(x=110, y=575)

        parent.y2Text.place(x=250, y=575)
        parent.y2Entry.place(x=310, y=575)

        parent.x3Text.place(x=50, y=650)
        parent.x3Entry.place(x=110, y=650)

        parent.y3Text.place(x=250, y=650)
        parent.y3Entry.place(x=310, y=650)

        parent.x4Text.place(x=550, y=500)
        parent.x4Entry.place(x=610, y=500)

        parent.y4Text.place(x=750, y=500)
        parent.y4Entry.place(x=810, y=500)

        parent.x5Text.place(x=550, y=575)
        parent.x5Entry.place(x=610, y=575)

        parent.y5Text.place(x=750, y=575)
        parent.y5Entry.place(x=810, y=575)

        parent.xLowText.place(x=50, y=725)
        parent.xHighText.place(x=250, y=725)
        parent.xLowEntry.place(x=150, y=725)
        parent.xHighEntry.place(x=350, y=725)

        parent.chkGrid.place(x=550, y=650)
        parent.chkHighlight.place(x=550, y=700)
        parent.chkDark.place(x=675, y=650)

        parent.graphTitleText.place(x=50, y=800)
        parent.graphTitleEntry.place(x=200, y=800)

        parent.xAxisTitleText.place(x=50, y=860)
        parent.xAxisTitleEntry.place(x=200, y=860)

        parent.yAxisTitleText.place(x=50, y=920)
        parent.yAxisTitleEntry.place(x=200, y=920)

        parent.clearButton.place(x=770, y=880)
        parent.viewPointsButton.place(x=750, y=775)
        parent.interpolateButton.place(x=550, y=775)
        parent.importDataButton.place(x=550, y=880)

        parent.helpButton.place(x=910, y=420)

        #Initial focus set to coefficient (a)
        parent.x1Entry.focus_set()

    def help(self):
        helpWindow = tk.Tk()
        helpWindow.title("Matrix Calculator")
        ScrollBar = tk.Scrollbar(helpWindow)
        textBox = tk.Text(helpWindow, height=20, width=100, font=("Times New Roman", 16))
        ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        textBox.pack(side=tk.LEFT, fill=tk.Y)
        ScrollBar.config(command=textBox.yview)
        textBox.config(yscrollcommand=ScrollBar.set)
        with open("InterpolationInfo.txt", "r", encoding="utf8") as f:
            text = f.read()
        textBox.insert(tk.END, text)

    def clear(self):
        answer = tk.messagebox.askquestion ('Matrix Calculator','Are you sure you want to clear all data?',icon = 'warning')
        if answer == 'yes':
            self.x1.set("")
            self.y1.set("")
            self.x2.set("")
            self.y2.set("")
            self.x3.set("")
            self.y3.set("")
            self.x4.set("")
            self.y4.set("")
            self.x5.set("")
            self.y5.set("")
            self.xLow.set(-10)
            self.xHigh.set(10)
            self.gridVal.set(0)
            self.highlightVal.set(0)
            self.darkVal.set(0)
            self.graphTitle.set("")
            self.xAxisTitle.set("")
            self.yAxisTitle.set("")
            self.xData = []
            self.yData = []

        # if answer is 'no' then does nothing

    def importData(self):
        self.xData = []
        self.yData = []

        fileName = filedialog.askopenfilename(title="Matrix Calculator")

        try:
            excelFile = xlrd.open_workbook(fileName)
            sheet = excelFile.sheet_by_index(0)

            tk.messagebox.showinfo(title="Matrix Calculator", message="Import successful!")

            for value in sheet.col_values(0):
                if isinstance(value, float):
                    self.xData.append(value)

            for value in sheet.col_values(1):
                if isinstance(value, float):
                    self.yData.append(value)

        except FileNotFoundError:
            pass

        except:
            tk.messagebox.showerror(title="Matrix Calculator", message="Unexpected error. Try again!")
            self.importData()
            pass

        if(len(self.xData) != len(self.yData)):
            tk.messagebox.showerror(parent=self.parent, title="Matrix Calculator", message="Unbalanced number of X's and Y's. Try again!")
            self.importData()

    def addPoints(self):

        try:
            float(self.x1.get())
        except:
            if self.x1.get() =="" and self.y1.get() !="":
                tk.messagebox.showwarning(title="Error in 'X1 & Y1' entry box", message="Please do not leave the 'X1' entry box emtpy.")
                pass
            elif self.x1.get()=="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X1' entry box", message="Please enter a number into entry box 'X1'")
                pass

        try:
            float(self.y1.get())
        except:
            if self.y1.get() =="" and self.x1.get() !="":
                tk.messagebox.showwarning(title="Error in 'X1 & Y1' entry box", message="Please do not leave the 'Y1' entry box emtpy.")
                pass
            elif self.y1.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y1' entry box", message="Please enter a number into entry box 'Y1'")
                pass

        try:
            float(self.x2.get())
        except:
            if self.x2.get() =="" and self.y2.get() !="":
                tk.messagebox.showwarning(title="Error in 'X2 & Y2' entry box", message="Please do not leave the 'X2' entry box emtpy.")
                pass
            elif self.x2.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X2' entry box", message="Please enter a number into entry box 'X2'")
                pass

        try:
            float(self.y2.get())
        except:
            if self.y2.get() =="" and self.x2.get() !="":
                tk.messagebox.showwarning(title="Error in 'X2 & Y2' entry box", message="Please do not leave the 'Y2' entry box emtpy.")
                pass
            elif self.y2.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y2' entry box", message="Please enter a number into entry box 'Y2'")
                pass

        try:
            float(self.x3.get())
        except:
            if self.x3.get() =="" and self.y3.get() !="":
                tk.messagebox.showwarning(title="Error in 'X3 & Y3' entry box", message="Please do not leave the 'X3' entry box emtpy.")
                pass
            elif self.x3.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X3' entry box", message="Please enter a number into entry box 'X3'")
                pass

        try:
            float(self.y3.get())
        except:
            if self.y3.get() =="" and self.x3.get() !="":
                tk.messagebox.showwarning(title="Error in 'X3 & Y3' entry box", message="Please do not leave the 'Y3' entry box emtpy.")
                pass
            elif self.y3.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y3' entry box", message="Please enter a number into entry box 'Y3'")
                pass

        try:
            float(self.x4.get())
        except:
            if self.x4.get() =="" and self.y4.get() !="":
                tk.messagebox.showwarning(title="Error in 'X4 & Y4' entry box", message="Please do not leave the 'X4' entry box emtpy.")
                pass
            elif self.x4.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X4' entry box", message="Please enter a number into entry box 'X4'")
                pass

        try:
            float(self.y4.get())
        except:
            if self.y4.get() =="" and self.x4.get() !="":
                tk.messagebox.showwarning(title="Error in 'X4 & Y4' entry box", message="Please do not leave the 'Y4' entry box emtpy.")
                pass
            elif self.y4.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y4' entry box", message="Please enter a number into entry box 'Y4'")
                pass

        try:
            float(self.x5.get())
        except:
            if self.x5.get() =="" and self.y5.get() !="":
                tk.messagebox.showwarning(title="Error in 'X5 & Y5' entry box", message="Please do not leave the 'X5' entry box emtpy.")
                pass
            elif self.x5.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'X5' entry box", message="Please enter a number into entry box 'X5'")
                pass

        try:
            float(self.y5.get())
        except:
            if self.y5.get() =="" and self.x5.get() !="":
                tk.messagebox.showwarning(title="Error in 'X5 & Y5' entry box", message="Please do not leave the 'Y5' entry box emtpy.")
                pass
            elif self.y5.get() =="":
                pass
            else:
                tk.messagebox.showwarning(title="Error in 'Y5' entry box", message="Please enter a number into entry box 'Y5'")
                pass

        x = []
        y = []

        if self.x1.get() != "":
            x.append(float (self.x1.get()))
        if self.x2.get() != "":
            x.append(float (self.x2.get()))
        if self.x3.get() != "":
            x.append(float (self.x3.get()))
        if self.x4.get() != "":
            x.append(float (self.x4.get()))
        if self.x5.get() != "":
            x.append(float (self.x5.get()))

        if self.y1.get() != "":
            y.append(float (self.y1.get()))
        if self.y2.get() != "":
            y.append(float (self.y2.get()))
        if self.y3.get() != "":
            y.append(float (self.y3.get()))
        if self.y4.get() != "":
            y.append(float (self.y4.get()))
        if self.y5.get() != "":
            y.append(float (self.y5.get()))

        if(len(self.xData) > 0):
            return self.xData, self.yData
        else:
            return x, y

    def viewPoints(self):
        xMin = 1
        xMax = -1
        yMin = 1
        yMax = -1

        x, y = self.addPoints()

        for i in range(0, len(x)):
            if(x[i] < xMin):
                xMin = x[i]
            if(x[i] > xMax):
                xMax = x[i]
            if(y[i] < yMin):
                yMin = y[i]
            if(y[i] > yMax):
                yMax = y[i]

        xMin = xMin - 5
        xMax = xMax + 5
        yMin = yMin - 5
        yMax = yMax + 5

        # Create the plot
        plt.close(1)
        if(self.darkVal.get() == 1):
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        plt.title(self.graphTitle.get())
        plt.xlabel(self.xAxisTitle.get())
        plt.ylabel(self.yAxisTitle.get())
        plt.plot(x, y, 'bo')
        if(self.gridVal.get() == 1):
            plt.grid(True)
        else:
            plt.grid(False)
        plt.axis([xMin, xMax, yMin, yMax])
        plt.pause(0.00001)

    def interpolate(self):
        x, y = self.addPoints()
        xNP = np.zeros(shape=(len(x),1), dtype=float)
        yNP = np.zeros(shape=(len(y),1), dtype=float)

        try:
            xLowVal = int (self.xLow.get())
        except:
            if self.xLow.get() =="":
                tk.messagebox.showwarning(title="Error in 'X Low' entry box", message="Please do not leave the 'X Low' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'X Low' entry box", message="Please enter a number into entry box 'X Low'")

        try:
            xHighVal = int (self.xHigh.get())
        except:
            if self.xHigh.get() =="":
                tk.messagebox.showwarning(title="Error in 'X High' entry box", message="Please do not leave the 'X High' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'X High' entry box", message="Please enter a number into entry box 'X High'")

        for i in range(0, len(x)):
            xNP = np.insert(xNP, i, x[i])
            xNP = np.delete(xNP, len(x))

        for i in range(0, len(y)):
            yNP = np.insert(yNP, i, y[i])
            yNP = np.delete(yNP, len(y))

        xValue = np.linspace(xLowVal, xHighVal, 1000)
        yValue = np.array([], float)

        for xp in xValue:
            yp = 0

            for xi,yi in zip(xNP,yNP):
                yp += yi * np.prod((xp - xNP[xNP != xi])/(xi - xNP[xNP != xi]))
            yValue = np.append(yValue, yp)

        # Create the plot
        plt.close(1)
        if(self.darkVal.get() == 1):
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        plt.title(self.graphTitle.get())
        plt.xlabel(self.xAxisTitle.get())
        plt.ylabel(self.yAxisTitle.get())
        if(self.highlightVal.get() == 1):
            plt.plot(xNP, yNP, 'bo', xValue, yValue, 'g-')
            plt.legend(['Point', 'F(X)'], loc="upper left")
        else:
            plt.plot(xValue, yValue, 'b-')
            plt.legend("F(X)", loc="upper left")
        if(self.gridVal.get() == 1):
            plt.grid(True)
        else:
            plt.grid(False)
        plt.pause(0.00001)

class Graphing:
    def __init__(self, parent):

        #Initial window
        self.parent = parent      

        # Current plot number
        self.pltNum = 0

        #Coefficients input store
        self.a = tk.StringVar(parent, "0.0")
        self.b = tk.StringVar(parent, "0.0")
        self.c = tk.StringVar(parent, "0.0")
        self.d = tk.StringVar(parent, "0.0")
        self.e = tk.StringVar(parent, "0.0")
        self.f = tk.StringVar(parent, "0.0")
        self.g = tk.StringVar(parent, "0.0")
        self.h = tk.StringVar(parent, "0.0")

        #Imported coefficients and degrees
        self.coefficient = []
        self.degree = []

        #X-Window input store
        self.xLow = tk.StringVar(parent, -10)
        self.xHigh = tk.StringVar(parent, 10)

        #Graph and axis title input store
        self.graphTitle = tk.StringVar()
        self.xAxisTitle = tk.StringVar()
        self.yAxisTitle = tk.StringVar()

        #Precision input store
        self.precision = tk.StringVar(parent, 0.001)

        #Checkbox input store
        self.gridVal = tk.IntVar()
        self.darkVal = tk.IntVar()

        #Call to set graphing GUI
        self.graphingGUI(parent)

        #Set initial window
        self.setWindow(parent)
        
        #Call when attempt to close window
        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(parent))

    def setWindow(self, parent):
        file = open("GraphingSaved.txt","r")
        lines = file.readlines()
        state = int(float(lines[0]))

        if(state == -1):
            self.a.set(float(lines[1]))
            self.b.set(float(lines[2]))
            self.c.set(float(lines[3]))
            self.d.set(float(lines[4]))
            self.e.set(float(lines[5]))
            self.f.set(float(lines[6]))
            self.g.set(float(lines[7]))
            self.h.set(float(lines[8]))
            self.xLow.set(int(lines[9]))
            self.xHigh.set(int(lines[10]))
            self.gridVal.set(int(lines[11]))
            self.darkVal.set(int(lines[12]))
            self.precision.set(lines[13])
            self.graphTitle.set(lines[14])
            self.xAxisTitle.set(lines[15])
            self.yAxisTitle.set(lines[16])

    def closeWindow(self, parent):
        answer = tk.messagebox.askquestion ("Matrix Calculator", "Do you want to save the data?", icon = "warning")
        if answer == 'yes':
            data = ("-1\n%f\n%f\n%f\n%f\n%f\n%f\n%f\n%f\n" % (float(self.a.get()), float(self.b.get()), float(self.c.get()),
                                                              float(self.d.get()), float(self.e.get()), float(self.f.get()),
                                                              float(self.g.get()), float(self.h.get())))
            data += ("%d\n%d\n" % (int(self.xLow.get()), int(self.xHigh.get())))
            data += ("%d\n%d\n" % (int(self.gridVal.get()), int(self.darkVal.get())))
            data += self.precision.get() + "\n"
            data += self.graphTitle.get() + " " + "\n" + self.xAxisTitle.get() + " " + "\n" + self.yAxisTitle.get() + " "
            
            file = open("GraphingSaved.txt","w")
            file.writelines(data)
            file.close()

        self.parent.destroy()
        showWindow()

    def graphingGUI(self, parent):
        self.parent = parent      #Initial
        setWindow(parent)         #Setting window size and settings
        frame = setFrame(parent)  #Setting frame size and settings
        Pmw.initialise(parent)    #Setting for widgets 

        #Title and information labels
        parent.titleText = tk.Label(frame, text="Polynomial Graphing", font=("Cooper Black", 45))
        parent.graphImage = ImageTk.PhotoImage(Image.open("graphImage.png"))
        parent.graphImageLabel = tk.Label(frame, image = parent.graphImage)
        parent.equationText = tk.Label(frame, text="Y = ax^7 + bx^6 + cx^5 + dx^4 + ex^3 + fx^2 + gx + h", font=("Times New Roman", 26))
        parent.enterEquationText = tk.Label(frame, text="Enter coefficients for above polynomial equation:", font=("Times New Roman", 20))

        #X range text labels
        parent.xLowText = tk.Label(frame, text="X Low:", font=("Times New Roman", 20))
        parent.xHighText = tk.Label(frame, text="X High:", font=("Times New Roman", 20))

        #X range text entries
        parent.xLowEntry = tk.Entry(frame, width=6, fg="crimson", font=("Times New Roman", 20), textvariable=self.xLow)
        parent.xHighEntry = tk.Entry(frame, width=6, fg="crimson", font=("Times New Roman", 20), textvariable=self.xHigh)

        #Graph text labels
        parent.graphTitleText = tk.Label(frame, text="Graph Title:", font=("Times New Roman", 20))
        parent.xAxisTitleText = tk.Label(frame, text="X-axis Title:", font=("Times New Roman", 20))
        parent.yAxisTitleText = tk.Label(frame, text="Y-axis Title:", font=("Times New Roman", 20))

        #Graph text entries
        parent.graphTitleEntry = tk.Entry(frame, width=24, fg="darkred", font=("Times New Roman", 20), textvariable=self.graphTitle)
        parent.xAxisTitleEntry = tk.Entry(frame, width=24, fg="darkred", font=("Times New Roman", 20), textvariable=self.xAxisTitle)
        parent.yAxisTitleEntry = tk.Entry(frame, width=24, fg="darkred", font=("Times New Roman", 20), textvariable=self.yAxisTitle)

        #Buttons for function
        parent.clearButton = tk.Button(frame, text = "Clear", borderwidth=7, overrelief = "groove", bg = "darkred", fg = "mistyrose", font=("Times New Roman", 20), command=self.clear)
        parent.newGraphButton = tk.Button(frame, text = "New Graph", borderwidth=7, overrelief = "groove", fg = "darkred", bg = "mistyrose", font=("Times New Roman", 20), command=self.newGraph)
        parent.addEquationButton = tk.Button(frame, text = "Add Equation", borderwidth=7, overrelief = "groove", fg = "darkred", bg = "mistyrose", font=("Times New Roman", 20), command=self.addEquation)
        parent.importDataButton = tk.Button(frame, text = "Import Data", borderwidth=7, overrelief = "groove", fg = "darkred", bg = "mistyrose", font=("Times New Roman", 20), command=self.importData)
        parent.rootsButton = tk.Button(frame, text = "Compute Roots of Polynomial", borderwidth=7, overrelief = "groove", fg = "darkred", bg = "mistyrose", font=("Times New Roman", 20), command=self.computeRoots)
        parent.helpButton = tk.Button(frame, bitmap = "question", width = 40, height = 60, borderwidth=3, overrelief = "groove", fg = "darkred", bg = "mistyrose", command=self.help)

        #Coefficients text labels
        parent.aText = tk.Label(frame, text="a: ", font=("Times New Roman", 25))
        parent.bText = tk.Label(frame, text="b: ", font=("Times New Roman", 25))
        parent.cText = tk.Label(frame, text="c: ", font=("Times New Roman", 25))
        parent.dText = tk.Label(frame, text="d: ", font=("Times New Roman", 25))
        parent.eText = tk.Label(frame, text="e: ", font=("Times New Roman", 25))
        parent.fText = tk.Label(frame, text="f: ", font=("Times New Roman", 25))
        parent.gText = tk.Label(frame, text="g: ", font=("Times New Roman", 25))
        parent.hText = tk.Label(frame, text="h: ", font=("Times New Roman", 25))

        #Coefficients text entries
        parent.aEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.a)
        parent.bEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.b)
        parent.cEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.c)
        parent.dEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.d)
        parent.eEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.e)
        parent.fEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.f)
        parent.gEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.g)
        parent.hEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 25), textvariable=self.h)

        #Accuracy text labels
        parent.precisionText = tk.Label(frame, text="Precision: ", font=("Times New Roman", 24))

        #Accuracy text entries
        parent.precisionEntry = tk.Entry(frame, width=8, fg="crimson", font=("Times New Roman", 24), textvariable=self.precision)

        #Check buttons
        parent.chkGrid = tk.Checkbutton(frame, text="Grid", font=("Times New Roman", 25), variable=self.gridVal)
        parent.chkDark = tk.Checkbutton(frame, text="Dark Mode", font=("Times New Roman", 25), variable=self.darkVal)

        #Display of all labels, entries, and buttons
        parent.titleText.place(x=175, y=15)
        parent.graphImageLabel.place(x=30, y=115)
        parent.equationText.place(x=50, y=450)
        parent.enterEquationText.place(x=50, y=500)

        parent.aText.place(x=50, y=550)
        parent.aEntry.place(x=100, y=550)

        parent.bText.place(x=50, y=600)
        parent.bEntry.place(x=100, y=600)

        parent.cText.place(x=50, y=650)
        parent.cEntry.place(x=100, y=650)

        parent.dText.place(x=50, y=700)
        parent.dEntry.place(x=100, y=700)

        parent.eText.place(x=350, y=550)
        parent.eEntry.place(x=400, y=550)

        parent.fText.place(x=350, y=600)
        parent.fEntry.place(x=400, y=600)

        parent.gText.place(x=350, y=650)
        parent.gEntry.place(x=400, y=650)

        parent.hText.place(x=350, y=700)
        parent.hEntry.place(x=400, y=700)

        parent.xLowText.place(x=50, y=765)
        parent.xLowEntry.place(x=150, y=765)
        parent.xHighText.place(x=350, y=765)
        parent.xHighEntry.place(x=450, y=765)
        parent.graphTitleText.place(x=50, y=825)
        parent.graphTitleEntry.place(x=200, y=825)

        parent.xAxisTitleText.place(x=50, y=875)
        parent.xAxisTitleEntry.place(x=200, y=875)

        parent.yAxisTitleText.place(x=50, y=925)
        parent.yAxisTitleEntry.place(x=200, y=925)

        parent.clearButton.place(x=800, y=900)
        parent.addEquationButton.place(x=775, y=700)
        parent.newGraphButton.place(x=600, y=700)
        parent.importDataButton.place(x=600, y=900)
        parent.rootsButton.place(x=600, y=800)

        parent.precisionText.place(x=650, y=615)
        parent.precisionEntry.place(x=800, y=615)

        parent.chkGrid.place(x=650, y=550)
        parent.chkDark.place(x=775, y=550)

        parent.helpButton.place(x=910, y=450)

        #Mouse hover over information
        parent.infoText = Pmw.Balloon(parent)
        parent.infoText.bind(parent.newGraphButton, "Graph the function in a new plot")
        parent.infoText.bind(parent.addEquationButton, "Graph the function to an existing plot")
        parent.infoText.bind(parent.importDataButton, "Add coefficients and degrees from a spreadsheet")
        parent.infoText.bind(parent.rootsButton, "Find values of x for which y is equal to zero")
        parent.infoText.bind(parent.clearButton, "Clear all data and reset window")
        parent.infoText.bind(parent.helpButton, "Information for graphing functions")
        parent.infoText.bind(parent.precisionEntry, "Adjust the accuracy for resulting graph")

        #Initial focus set to new graph button
        parent.newGraphButton.focus_set()

    def clear(self):
        answer = tk.messagebox.askquestion ('Matrix Calculator','Are you sure you want to clear all data?',icon = 'warning', parent=self.parent)
        if answer == 'yes':
            self.a.set(0.0)
            self.b.set(0.0)
            self.c.set(0.0)
            self.d.set(0.0)
            self.e.set(0.0)
            self.f.set(0.0)
            self.g.set(0.0)
            self.h.set(0.0)
            self.xLow.set(-10)
            self.xHigh.set(10)
            self.graphTitle.set("")
            self.xAxisTitle.set("")
            self.yAxisTitle.set("")
            self.precision.set(0.001)
            self.gridVal.set(0)
            self.darkVal.set(0)
            self.coefficient = []
            self.degree = []

        # if answer is 'no' then does nothing

    def help(self):
        helpWindow = tk.Tk()
        helpWindow.title("Matrix Calculator")
        ScrollBar = tk.Scrollbar(helpWindow)
        textBox = tk.Text(helpWindow, height=20, width=80, font=("Times New Roman", 16))
        ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        textBox.pack(side=tk.LEFT, fill=tk.Y)
        ScrollBar.config(command=textBox.yview)
        textBox.config(yscrollcommand=ScrollBar.set)
        with open("GraphingInfo.txt", "r", encoding="utf8") as f:
            text = f.read()
        textBox.insert(tk.END, text)

    def importData(self):
        self.coefficient = []
        self.degree = []

        fileName = filedialog.askopenfilename(parent=self.parent, title="Matrix Calculator")

        try:
            excelFile = xlrd.open_workbook(fileName)
            sheet = excelFile.sheet_by_index(0)

            tk.messagebox.showinfo(parent=self.parent, title="Matrix Calculator", message="Import successful!")

            for value in sheet.col_values(0):
                if isinstance(value, float):
                    self.coefficient.append(value)

            for value in sheet.col_values(1):
                if isinstance(value, float):
                    self.degree.append(value)

        except FileNotFoundError:
            pass

        except:
            tk.messagebox.showerror(parent=self.parent, title="Matrix Calculator", message="Unexpected error. Try again!")
            self.importData()
            pass

        if(len(self.coefficient) != len(self.degree)):
            tk.messagebox.showerror(parent=self.parent, title="Matrix Calculator", message="Unbalanced number of coefficients and degrees. Try again!")
            self.importData()

    def calculate(self):
        try:
            xLowVal = int (self.xLow.get())
        except:
            if self.xLow.get() =="":
                tk.messagebox.showwarning(title="Error in 'X Low' entry box", message="Please do not leave the 'X Low' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'X Low' entry box", message="Please enter a number into entry box 'X Low'")

        try:
            xHighVal = int (self.xHigh.get())
        except:
            if self.xHigh.get() =="":
                tk.messagebox.showwarning(title="Error in 'X High' entry box", message="Please do not leave the 'X High' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'X High' entry box", message="Please enter a number into entry box 'X High'")
        try:
            precisiontemp = float(self.precision.get())
        except:
            if self.precision.get() =="":
                tk.messagebox.showwarning(title="Error in 'Precision' entry box", message="Please do not leave the 'Precision' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'Precision' entry box", message="Please enter a number into entry box 'Precision'")

        try:
            aVal = float(self.a.get())
        except:
            if self.a.get() =="":
                tk.messagebox.showwarning(title="Error in 'a' entry box", message="Please do not leave the 'a' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'a' entry box", message="Please enter a number into entry box 'a'")
        try:
            bVal = float (self.b.get())
        except:
            if self.b.get() =="":
                tk.messagebox.showwarning(title="Error in 'b' entry box", message="Please do not leave the 'b' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'b' entry box", message="Please enter a number into entry box 'b'")
        try:
            cVal = float (self.c.get())
        except:
            if self.c.get() =="":
                tk.messagebox.showwarning(title="Error in 'c' entry box", message="Please do not leave the 'c' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'c' entry box", message="Please enter a number into entry box 'c'")
        try:
            dVal = float (self.d.get())
        except:
            if self.d.get() =="":
                tk.messagebox.showwarning(title="Error in 'd' entry box", message="Please do not leave the 'd' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'd' entry box", message="Please enter a number into entry box 'd'")
        try:
            eVal = float (self.e.get())
        except:
            if self.e.get() =="":
                tk.messagebox.showwarning(title="Error in 'e' entry box", message="Please do not leave the 'e' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'e' entry box", message="Please enter a number into entry box 'e'")
        try:
            fVal = float (self.f.get())
        except:
            if self.f.get() =="":
                tk.messagebox.showwarning(title="Error in 'f' entry box", message="Please do not leave the 'f' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'f' entry box", message="Please enter a number into entry box 'f'")
        try:
            gVal = float (self.g.get())
        except:
            if self.g.get() =="":
                tk.messagebox.showwarning(title="Error in 'g' entry box", message="Please do not leave the 'g' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'g' entry box", message="Please enter a number into entry box 'g'")
        try:
            hVal = float (self.h.get())
        except:
            if self.h.get() =="":
                tk.messagebox.showwarning(title="Error in 'h' entry box", message="Please do not leave the 'h' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'h' entry box", message="Please enter a number into entry box 'h'")

        try:
            equation = "Y = "
            if (aVal != 0):
                equation = equation + str (aVal) + "X^7"
            if ((equation != "Y = ") & (bVal < 0)):
                equation = equation + " - " + str (abs(bVal)) + "X^6"
            elif ((equation != "Y = ") & (bVal != 0)):
                equation = equation + " + " + str (bVal) + "X^6"
            elif (bVal != 0):
                equation = equation + str (bVal) + "X^5"
            if ((equation != "Y = ") & (cVal < 0)):
                equation = equation + " - " + str (abs(cVal)) + "X^5"
            elif ((equation != "Y = ") & (cVal != 0)):
                equation = equation + " + " + str (cVal) + "X^5"
            elif (cVal != 0):
                equation = equation + str (cVal) + "X^4"
            if ((equation != "Y = ") & (dVal < 0)):
                equation = equation + " - " + str (abs(dVal)) + "X^4"
            elif ((equation != "Y = ") & (dVal != 0)):
                equation = equation + " + " + str (dVal) + "X^4"
            elif (dVal != 0):
                equation = equation + str (dVal) + "X^4"
            if ((equation != "Y = ") & (eVal < 0)):
                equation = equation + " - " + str (abs(eVal)) + "X^3"
            elif ((equation != "Y = ") & (eVal != 0)):
                equation = equation + " + " + str (eVal) + "X^3"
            elif (eVal != 0):
                equation = equation + str (eVal) + "X^3"
            if ((equation != "Y = ") & (fVal < 0)):
                equation = equation + " - " + str (abs(fVal)) + "X^2"
            elif ((equation != "Y = ") & (fVal != 0)):
                equation = equation + " + " + str (fVal) + "X^2"
            elif (fVal != 0):
                equation = equation + str (fVal) + "X^2"
            if ((equation != "Y = ") & (gVal < 0)):
                equation = equation + " - " + str (abs(gVal)) + "X"
            elif ((equation != "Y = ") & (gVal != 0)):
                equation = equation + " + " + str (gVal) + "X"
            elif (gVal != 0):
                equation = equation + str (gVal) + "X"
            if ((equation != "Y = ") & (hVal < 0)):
                equation = equation + " - " + str (abs(hVal))
            elif ((equation != "Y = ") & (hVal != 0)):
                equation = equation + " + " + str (hVal)
            elif (equation == "Y = "):
                equation = equation + str (hVal)

            x = np.arange(xLowVal, xHighVal, precisiontemp)
            y = ((aVal*(x**7)) + (bVal*(x**6)) + (cVal*(x**5)) +
                 (dVal*(x**4)) + (eVal*(x**3)) + (fVal*(x**2)) +
                 (gVal*x) + hVal)

            return x, y, equation

        except:
            return 0, 0, "Error"

    def newGraph(self):
        self.pltNum = self.pltNum + 1
        self.addEquation()

    def addEquation(self):
        if(len(self.coefficient) == 0 & len(self.degree) == 0):
            x, y, equation = self.calculate()
        else:
            x, y, equation = self.excelEquation()

        if(equation != "Error"):
            # Create the plot
            if(self.darkVal.get() == 1):
                plt.style.use("dark_background")
            else:
                plt.style.use("default")
            plt.figure(self.pltNum)
            plt.title(self.graphTitle.get())
            plt.xlabel(self.xAxisTitle.get())
            plt.ylabel(self.yAxisTitle.get())
            plt.plot(x, y, label=equation)
            if(self.gridVal.get() == 1):
                plt.grid(True)
            else:
                plt.grid(False)
            plt.legend(loc="upper left")
            plt.pause(0.00001)

    def excelEquation(self):
        equation = "F(x)"
        x = np.arange(int (self.xLow.get()), int (self.xHigh.get()), float(self.precision.get()))
        y = 0
        for i in range(len(self.coefficient)):
            y += self.coefficient[i]*x**self.degree[i]
        return x, y, equation

    def computeRoots(self):
        coeff = []

        if(len(self.coefficient) == 0 & len(self.degree) == 0):
            coeff.append(float(self.a.get()))
            coeff.append(float(self.b.get()))
            coeff.append(float(self.c.get()))
            coeff.append(float(self.d.get()))
            coeff.append(float(self.e.get()))
            coeff.append(float(self.f.get()))
            coeff.append(float(self.g.get()))
            coeff.append(float(self.h.get()))
        else:
            coeff = self.coefficient

        result = "Polynomial Roots: ["
        result += ", ".join(map(str, np.around(np.roots(coeff), decimals=5)))
        result += "]"

        generateWindow = tk.Tk()
        generateWindow.title("Matrix Calculator")
        ScrollBar = tk.Scrollbar(generateWindow)
        textBox = tk.Text(generateWindow, height=20, width=80, font=("Times New Roman", 16))
        ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        textBox.pack(side=tk.LEFT, fill=tk.Y)
        ScrollBar.config(command=textBox.yview)
        textBox.config(yscrollcommand=ScrollBar.set)
        textBox.insert(tk.END, result)

class XY_Table:
    def __init__(self, parent):

        #Coefficients input store
        self.a = tk.DoubleVar()
        self.b = tk.DoubleVar()
        self.c = tk.DoubleVar()
        self.d = tk.DoubleVar()
        self.e = tk.DoubleVar()
        self.f = tk.DoubleVar()
        self.g = tk.DoubleVar()
        self.h = tk.DoubleVar()

        #X-Window input store
        self.xLow = tk.IntVar(parent, -10)
        self.xHigh = tk.IntVar(parent, 10)

        #Graph and axis title input store
        self.xColumnTitle = tk.StringVar()
        self.yColumnTitle = tk.StringVar()

        #Call to set table GUI
        self.xyTableGUI(parent)

        #Set initial window
        self.setWindow(parent)
        
        #Call when attempt to close window
        self.parent.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(parent))

    def setWindow(self, parent):
        file = open("XYTableSaved.txt","r")
        lines = file.readlines()
        state = int(float(lines[0]))

        if(state == -1):
            self.a.set(float(lines[1]))
            self.b.set(float(lines[2]))
            self.c.set(float(lines[3]))
            self.d.set(float(lines[4]))
            self.e.set(float(lines[5]))
            self.f.set(float(lines[6]))
            self.g.set(float(lines[7]))
            self.h.set(float(lines[8]))
            self.xLow.set(int(lines[9]))
            self.xHigh.set(int(lines[10]))
            self.xColumnTitle.set(lines[11])
            self.yColumnTitle.set(lines[12])

    def closeWindow(self, parent):
        answer = tk.messagebox.askquestion ("Matrix Calculator", "Do you want to save the data?", icon = "warning")
        if answer == 'yes':
            data = ("-1\n%f\n%f\n%f\n%f\n%f\n%f\n%f\n%f\n" % (float(self.a.get()), float(self.b.get()), float(self.c.get()),
                                                              float(self.d.get()), float(self.e.get()), float(self.f.get()),
                                                              float(self.g.get()), float(self.h.get())))
            data += ("%d\n%d\n" % (int(self.xLow.get()), int(self.xHigh.get())))
            data += self.xColumnTitle.get() + " " + "\n" + self.yColumnTitle.get() + " "
        
            file = open("XYTableSaved.txt","w")
            file.writelines(data)
            file.close()

        self.parent.destroy()
        showWindow()

    """ Creating X-Y table graphics """
    def xyTableGUI(self, parent):
        self.parent = parent      #Initial
        setWindow(parent)         #Setting window size and settings
        frame = setFrame(parent)  #Setting frame size and settings

        #Title and information labels
        parent.titleText = tk.Label(frame, text="X-Y Table", font=("Cooper Black", 45))
        parent.xyImage = ImageTk.PhotoImage(Image.open("xyImage.png"))
        parent.xyImageLabel = tk.Label(frame, image = parent.xyImage)
        parent.equationText = tk.Label(frame, text="Y = ax^7 + bx^6 + cx^5 + dx^4 + ex^3 + fx^2 + gx + h", font=("Times New Roman", 26))
        parent.enterEquationText = tk.Label(frame, text="Enter coefficients for above polynomial equation:", font=("Times New Roman", 20))

        #X range text labels
        parent.xLowText = tk.Label(frame, text="X Low:", font=("Times New Roman", 20))
        parent.xHighText = tk.Label(frame, text="X High:", font=("Times New Roman", 20))

        #X range text entries
        parent.xLowEntry = tk.Entry(frame, width=6, fg="forestgreen", font=("Times New Roman", 20), textvariable=self.xLow)
        parent.xHighEntry = tk.Entry(frame, width=6, fg="forestgreen", font=("Times New Roman", 20), textvariable=self.xHigh)

        #Buttons for function
        parent.clearButton = tk.Button(frame, text = "Clear", overrelief = "groove", borderwidth=8, bg = "darkgreen", fg = "honeydew", font=("Times New Roman", 28), command=self.clear)
        parent.generateButton = tk.Button(frame, text = "Generate", overrelief = "groove", borderwidth=8, bg = "honeydew", fg = "darkgreen", font=("Times New Roman", 28), command=self.generate)
        parent.saveButton = tk.Button(frame, text = "Save", overrelief = "groove", borderwidth=8, bg = "honeydew", fg = "darkgreen", font=("Times New Roman", 28), command=self.save)

        #Table text labels
        parent.xColumnTitleText = tk.Label(frame, text="X Column Title:", font=("Times New Roman", 20))
        parent.yColumnTitleText = tk.Label(frame, text="Y Column Title:", font=("Times New Roman", 20))

        #Graph text entries
        parent.xColumnTitleEntry = tk.Entry(frame, width=20, fg="darkgreen", font=("Times New Roman", 20), textvariable=self.xColumnTitle)
        parent.yColumnTitleEntry = tk.Entry(frame, width=20, fg="darkgreen", font=("Times New Roman", 20), textvariable=self.yColumnTitle)

        #Coefficients text labels
        parent.aText = tk.Label(frame, text="a: ", font=("Times New Roman", 25))
        parent.bText = tk.Label(frame, text="b: ", font=("Times New Roman", 25))
        parent.cText = tk.Label(frame, text="c: ", font=("Times New Roman", 25))
        parent.dText = tk.Label(frame, text="d: ", font=("Times New Roman", 25))
        parent.eText = tk.Label(frame, text="e: ", font=("Times New Roman", 25))
        parent.fText = tk.Label(frame, text="f: ", font=("Times New Roman", 25))
        parent.gText = tk.Label(frame, text="g: ", font=("Times New Roman", 25))
        parent.hText = tk.Label(frame, text="h: ", font=("Times New Roman", 25))

        #Coefficients text entries
        parent.aEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.a)
        parent.bEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.b)
        parent.cEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.c)
        parent.dEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.d)
        parent.eEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.e)
        parent.fEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.f)
        parent.gEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.g)
        parent.hEntry = tk.Entry(frame, width=8, fg="forestgreen", font=("Times New Roman", 25), textvariable=self.h)

        #Display of all labels, entries, and buttons
        parent.titleText.place(x=335, y=15)
        parent.xyImageLabel.place(x=100, y=100)
        parent.equationText.place(x=50, y=475)
        parent.enterEquationText.place(x=50, y=525)

        parent.aText.place(x=50, y=575)
        parent.aEntry.place(x=100, y=575)

        parent.bText.place(x=50, y=625)
        parent.bEntry.place(x=100, y=625)

        parent.cText.place(x=50, y=675)
        parent.cEntry.place(x=100, y=675)

        parent.dText.place(x=50, y=725)
        parent.dEntry.place(x=100, y=725)

        parent.eText.place(x=350, y=575)
        parent.eEntry.place(x=400, y=575)

        parent.fText.place(x=350, y=625)
        parent.fEntry.place(x=400, y=625)

        parent.gText.place(x=350, y=675)
        parent.gEntry.place(x=400, y=675)

        parent.hText.place(x=350, y=725)
        parent.hEntry.place(x=400, y=725)

        parent.xLowText.place(x=50, y=785)
        parent.xLowEntry.place(x=150, y=785)
        parent.xHighText.place(x=350, y=785)
        parent.xHighEntry.place(x=450, y=785)

        parent.xColumnTitleText.place(x=50, y=850)
        parent.xColumnTitleEntry.place(x=250, y=850)

        parent.yColumnTitleText.place(x=50, y=910)
        parent.yColumnTitleEntry.place(x=250, y=910)

        parent.clearButton.place(x=650, y=850)
        parent.saveButton.place(x=650, y=738)
        parent.generateButton.place(x=650, y=625)

        #Initial focus set to coefficient (a)
        parent.aEntry.focus_set()

    def clear(self):
        self.a.set(0.0)
        self.b.set(0.0)
        self.c.set(0.0)
        self.d.set(0.0)
        self.e.set(0.0)
        self.f.set(0.0)
        self.g.set(0.0)
        self.h.set(0.0)
        self.xLow.set(-10)
        self.xHigh.set(10)
        self.xColumnTitle.set("")
        self.yColumnTitle.set("")

    def calculate(self):
        try:
            xLowVal = int (self.xLow.get())
        except:
            if self.xLow.get() =="":
                tk.messagebox.showwarning(title="Error in 'X Low' entry box", message="Please do not leave the 'X Low' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'X Low' entry box", message="Please enter a number into entry box 'X Low'")

        try:
            xHighVal = int (self.xHigh.get())
        except:
            if self.xHigh.get() =="":
                tk.messagebox.showwarning(title="Error in 'X High' entry box", message="Please do not leave the 'X High' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'X High' entry box", message="Please enter a number into entry box 'X High'")

        try:
            aVal = float(self.a.get())
        except:
            if self.a.get() =="":
                tk.messagebox.showwarning(title="Error in 'a' entry box", message="Please do not leave the 'a' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'a' entry box", message="Please enter a number into entry box 'a'")
        try:
            bVal = float (self.b.get())
        except:
            if self.b.get() =="":
                tk.messagebox.showwarning(title="Error in 'b' entry box", message="Please do not leave the 'b' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'b' entry box", message="Please enter a number into entry box 'b'")
        try:
            cVal = float (self.c.get())
        except:
            if self.c.get() =="":
                tk.messagebox.showwarning(title="Error in 'c' entry box", message="Please do not leave the 'c' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'c' entry box", message="Please enter a number into entry box 'c'")
        try:
            dVal = float (self.d.get())
        except:
            if self.d.get() =="":
                tk.messagebox.showwarning(title="Error in 'd' entry box", message="Please do not leave the 'd' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'd' entry box", message="Please enter a number into entry box 'd'")
        try:
            eVal = float (self.e.get())
        except:
            if self.e.get() =="":
                tk.messagebox.showwarning(title="Error in 'e' entry box", message="Please do not leave the 'e' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'e' entry box", message="Please enter a number into entry box 'e'")
        try:
            fVal = float (self.f.get())
        except:
            if self.f.get() =="":
                tk.messagebox.showwarning(title="Error in 'f' entry box", message="Please do not leave the 'f' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'f' entry box", message="Please enter a number into entry box 'f'")
        try:
            gVal = float (self.g.get())
        except:
            if self.g.get() =="":
                tk.messagebox.showwarning(title="Error in 'g' entry box", message="Please do not leave the 'g' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'g' entry box", message="Please enter a number into entry box 'g'")
        try:
            hVal = float (self.h.get())
        except:
            if self.h.get() =="":
                tk.messagebox.showwarning(title="Error in 'h' entry box", message="Please do not leave the 'h' entry box emtpy.")
            else:
                tk.messagebox.showwarning(title="Error in 'h' entry box", message="Please enter a number into entry box 'h'")

        t = PrettyTable()
        x = []
        y = []

        for i in range(xLowVal, xHighVal+1):
            x.append(i)
            y.append((aVal*(i**7)) + (bVal*(i**6)) + (cVal*(i**5)) +
                     (dVal*(i**4)) + (eVal*(i**3)) + (fVal*(i**2)) +
                     (gVal*i) + hVal)

        t.add_column(self.xColumnTitle.get(), x)
        t.add_column(self.yColumnTitle.get(), y)

        return t

    def generate(self):
        table = self.calculate()
        generateWindow = tk.Tk()
        generateWindow.title("Matrix Calculator")
        ScrollBar = tk.Scrollbar(generateWindow)
        textBox = tk.Text(generateWindow, height=20, width=80, font=("Times New Roman", 16))
        ScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        textBox.pack(side=tk.LEFT, fill=tk.Y)
        ScrollBar.config(command=textBox.yview)
        textBox.config(yscrollcommand=ScrollBar.set)
        textBox.insert(tk.END, table)

    def save(self):
        table = self.calculate()
        fileName = filedialog.asksaveasfile(mode = 'w', filetypes = [("Plain Text (*.txt)", "*.txt")], defaultextension = [("Plain Text (*.txt)", "*.txt")])
        table_txt = table.get_string()
        fileName.write(table_txt)
        fileName.close()
        tk.messagebox.showinfo(title="Matrix Calculator", message="Save successful!")

def main():
    main = tk.Tk()
    app = MatrixCalculator(main)
    setWindow(main)
    main.mainloop()

def setFrame(main):
    frame = tk.Frame(main)
    frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(frame)

    vert_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    vert_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    horiz_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, comman=canvas.xview)
    horiz_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    canvas.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    second_frame = tk.Frame(canvas)
    second_frame.configure(width=1000, height=1000)

    canvas.create_window((0,0), window=second_frame, anchor="nw")

    return second_frame

def setWindow(main):
    file = open("windowInfo.txt","r")
    lines = file.readlines()
    
    state = int(float(lines[0]))
    screenHeight = int(float(lines[1]))
    screenWidth = int(float(lines[2]))
    xCenter = int(float(lines[3]))
    yCenter = int(float(lines[4]))
    
    file.close()

    if(state == 0):
        screenWidth = main.winfo_screenwidth()
        screenHeight = main.winfo_screenheight()
        xCenter = screenWidth/2 - 500
        yCenter = screenHeight/2 - 290
        screenWidth = 1000
        screenHeight = 1000
        
    main.title("Matrix Calculator")
    main.geometry("%dx%d+%d+%d" % (screenWidth, screenHeight, xCenter, yCenter))
    main.maxsize(1000, 1000)
    main.iconphoto(False, ImageTk.PhotoImage(Image.open("logo.png")))
    menubar(main)

def menubar(main):
    menubar = tk.Menu(main)
    main.config(menu=menubar)

    #Adding a helptab in menubar
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=helpIndex)
    helpmenu.add_command(label="About...", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    #Adding a settingtab in menubar
    settingsmenu = tk.Menu(menubar, tearoff=0)
    settingsmenu.add_command(label="Save Window", command=lambda: saveWindow(main))
    settingsmenu.add_command(label="Reset Window", command=lambda: resetWindow(main))
    menubar.add_cascade(label="Settings", menu=settingsmenu)

def saveWindow(main):
    windowHeight = main.winfo_height()
    windowWidth = main.winfo_width()
    windowX = main.winfo_x()
    windowY = main.winfo_y()

    data = ("-1\n%d\n%d\n%d\n%d" % (windowHeight, windowWidth, windowX, windowY))

    file = open("windowInfo.txt","w")
    file.writelines(data)
    file.close()

    tk.messagebox.showinfo("Matrix Calculator", "Configuration saved successfully!")

def resetWindow(main):
    file = open("windowInfo.txt","w")
    file.writelines("0\n0\n0\n0\n0")
    file.close()

    tk.messagebox.showinfo("Matrix Calculator", "Configuration has been set to default.")

def about():
    tk.messagebox.showinfo("Matrix Calculator", "© 2020 JOHN M. INGRAM ALL RIGHTS RESERVED")

def helpIndex():
    webbrowser.open('http://athena.ecs.csus.edu/~liuj/matrix.html')

def hideWindow():
    mainWindow.withdraw()

def showWindow():
    mainWindow.deiconify()

if __name__ == "__main__":
    main()
