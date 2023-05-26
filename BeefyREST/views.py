import random

from django.shortcuts import render

# Create your views here.
def index(request):
    quotes = [
        "Beef. Yes. Roast beef. It's the Swedish term for beef that is roasted",
        "Not eating meat is a decision. Eating meat is an instinct.",
        "Live life. Eat meat.",
        "No Vegans, just eat meat",
        "Meat is my therapy.",
        "You can't buy happiness, but you can buy meat and that's basically the same thing.",
        "Heaven sends us good meat, but the Devil sends us cooks.",
        "First we eat meat, then we do everything else.",
        "Becoming a vegetarian is just a big mis-steak.",
        "You had me at meat tornado."
    ]
    contexs = {
        'quote': random.choice(quotes)
    }
    return render(request=request, template_name='index.html', context=contexs)