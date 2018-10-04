from django.shortcuts import render
from django.http import HttpResponse
from .models import Image

# Create your views here.
def index(request):
  '''
  View function that renders the index page
  '''
  pictures = Image.get_all_images()
  return render(request, 'index.html',{"pictures":pictures})



# def images(request):
#   '''
#   View function that queries the database and returns images added
#   '''
#   pictures = Image.get_all_images()

#   return render(request,'index.html',{"pictures":pictures})