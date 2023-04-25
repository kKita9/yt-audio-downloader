from tkinter import *
from tkinter import messagebox
from pytube import YouTube, Playlist
import os


# tworzenie obiektu YouTube lub PlayList
def stworz_obiekt():
    # pobranie linku
    link = entr_link.get()

    # tworzenie obiektu
    if var_ilosc.get() == "film":
        yt = YouTube(link)
    else:
        yt = Playlist(link)

    return yt


# funkcja zmienajaca format z MP4 na MP3
def zmien_format(plik):
    nazwa, rozsz = os.path.splitext(plik)
    nowy = nazwa + ".mp3"
    os.rename(plik, nowy)


# funkcja pobierajaca plik lub playliste
def pobierz():
    # tworzenie obiektu
    yt = stworz_obiekt()

    # pobieranie
    if isinstance(yt, YouTube):
        plik = yt.streams.filter(only_audio=True).first().download("pobrane")
        zmien_format(plik)
    else:
        for wideo in yt.videos:
            plik = wideo.streams.filter(only_audio=True).first().download("pobrane")
            zmien_format(plik)

    # okno informujace o zakonczeniu pobierania
    messagebox.showinfo("Stan pobierania", "Pobieranie zakonczone!")

# metoda sluzaca do usuwania obecnego linku oraz wklejania skopiowanego linku do pola entr_link
def wyczysc_i_wklej():
    entr_link.delete(0, END)
    entr_link.event_generate("<<Paste>>")


# tworzenie okna
okno = Tk()
okno.title("Music downloader")
okno.geometry("700x250")

# etykieta startowa
lbl_start = Label(okno, text="YouTube downloader", width=500, height=2, font=('Times New Roman', 20, 'bold'))
lbl_start.pack()

# wklejanie linku
frm_link = Frame(okno, pady=10, padx=20)
frm_link.pack(anchor=W)

lbl_link = Label(frm_link, text="Link: ", font=('Times', 15))
lbl_link.pack(side=LEFT)

entr_link = Entry(frm_link, bd=5, width=50, font=('Times', 15, 'italic'))
entr_link.pack(side=LEFT)

btn_wklej = Button(frm_link,
                   text='Wklej',
                   width=9,
                   font=('Times', 12, 'bold'),
                   background='#808080',
                   command=wyczysc_i_wklej)
btn_wklej.pack(side=LEFT)

# wybor pobierania (jeden plik czy playlista)
frm_ilosc = Frame(okno, pady=10, padx=20)
frm_ilosc.pack(anchor=W)

lbl_ilosc = Label(frm_ilosc, text="Pobierz: ", font=('Times', 15), width=10)
lbl_ilosc.pack(side=LEFT)

var_ilosc = StringVar()
var_ilosc.set('film')

rdb_film = Radiobutton(frm_ilosc, text="film", variable=var_ilosc, value="film", font=('Times', 15))
rdb_film.pack(side=LEFT)

rdb_playlist = Radiobutton(frm_ilosc, text="playliste", variable=var_ilosc, value="playlist", font=('Times', 15))
rdb_playlist.pack(side=LEFT)

# pobierz
pobierz = Button(okno, text="POBIERZ", font=('Times New Roman', 15, 'bold'), bd=5, command=pobierz)
pobierz.pack()

okno.mainloop()

