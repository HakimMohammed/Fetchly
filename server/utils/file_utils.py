import os
import uuid

DOWNLOADS_DIR = "downloads"

class FileManager:
	def __init__(self, downloads_dir=DOWNLOADS_DIR):
		self.downloads_dir = downloads_dir
		if not os.path.exists(self.downloads_dir):
			os.makedirs(self.downloads_dir)

	def create_temp_file(self, prefix: str, extension: str) -> str:
		filename = f"{prefix}_{uuid.uuid4().hex}{extension}"
		return os.path.join(self.downloads_dir, filename)