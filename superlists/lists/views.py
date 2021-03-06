from lists.models import Item
from django.shortcuts import redirect, render


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
        
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
