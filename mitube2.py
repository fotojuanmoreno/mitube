from tkinter import *
from tkinter import filedialog
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


		def d_vid(url):
			try:
				print("Open video")
				#downloadingLabel = Label(underbotons, text = "Downloading:")
				#downloadingLabel.pack()
				youtube = pytube.YouTube(url)
				videotittle = youtube.title
				name = Label(underbotons, text = "Downloading: " + videotittle)
				name.pack()
				video = youtube.streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').desc().first()
				print("Downloading : " + videotittle)
				video.download(save_in)
				print("Download complete")
			except :
				print("Video Eliminado")

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
				name = Label(underbotons, text = videotittle)
				name.pack()
				video = youtube.streams.filter(only_audio=True).first()
				print("Downloading : " + videotittle)
				video.download(save_in)
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
			
				listrep = re.search(r'playlist', str(url))
				if listrep:
					d_list(url)
				else:
					d_vid(url)
				finish = Label(underbotons, text = "Download completed")
				finish.pack()
				elboton1.config(text = "Download", state = NORMAL)
				elboton2.config(text = "Download audio", state = NORMAL)
				video_direction.delete(0, END)
				downloadingLabel.config(text = " ")

			except Exception as e:
				print(e)
				print("Error!")

		def downloadAu(url):
			print("Estamos en audio")
			global save_in
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
		name = Label(body, text = "")
		name.pack()


def main():
	root = Tk()
	aplicacion = App(root)
	root.mainloop()

if __name__ == '__main__':
	main()