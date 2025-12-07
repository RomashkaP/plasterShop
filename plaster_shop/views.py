from django.shortcuts import render, redirect

def main_page_view(request):
    return render(request, 'main_page.html')