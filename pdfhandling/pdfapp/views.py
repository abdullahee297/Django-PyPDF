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

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

def watermark(pdf_file, watermark_text):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        packet = BytesIO()
        can = canvas.Canvas(packet)
        can.setFont("Helvetica", 40)
        can.setFillAlpha(0.2)   #transparency
        can.drawString(150, 300, watermark_text)
        can.save() 
        packet.seek(0)

        watermark_pdf = PdfReader(packet)
        watermark_page = watermark_pdf.pages[0]

        page.merge_page(watermark_page)
        writer.add_page(page)
    
    output_stream = BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    return output_stream

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
            if not watermark_text:
                return HttpResponse("Please enter watermark text")

            output_pdf = watermark(pdf_file, watermark_text)

            response = HttpResponse(output_pdf, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="watermarked.pdf"'

            return response

        elif mode == "details":
            result = details(pdf_file)

        else:
            result = "Invalid Option"

        return HttpResponse(result)

    return render(request, 'home.html')