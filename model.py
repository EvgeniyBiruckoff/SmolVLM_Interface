import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
import os
class Model:
	def __init__(self):
		device = str(os.environ.get('DEVICE'))
		nn_ver = str(os.environ.get('NN_VER'))
		self.DEVICE = device if torch.cuda.is_available() else "cpu"
		self.processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-"+nn_ver+"-Instruct")
		self.model = AutoModelForVision2Seq.from_pretrained("HuggingFaceTB/SmolVLM-"+nn_ver+"-Instruct")
		self.model.to(self.DEVICE)

	def get_any_answer(self, promt, link):
		messages = [
		{
		"role": "user",
		"content": [
		    {"type": "image", "url": link},
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

	def get_what_answer(self, link):
		messages = [
		{
		"role": "user",
		"content": [
		    {"type": "image", "url": link},
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
