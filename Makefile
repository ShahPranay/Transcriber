audio:
	python3 transcribe_audio.py $(lang) $(filepath) $(model_name)

video:
	python3 transcribe_video.py $(lang) $(filepath) $(model_name)
