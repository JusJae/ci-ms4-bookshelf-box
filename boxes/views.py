from django.shortcuts import render


def view_box(request):
    """ A view that renders the box contents page """

    return render(request, 'boxes/box.html')
