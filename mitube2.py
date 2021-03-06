from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pytube
from pytube import Playlist
from pytube import exceptions
from pydub import AudioSegment
import pydub
import os

class App():
	
	def __init__(self, root):

		self.master = root
		self.master.config(padx = 50, pady = 50)
		self.master.title("MiTube - Youtube downloader")

		body = Frame(self.master)
		body.pack()
		botons = Frame(self.master)
		botons.pack()
		underbotons = Frame(self.master)
		underbotons.pack()
		listspace = Frame(self.master)
		listspace.pack()

		def replace_all(text, dic):
		    for i, j in dic.items():
		        text = text.replace(i, j)
		    return text

		def to_mp3(save_in, videotittle):
			clean_link = {".": "","'":"", "|":"", "*":"", ",":"", "/":"", '"':'', " / ":" ", ":":""}
			track_name = replace_all(videotittle, clean_link)
			ruta = str(save_in + "/" + track_name + ".mp4")
			#print(ruta)
			pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
			sound = AudioSegment.from_file(ruta)
			sound.export(save_in + "/" + videotittle + ".mp3", format="mp3")
			os.remove(ruta)
			print("Download complete")


		def d_vid(url):
			global count
			try:
				print("scanning video")
				youtube = pytube.YouTube(url)
				videotittle = youtube.title
				count = count+1
				name['text'] = "Downloading: " + videotittle
				video = youtube.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc().first()
				print("Downloading : " + videotittle)
				video.download(save_in)
				lalista.insert(folder1, 1, text = count, values=(videotittle, "Complete"))
				print("Download complete")
			except :
				print("Video Eliminado")
				lalista.insert(folder1, "end", "", text = count, values=(videotittle, "Error"))

		def d_list(url):
			print("Estamos en una lista")
			playlist = Playlist(url)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
			print(playlist)
			print('Number of videos in playlist: ' + str(len(playlist.video_urls)))
			for video in playlist:
				d_vid(video)

		def d_audio_vid(url):
			global count
			videotittle = ""
			try:
				count = count+1
				print("Open video")
				downloadingLabel['text'] = "Downloading:"
				youtube = pytube.YouTube(url)
				videotittle = youtube.title
				name['text'] = videotittle
				video = youtube.streams.filter(only_audio=True).first()
				print("Downloading : " + videotittle)
				print(save_in)
				video.download(save_in)
				try:
					to_mp3(save_in, videotittle)
					lalista.insert(folder1, "end", "", text = count, values=(videotittle, "Complete"))
				except:
					print("Can't converted to mp3")
					lalista.insert(folder1, "end", "", text = count, values=(videotittle, "Error in mp3 export"))
			except :
				print("Video Eliminado")
				lalista.insert(folder1, "end", "", text = count, values=(videotittle, "Error"))



		def d_audio_list(url):
			print("Estamos en una lista")
			playlist = Playlist(url)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
			print(playlist)
			print('Number of audios in playlist: %s' % len(playlist.video_urls))
			for video in playlist:
				print()
				print("#########################################################################")
				d_audio_vid(video)
				print("#########################################################################")
				print()


		def downloadVid(url):
			print("---------------")
			print("STARTING MITUBE")
			print("---------------")
			print()
			global save_in
			global count
			downloadingLabel['text'] = " "
			try:
				print("Coge el link")
				url = video_direction.get()
				if url == "":
					print("No link disponible")
					return
				elboton1.config(text = "Please wait...")
				elboton1.config(state = DISABLED)
				elboton2.config(text = "Please wait...")
				elboton2.config(state = DISABLED)
				downloadingLabel['text'] = " - Downloading - "
				print("select place to save")
				path_to_save_video = filedialog.askdirectory()
				save_in = path_to_save_video
				count = 0
				listrep = re.search(r'playlist', str(url))
				if listrep:
					d_list(url)
				else:
					d_vid(url)
				print("Donload finished")
				finish = Label(underbotons, text = "Download completed")
				finish.pack()
				elboton1.config(text = "Download", state = NORMAL)
				elboton2.config(text = "Download audio", state = NORMAL)
				video_direction.delete(0, END)
				downloadingLabel['text'] = " "
				path_to_save_video = ""
				count = 0
			except Exception as e:
				print(e)
				print("Error!")
				elboton1.config(text = "Download", state = NORMAL)
				elboton2.config(text = "Download audio", state = NORMAL)
				video_direction.delete(0, END)
				downloadingLabel['text'] = " "
				count = 0

		def downloadAu(url):
			print("Estamos en audio")
			global save_in
			global count
			downloadingLabel['text'] = " "
			try:
				print("Coge el link")
				url = video_direction.get()
				if url == "":
					print("No link disponible")
					return
				elboton1.config(text = "Please wait...")
				elboton1.config(state = DISABLED)
				elboton2.config(text = "Please wait...")
				elboton2.config(state = DISABLED)
				downloadingLabel['text'] = " - Downloading - "
				print("select place to save")
				path_to_save_video = filedialog.askdirectory()
				save_in = path_to_save_video
				count = 0
				listrep = re.search(r'playlist', str(url))
				if listrep:
					d_audio_list(url)
				else:
					d_audio_vid(url)
				finish = Label(underbotons, text = "Download completed")
				finish.pack()
				elboton1.config(text = "Download", state = NORMAL)
				elboton2.config(text = "Download audio", state = NORMAL)
				video_direction.delete(0, END)
				downloadingLabel['text'] = " "
				path_to_save_video = ""
				count = 0

			except Exception as e:
				print(e)
				print("Error!")
				elboton1.config(text = "Download", state = NORMAL)
				elboton2.config(text = "Download audio", state = NORMAL)
				video_direction.delete(0, END)
				downloadingLabel['text'] = " "
				count = 0


		#----- BODY -----

		welomeLabel = Label(body, text = "Welcome to MiTube", font = ("verdana", 20))
		welomeLabel.pack()

		messageLabel = Label(body, text = "\nWith This simple application you will can download videos from YouTube")
		messageLabel.pack()

		instruction1 = Label(body, text = "\nPlease, enter the link to the video you want download:\n")
		instruction1.pack()

		video_direction = Entry(body)
		video_direction.config(width = 50)
		video_direction.pack()
		video_direction.focus()

		elboton1 = Button(botons, text = "Download", font = ("verdana",15), pady = 20, relief = 'ridge', command = lambda:downloadVid(video_direction.get()))
		elboton1.pack(side = LEFT)
		elboton2 = Button(botons, text = "Download audio", font = ("verdana",15), pady = 20, relief = 'ridge', command = lambda:downloadAu(video_direction.get()))
		elboton2.pack(side = RIGHT)

		downloadingLabel = Label(underbotons, text = " ")
		downloadingLabel.pack()

		name = Label(underbotons, text = " ")
		name.pack()

		lalista = ttk.Treeview(listspace)
		lalista['columns']=("name", "Download")
		lalista.pack()
		lalista.column("#0", width=50, minwidth=50)
		lalista.column("name", width=450, minwidth=150)
		lalista.column("Download", width=100, minwidth=20)

		folder1 = lalista.insert("", 0, "", text="ID", values=("File name","Download",""))



def main():
	root = Tk()
	aplicacion = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()