from pypdf import PdfReader
import sys

def pdfToTxt(reader, outfile):
    for page in reader.pages:
        outfile.write(page.extract_text())
        outfile.write("\n\n\n")

def pdfOCR(filepath, outfile):
    import pytesseract
    from tempfile import TemporaryDirectory
    from pdf2image import convert_from_path
    from PIL import Image

    with TemporaryDirectory() as tempdir:
        pdf_pages = convert_from_path(filepath, 500)
        img_filelist = []

        for enum, page in enumerate(pdf_pages, start=1):
            img_filepath = f"{tempdir}/page_{enum}:03.jpg"
            page.save(img_filepath, "JPEG")
            img_filelist.append(img_filepath)
        
        for img_filepath in img_filelist:
            txt = str(((pytesseract.image_to_string(Image.open(img_filepath)))))
            outfile.write(txt)
            outfile.write("\n\n\n")

def main():
    isocr = False
    if len(sys.argv) == 3:
        if sys.argv[2] == "ocr":
            isocr = True
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else:
        raise RuntimeError("atleast one argument required")

    filename = filepath.split('/')[-1].split('.')[0]

    out_filepath = '/'.join(filepath.split('/')[:-1]) + "/outputs/" + filename + ".txt"
    outfile = open(out_filepath, 'w')

    if outfile: 
        if isocr:
            pdfOCR(filepath, outfile)
        else:
            reader = PdfReader(filepath)
            pdfToTxt(reader, outfile)

if __name__ == "__main__":
    main()
