from tkinter import *
import socket

def clicked():
    HOST = txt1.get()  # The remote host
    PORT = 8899

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




window = Tk()
window.title("PDT to SIC sender")
lbl1 = Label(window, text="SIC IP")
lbl1.grid(column=0, row=0)
txt1 = Entry(window, width=10)
txt1.grid(column=1, row=0)

lbl2 = Label(window, text="Data")
lbl2.grid(column=0, row=1)
txt2 = Entry(window, width=10)
txt2.grid(column=1, row=1)

lbl3 = Label(window, text="1. Cканировать IP адрес на контроллере\r2. Сканировать данные для маркировки")
lbl3.grid(column=0, row=2)

btn = Button(window, text="Send", command=clicked)
btn.grid(column=0, row=3)

lbl4 = Label(window, text="Ответ:")
lbl4.grid(column=0, row=4)

txt1.focus()

window.mainloop()