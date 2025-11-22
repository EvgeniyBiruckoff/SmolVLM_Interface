import torch
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
from io import BytesIO
from urllib.parse import urlparse
import os
class Model:
	def __init__(self):
		device = str(os.environ.get('DEVICE'))
		nn_ver = str(os.environ.get('NN_VER'))
		self.DEVICE = device if torch.cuda.is_available() else "cpu"
		self.processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-"+nn_ver+"-Instruct")
		self.model = AutoModelForVision2Seq.from_pretrained("HuggingFaceTB/SmolVLM-"+nn_ver+"-Instruct")
		self.model.to(self.DEVICE)
		self.image = None

	def get_any_answer(self, promt):
		messages = [
		{
		"role": "user",
		"content": [
		    {"type": "image", "image": self.image},
		    {"type": "text", "text": promt}
		]
		},
		]
		inputs = self.processor.apply_chat_template(
		    messages,
		    add_generation_prompt=True,
		    tokenize=True,
		    return_dict=True,
		    return_tensors="pt",
		).to(self.DEVICE)

		outputs = self.model.generate(**inputs, max_new_tokens=40)
		response = str(self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
		clean_output = response.replace("<end_of_utterance>", "").strip()
		return clean_output

	def get_what_answer(self):
		messages = [
		{
		"role": "user",
		"content": [
		    {"type": "image", "image": self.image},
		    {"type": "text", "text": "Whats that?"}
		]
		},
		]
		inputs = self.processor.apply_chat_template(
		    messages,
		    add_generation_prompt=True,
		    tokenize=True,
		    return_dict=True,
		    return_tensors="pt",
		).to(self.DEVICE)

		outputs = self.model.generate(**inputs, max_new_tokens=40)
		response = str(self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
		clean_output = response.replace("<end_of_utterance>", "").strip()
		return clean_output

	def set_image(self, link):
		headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
		}

		try:
			parsed = urlparse(link)
			is_url = all([parsed.scheme, parsed.netloc])
		except:
			is_url = False

		if is_url:
			try:
			    response = requests.get(link, headers=headers, timeout=30)
			    response.raise_for_status()
			    self.image = Image.open(BytesIO(response.content))
			except Exception as e:
			    raise ValueError(f"Ошибка загрузки изображения по URL: {e}")
		else:
			try:
				if not os.path.exists(link):
					raise FileNotFoundError(f"Файл не найден: {link}")
			    
				if not os.path.isfile(link):
					raise ValueError(f"Указанный путь ведет к директории, а не к файлу: {link}")
			
				self.image = Image.open(link)
			    
			except Exception as e:
			    raise ValueError(f"Ошибка загрузки изображения с локального диска: {e}")

		# Проверяем, что изображение успешно загружено
		if self.image is None:
			raise ValueError("Не удалось загрузить изображение")
		
