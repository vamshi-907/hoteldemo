from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')


def faq(request):
    return render(request,'faq.html')

def terms(request):
    return render(request,'terms.html')

def privacy(request):
    return render(request,'privacy.html')
