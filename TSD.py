from tkinter import *
import socket

def clicked():
    HOST = txt1.get()  # The remote host
    PORT = 8899

    print('123')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        #translated = bytearray()



        #translated = str(txt2.get()) + b'\r\n'

        s.sendall(txt2.get().encode()+b'\r\n')  # load file to e10
        print(txt2.get().encode()+b'\r\n')
        data = s.recv(1024)
        lbl4['text'] = data
        s.close()

    txt1.delete(0,END)
    txt1.focus()
    txt2.delete(0,END)

def change_focus(event):
    global i
    if i==0:
        txt2.focus()
        i+=1
    else:
        try:
            clicked()
        except:
            lbl4['text'] = "нет связи"
        i=0
        txt1.delete(0 ,'end')
        txt2.delete(0 ,'end')
        txt1.focus()

i = 0

window = Tk()
window.minsize(width=300, height=300)
window.title("PDT to SIC sender")
lbl1 = Label(window, text="SIC IP",font='Arial 20')
lbl1.grid(column=0, row=0)
txt1 = Entry(window, width=50,font='Arial 12')
txt1.grid(column=0, row=1)

lbl2 = Label(window, text="Data",font='Arial 20')
lbl2.grid(column=0, row=2)
txt2 = Entry(window, width=50,font='Arial 12')
txt2.grid(column=0, row=3)

lbl3 = Label(window, text="1. Cканировать IP адрес на контроллере\r2. Сканировать данные для маркировки")
lbl3.grid(column=0, row=4)

btn = Button(window, text="Send", command=clicked, width=20, height=5,font='Arial 20')
btn.grid(column=0, row=5)

lbl4 = Label(window, text="Ответ:")
lbl4.grid(column=0, row=6)

txt1.focus()

window.bind('<Return>', change_focus)


window.mainloop()
