# Transcriber
Assignment 2 of the course COP290 at IITD

## Audio and Video to Text

Transcribing both audio and video files to text are similar processes. In the case of videos, we first extract the audio and write it into a `.mp3` file and then transcribe the audio.

### SpeechRecognition

There are various ways to transcribe audio files and one of the most popular ones is the python library: SpeechRecognition. It offeres several APIs like google, etc. via which we can parse our audio clips. But this method only makes sense for small clips.
For large audio files, the program will have to make many API calls to completely convert them to text. This causes a huge latency cost (around 5-10 mins for a video 15mins long).

### Vosk

Vosk is a speech recognition toolkit with its key feature being that it works offline and runs smoothly even on very lightweight devices. It also suports transcribing different languages which can be provided as a command line argument.

### Comparison between different models

Vosk offers several models depending on computing power available. The default small one is only 50Mb in size for most languages. While I was not able to test the full size models on my laptop, given below is the performance and accuracy difference between the small and the 
big english-US models.

1. test1.wav:
    - small: Time taken = 1.37s
    > one zero zero zero one nah no to i know zero one eight zero three
    - big: Time taken = 5.55s
    > one zero zero zero one
    > nine oh two one oh
    > zero one eight zero three

We can see that the accuracy of the transcribed text has increased by using a bigger model, but the time taken has also increased.

A similar trend is seen with large videos too. For Transcribing the sample video, the small model takes around 70s whereas the big model takes around 448s with a considerable improvement in accuracy. We can also see the model struggling with identifying Proper Nouns which 
is expected.

## Pdf to Text

### pypdf

The PdfReader class of the pypdf library of python provides a straightforward way to extract textual content from pdfs. There are some issues with this though:

1. The tables in Courses Of Study are not recognised properly - Fundamental issue of how to deal with tables. 
2. Sometimes PDFs do not contain the text as it’s displayed, but instead an image. You notice that when you cannot copy the text. Text extraction fails to give accurate results here.

### Tesseract (OCR)

To read text from pdfs that are scanned the Tesseract library for python can be used. To use this you must first install Tesseract ocr using your systems package manager and also install the data for the languages for which you need to perform text extraction. 
In arch linux the command to do so is:

`pacman -S tesseract tesseract-data-eng`

After this giving an extra commandline parameter "ocr" to the python script will generate images corresponding to each page of the pdf and perform OCR on each of them to generate the output. Shown below is a comparision for "./test\_pdfsnothernLights.pdf" which is a scanned pdf.

- pypdf:
> John Milton: Paradise Lost, Book 
II Pondering his voyage Stood 
on 
the 
brink 
of 
hell 
and 
looked 
a 
while, Into 
this 
wild 
abyss 
the 
wary 
fiend His 
dark 
materials 
to 
create 
more 
worlds, Unless 
the 
almighty 
maker 
them 
ordain Confusedly, 
and 
which 
thus 
must 
ever 
fight, But 
all 
these 
in 
their 
pregnant 
causes 
mixed Of 
neither 
sea, 
nor 
shore, 
nor 
air,, 
nor 
fre, The 
womb 
of 
nature 
and 
perhaps 
her 
grave, Into 
this 
pild 
abyss, 


- Tesseract:
> Into this wild abyss,
> The womb of nature and perhaps her grave,
> Of neither sea, nor shore, nor asr, nor fire,
> But all these in their pregnant causes mixed
> Confusedly, and which thus must ever Sfight,
> Unless the almighty maker them ordain
> His dark materials to create more worlds,
> Into this wild abyss the wary Sfiend |
> Stood on the brink of hell and looked 4 while,
> 
> Pondering his voyage . . .
> 
> John Milton: Paradise Lost, Book II

Shown below are the outputs for `./test_pdfs/ocr_test.pdf`:

- pypdf:
> He llo Wenld 
Test 



- Tesseract:
> HQQQp N endd
OC R Tekt


We find some surprising results here. We can see that pypdf performs better than tesseract in some cases and the reverse is true in other cases.
