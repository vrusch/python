from tkinter import *
from tkinter import filedialog
import os


def getCsvPath():
    inputfile_selected = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("csv", "*.csv")])
    inputfile.set(inputfile_selected)
    checkButtonState()

def getOutputPath():
    parent_dir_selected = filedialog.askdirectory(initialdir=os.getcwd())
    parent_dir.set(parent_dir_selected)
    checkButtonState()

def getProtoPath():
    proto_dir_selected = filedialog.askdirectory(initialdir=os.getcwd())
    proto_dir.set(proto_dir_selected)
    checkButtonState()

def checkButtonState():
    if len(inputfile.get()) > 0 and len(parent_dir.get()) > 0 and len(proto_dir.get()) > 0 and len(a4.curselection()) > 0:
        btnStart.config(state='active')
    else:
        btnStart.config(state='disabled')

def callb(event):
    checkButtonState()
        

def makeScripts():
    scr_num = 100                                      
    op = (a4.get(a4.curselection()))
    operator = op[0]
    operator_code = op[1]
    output_dir = operator + "-channels"

    print(inputfile.get())
    #print(output_dir)
    print(parent_dir.get())
    print(operator)
    print(operator_code)
    print(proto_dir.get())
    print(str(scr_num))
    print(output_dir)


root = Tk()
root.geometry("500x400")
root.title("AMON channel script generator")

inputfile = StringVar()
parent_dir = StringVar()
proto_dir = StringVar()
operator_list = (("TLRS", "3200"), ("O2CZ", "3201"), ("TLHU", "3206"), ("O2SK", "3204"))
operator_var = StringVar(value=operator_list)

label1 = Label(root, text = '  input csv:', font="bold").grid(row=0,sticky=E)
a1 = Entry(root, textvariable = inputfile, width=50).grid(row=0,column=2)
btnFind1 = Button(root, text="Browse CSV", command=getCsvPath).grid(row=0,column=3)

label2 = Label(root, text = 'working dir.:', font="bold").grid(row=1,sticky=E)
a2 = Entry(root, textvariable = parent_dir, width=50).grid(row=1,column=2)
btnFind2 = Button(root, text="Browse", command=getOutputPath).grid(row=1,column=3)

label3 = Label(root, text = 'proto dir.:', font="bold").grid(row=2,sticky=E)
a3 = Entry(root, textvariable = proto_dir, width=50).grid(row=2,column=2)
btnFind3 = Button(root, text="Browse", command=getProtoPath).grid(row=2,column=3)

label4 = Label(root, text = 'for operator.:', font="bold").grid(row=3,sticky=W)
a4 = Listbox(root, listvariable=operator_var, height=4, width=10)
a4.grid(row=3, column=2, sticky=W)

btnStart = Button(root, text="Make", command=makeScripts)
btnStart.grid(row=3,column=3)
a4.bind('<<ListboxSelect>>', callb)
checkButtonState()



root.mainloop()