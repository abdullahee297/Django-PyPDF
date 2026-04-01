from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def text_extract(filename):
    print("Extrated")
    pass

def rotate(filename):
    print("Rotated")
    pass

def watermark(filename):
    print("Watermart")
    pass

def details(filename):
    print("Details")
    pass


def home(request):
    if request.method == "POST":
        pdf_file = request.FILES.get("pdf_file")
        mode = request.POST.get("mode")

        if not pdf_file:
            return HttpResponse("NO File Uploaded")
        
        elif mode == "extract":
            result = text_extract(pdf_file)
        
        elif mode == "rotate":
            result = rotate(pdf_file)
        
        elif mode == "watermark":
            result = watermark(pdf_file)
        
        elif mode == "details":
            result = details(pdf_file)

        else:
            result = "Invalid Option"

        return HttpResponse(result)

    return render(request, 'home.html')