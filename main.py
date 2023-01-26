from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox
from pytube import YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO

default_folder = 'D:/YTDownloads'
download_list = []
youtube_url = ''
myVideo = ''
yt = ''
base_width = 500


def choose_directory():
    global default_folder
    directory = fd.askdirectory(title="Изменить папку", initialdir=default_folder)
    if directory:
        print(directory)
        folder_path.configure(text='Путь: ' + directory)
        default_folder = directory


def get_data_func():
    global youtube_url
    global myVideo
    global yt
    if "youtube" in link_entry_string.get():
        youtube_url = link_entry_string.get()
        yt = YouTube(youtube_url)
        myVideo = yt.streams.filter(progressive=True).desc()
        if download_list:
            download_list.clear()
            download_listbox.delete(0, END)
            root.update()
            for video in myVideo:
                download_list.append(video)
            for video in download_list:
                download_listbox.insert(END, "Разрешение: " + video.resolution)
            video_name.configure(text='Название: ' + yt.title)
            load_image()

        else:
            for video in myVideo:
                download_list.append(video)
            for video in download_list:
                download_listbox.insert(END, "Разрешение: " + video.resolution)

            video_name.configure(text='Название: ' + yt.title)
            load_image()

    elif link_entry_string.get() and "youtube" not in link_entry_string.get():
        tkinter.messagebox.showerror('Ошибка!', 'Неправильный адрес ссылки.\nПопробуйте еще раз.')
    else:
        tkinter.messagebox.showerror('Ошибка!', 'Поле ввода ссылки пусто.к\nВставьте ссылку и повторите.')


def download_func():
    global youtube_url
    global myVideo
    selected = int(download_listbox.curselection()[0])
    print(type(selected))
    print(selected)
    myVideo[selected].download(output_path=default_folder)


def show_about():
    tkinter.messagebox.showinfo('О программе', '''Программа была разработана с использованием модуля Pytube.
Версия: 0.1beta
Автор программы: Капралов Максим
Почта: maxx@kantavra.com
Сайт: http://kantavra.com
''')


def clipboard_paste():
    x = frame1.clipboard_get()
    message.set(x)


root = Tk()


def load_image():
    label['text'] = 'Загрузка картинки...'
    root.update()
    try:
        response = requests.get(yt.thumbnail_url, timeout=10)
    except requests.exceptions.Timeout:
        label['text'] = 'Timeout error'
    else:
        if response.status_code != 200:
            label['text'] = 'HTTP error ' + str(response.status_code)
        else:
            pil_image = Image.open(BytesIO(response.content))
            wpercent = (base_width / float(pil_image.size[0]))
            hsize = int((float(pil_image.size[1]) * float(wpercent)))
            pil_image = pil_image.resize((base_width, hsize), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(pil_image)

            label.config(image=image, text='')

            # прикрепляем ссылку на изображение к объекту label,
            # чтобы изображение не удалил сборщик мусора
            label.image = image


root.title("YouTube Downloader")
root.resizable(width='false', height='false')
root.minsize(width=515, height=480)
root.maxsize(width=1024, height=768)

frame1 = Frame(root, width=640, height=100, bd=2, relief='ridge')
frame2 = Frame(root, width=640, height=75, bd=2, relief='ridge')
frame3 = Frame(root, width=640, height=75, bd=2, relief='ridge')
frame4 = Frame(root, width=640, height=75, bd=2, relief='ridge')

download_listbox = Listbox(frame2, height=3, width=65, selectmode=SINGLE)

folder_path = Label(frame1, text='Путь: ' + default_folder)

message = StringVar()
link_entry_string = Entry(frame1, width=65, textvariable=message)

insert_button = Button(frame1, text='Вставить', width=15, height=1, command=clipboard_paste)
get_data_button = Button(frame2, text='Получить данные', width=15,
                         height=1, command=get_data_func)
change_path_button = Button(frame1, text='Изменить папку', width=15, height=1,
                            command=choose_directory)
close_button = Button(frame4, text='Выход',
                      command=root.destroy, width=15, height=1)

download_button = Button(frame4, text='Скачать',
                         command=download_func, width=15, height=1)
about_button = Button(frame4, text='О программе',
                      command=show_about, width=15, height=1)

video_name = Label(frame3, bd=3, justify=LEFT, wraplength=450, text='Здесь загрузится информация о видео...', font="arial 16")

label = Label(frame3)
label.grid(row=2, column=0, sticky='we')
frame1.grid(row=0, column=0, sticky='we')
frame2.grid(row=1, column=0, sticky='we')
frame3.grid(row=2, column=0, sticky='we')
frame4.grid(row=3, column=0, sticky='we')

folder_path.grid(row=0, column=1, sticky='nws')
insert_button.grid(row=1, column=0, sticky='nwse')
link_entry_string.grid(row=1, column=1, sticky='nswe')

change_path_button.grid(row=0, column=0, sticky='w')
for i in download_list:
    download_listbox.insert(END, i)
get_data_button.grid(row=0, column=0, sticky='ns', rowspan=2)
download_listbox.grid(row=0, column=1, sticky='nswe')
close_button.grid(row=0, column=2, sticky='e')
about_button.grid(row=0, column=1, sticky='e')
download_button.grid(row=0, column=0)
video_name.grid(row=0, column=0, sticky='w')

root.mainloop()
