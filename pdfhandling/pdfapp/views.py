from django.shortcuts import render
from django.http import HttpResponse
import PyPDF2
from PyPDF2 import PdfFileReader, PdfReader, PdfWriter

# Create your views here.

def text_extract(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text if text else "No text found in PDF"

def rotate(pdf_file):
    print("Rotated")
    pass

def watermark(pdf_file):
    print("Watermart")
    pass

def details(pdf_file):
    reader = PdfReader(pdf_file) 
    metadata = reader.metadata     
    return str(metadata)

def home(request):
    if request.method == "POST":
        pdf_file = request.FILES.get("pdf_file")
        mode = request.POST.get("mode")
        watermark_text = request.POST.get("watermark_text")

        if not pdf_file:
            return HttpResponse("NO File Uploaded")
        
        elif mode == "extract":
            result = text_extract(pdf_file)
        
        elif mode == "rotate":
            result = rotate(pdf_file)
        
        elif mode == "watermark":
            result = watermark(pdf_file, watermark_text)
        
        elif mode == "details":
            result = details(pdf_file)

        else:
            result = "Invalid Option"

        return HttpResponse(result)

    return render(request, 'home.html')