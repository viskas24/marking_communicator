from tkinter import *
from tkinter import ttk
import socket

def clicked1():
    HOST = txt1.get()  # The remote host
    PORT = 8899

    print('SEND message to IP')

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

def clicked2():
    HOST = txt3.get()  # The remote host
    PORT = 8899

    print('LOAD FILE LIST from IP')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(b'\x02\x00\x35\x4c\x00\x0d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03')  # load file list
        data = s.recv(1024)
        chunk_size = 19
        print(chunk_size)
        chunks = [data[i+4:i + chunk_size+4] for i in range(0, len(data)-7, chunk_size)]

        filenames = ['']
        for x in range(len(chunks)):
            if chunks[x][12]== 2:
                filenames.append(chunks[x][0:11])

                #print(chunks[x][0:11],chunks[x][13:15])
                #lbl5['text'] += chunks[x][0:11].decode()

        #lbl5['text'] = filenames

        s.close()


    lbl6['text'] = "Выбрать файл, сканировать целевой IP, нажать кнопку SEND"
    txt4['state'] = "normal"
    btn3['state'] = "normal"
    combobox['values'] = filenames

    #txt3.delete(0,END)
    txt4.focus()

def clicked3():
    HOST = txt3.get()  # The remote host
    PORT = 8899

#    global selected_file

    print('LOAD FILE from IP ' + HOST)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        filename = combobox.get().encode()
        print(filename)
        print(filename[0:11])

        s.sendall(b'\x02\x00\x35\x53\x00\x0d' + filename[0:11] + b'\x00\x02\x03')  # load file to e10
        data = s.recv(1024)
        print(data)
        line = data[17:]
        print(line)
        print(len(line) + 13)
        print(hex(len(line) + 13))

        num = len(line) + 13
        len_bytes = num.to_bytes(2, byteorder='big')
        print(len_bytes)

        s.close()

    HOST = txt4.get()  # The remote host
    PORT = 8899

    print('LOAD FILE to IP ' + HOST)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(b'\x02\x00\x35\x47' + len_bytes + filename[0:11] + b'\x00\x02' + line + b'\x03')  # load file to e10
        #s.sendall(b'GETVERSION\r\n')
        data = s.recv(1024)
        print(data)
        #s.sendall(b'\x02\x00\x35\x47\x00\xa3' + filename + b'\x00\x02' + line + b'\x03')  # load file to e10
        #data = s.recv(1024)


        s.close()

    txt4.delete(0,END)
    txt4.focus()

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

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Отправка Команд")
tab_control.add(tab2, text="Копирование файлов")

#первая вкладка по отправке команд
lbl1 = Label(tab1, text="SIC IP",font='Arial 20')
lbl1.grid(column=0, row=0)
txt1 = Entry(tab1, width=50,font='Arial 12')
txt1.grid(column=0, row=1)

lbl2 = Label(tab1, text="Data",font='Arial 20')
lbl2.grid(column=0, row=2)
txt2 = Entry(tab1, width=50,font='Arial 12')
txt2.grid(column=0, row=3)

lbl3 = Label(tab1, text="1. Cканировать IP адрес на контроллере\r2. Сканировать данные для маркировки")
lbl3.grid(column=0, row=4)

btn1 = Button(tab1, text="Send", command=clicked1, width=20, height=5,font='Arial 20')
btn1.grid(column=0, row=5)

lbl4 = Label(tab1, text="Список файлов:")
lbl4.grid(column=0, row=6)

txt1.focus()

#вторая вкладка по копированию файлов
lbl5 = Label(tab2, text="SIC IP",font='Arial 20')
lbl5.grid(column=0, row=0)
txt3 = Entry(tab2, width=50,font='Arial 12')
txt3.grid(column=0, row=1)

btn2 = Button(tab2, text="Load File List", command=clicked2, width=20, height=2,font='Arial 20')
btn2.grid(column=0, row=5)

lbl5 = Label(tab2, text="Список файлов:")
lbl5.grid(column=0, row=6)

selected_file = ''
combobox = ttk.Combobox(tab2, textvariable=selected_file, values='')
combobox.grid(column=0, row=7)
lbl6 = Label(tab2, text="Cканировать IP, нажать кнопку LOAD FILE LIST")
lbl6.grid(column=0, row=8)
txt4 = Entry(tab2, width=50, font='Arial 12', state=["disabled"])
txt4.grid(column=0, row=9)
btn3 = Button(tab2, text="Send", command=clicked3, width=20, height=2, font='Arial 20', state=["disabled"])
btn3.grid(column=0, row=10)

window.bind('<Return>', change_focus)
tab_control.pack(expand=1, fill="both")

window.mainloop()
