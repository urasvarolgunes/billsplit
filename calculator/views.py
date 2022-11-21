from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from collections import defaultdict
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class index(View):
    def get(self, request):
        return render(request, "calculator/index.html")

    def post(self, request):
        people = request.POST.getlist('people')
        items = request.POST.getlist('item_name')
        prices = request.POST.getlist('price')
        total_price = request.POST['total_price']
        finals, item_lists = compute_totals(people, items, prices, total_price)

        return render(request, "calculator/result.html", context={'finals': finals, 'item_lists': item_lists})


def compute_totals(people, items, prices, total_price):

    prices = list(map(float, prices))
    before_tax = sum(prices)
    multiplier = float(total_price)/before_tax
    finals = dict()
    item_lists = defaultdict(str)

    for i in range(len(items)):
        people_list = [p.strip() for p in people[i].split(',')]
        num_people = len(people_list)

        if num_people > 1:
            items[i] += f" (between {', '.join(people_list)})"

        for person in people_list:
            finals[person]= finals.get(person, 0) + (prices[i]/num_people)*multiplier
            item_lists[person] += '-{}\n'.format(items[i])

    return finals, item_lists