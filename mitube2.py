from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pytube
from pytube import Playlist
from pytube import exceptions
import time


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


		def d_vid(url):
			global count
			try:
				print("Open video")
				#downloadingLabel = Label(underbotons, text = "Downloading:")
				#downloadingLabel.pack()
				youtube = pytube.YouTube(url)
				videotittle = youtube.title
				count = count+1
				name['text'] = "Downloading: " + videotittle
				video = youtube.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc().first()
				print("Downloading : " + videotittle)
				video.download(save_in)
				lalista.insert("", 1, "", text = count, values=(videotittle, "Complete"))
				print("Download complete")
			except :
				print("Video Eliminado")
				lalista.insert("", 1, "", text = count, values=(videotittle, "Error"))

		def d_list(url):
			print("Estamos en una lista")
			playlist = Playlist(url)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
			print(playlist)
			print('Number of videos in playlist: ' + str(len(playlist.video_urls)))
			for video in playlist:
				d_vid(video)

		def d_audio_vid(url):
			try:
				print("Open video")
				downloadingLabel = Label(underbotons, text = "Downloading:")
				downloadingLabel.pack()
				youtube = pytube.YouTube(url)
				videotittle = youtube.title
				count = count+1
				name = Label(underbotons, text = videotittle)
				name.pack()
				video = youtube.streams.filter(only_audio=True).first()
				print("Downloading : " + videotittle)
				video.download(save_in)
				# lalista.insert(folder1, "end", "", text = count, values=(videotittle, "OK"))
				print("Download complete")
			except :
				print("Video Eliminado")

		def d_audio_list(url):
			print("Estamos en una lista")
			playlist = Playlist(url)
			playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
			print(playlist)
			print('Number of audios in playlist: %s' % len(playlist.video_urls))
			# videotittle = playlist.title
			# name = Label(underbotons, text = videotittle)
			# name.pack()
			for video in playlist:
				d_audio_vid(video)

		def downloadVid(url):
			global save_in
			global count
			downloadingLabel['text'] = " "
			elboton1.config(text = "Please wait...")
			elboton1.config(state = DISABLED)
			elboton2.config(text = "Please wait...")
			elboton2.config(state = DISABLED)
			downloadingLabel['text'] = " - Downloading - "
			

			try:
				print("Coge el link")
				url = video_direction.get()
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
				count = 0
			except Exception as e:
				print(e)
				print("Error!")

		def downloadAu(url):
			print("Estamos en audio")
			global save_in
			global count
			downloadingLabel = Label(body, text = " ")
			downloadingLabel.pack()
			elboton1.config(text = "Please wait...")
			elboton1.config(state = DISABLED)
			elboton2.config(text = "Please wait...")
			elboton2.config(state = DISABLED)
			downloadingLabel.config(text = "- Downloading - ")

			try:
				print("Coge el link")
				url = video_direction.get()
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
				downloadingLabel = Label(underbotons, text = " ")
				count = 0

			except Exception as e:
				print(e)
				print("Error!")


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
		# lalista.heading("#0",text="ID")
		# lalista.heading("name", text="Name")
		# lalista.heading("Download", text="Download")
		# Level 1
		folder1=lalista.insert("", 1, "", text="ID", values=("File name","Download",""))
		# Level 2
		# lalista.insert(folder1, "end", "", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
		# lalista.insert(folder1, "end", "", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
		# lalista.insert(folder1, "end", "", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))


def main():
	root = Tk()
	aplicacion = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()