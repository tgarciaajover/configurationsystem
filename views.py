from django.shortcuts import render

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':0,'num_instances':0,'num_instances_available':0,'num_authors':0},
    )
