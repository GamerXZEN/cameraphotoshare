import filestack
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time
import webbrowser
import os

Builder.load_file("frontend.kv")

current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())


class CameraScreen(Screen):
	def start(self):
		self.ids.webcamera.play = True
		self.ids.webcamera.opacity = 1
		self.ids.camera_button.text = "Stop Camera"
		self.ids.webcamera.texture = self.ids.webcamera._camera.texture

	def stop(self):
		self.ids.webcamera.play = False
		self.ids.camera_button.text = "Start Camera"
		self.ids.webcamera.texture = None
		self.ids.webcamera.opacity = 0

	def capture(self):
		self.ids.webcamera.export_to_png(f"files/{current_time}.png")
		self.ids.webcamera.play = False
		self.ids.webcamera.texture = None
		self.manager.current = "image_screen"
		self.manager.current_screen.ids.img.source = f"files/{current_time}.png"


class ImageScreen(Screen):
	link_message = "Please create a link first!"

	def update_label(self):
		file_sharer = FileSharer()
		self.ids.link_label.text = file_sharer.upload()

	def copy_url(self):
		try:
			Clipboard.copy(self.ids.link_label.text)
		except:
			self.ids.link_label.text = self.link_message

	def open_url(self):
		try:
			webbrowser.open(self.ids.link_label.text)
		except:
			self.ids.link_label.text = self.link_message



class RootWidget(ScreenManager):
	pass


class MainApp(App):

	def build(self):
		return RootWidget()


class FileSharer:
	def __init__(self, filepath=f"files/{current_time}.png", api_key=os.getenv("FILESTACK_API_KEY")):
		self.filepath = filepath
		self.api_key = api_key

	def upload(self):
		client = filestack.Client(self.api_key)
		new_file = client.upload(filepath=self.filepath)
		return new_file.url


if __name__ == "__main__":
	MainApp().run()
