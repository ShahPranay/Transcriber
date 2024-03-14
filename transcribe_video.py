import sys
import time
from transcribe_audio import transcribeAudio
from moviepy.editor import VideoFileClip

def main():
    model_name = None
    if len(sys.argv) == 4:
        video_language = sys.argv[1]
        video_filepath = sys.argv[2]
        model_name = sys.argv[3]
    if len(sys.argv) == 3:
        video_language = sys.argv[1]
        video_filepath = sys.argv[2]
    elif len(sys.argv) == 2:
        video_language = "en-us"
        video_filepath = sys.argv[1]
    else:
        raise RuntimeError("Atleast one argument is required")

    start_time = time.process_time()

    video = VideoFileClip(video_filepath)
    audio = video.audio
    if audio:
        video_filename = video_filepath.split('/')[-1]
        while(video_filename[-1] != '.'):
            video_filename = video_filename[:-1]

        audio_filepath = "/".join(video_filepath.split("/")[:-1]) + "/audiofiles/" + video_filename + "mp3"
        audio.write_audiofile(audio_filepath)

        out_filepath = "/".join(video_filepath.split("/")[:-1]) + "/outputs/" + video_filename + "txt"

        transcribeAudio(audio_filepath, out_filepath, video_language, model_name)
        print("Time taken to transcribe video: ", time.process_time() - start_time)
    else:
        print("error in reading video file")

if __name__ == "__main__":
    main()
