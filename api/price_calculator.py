from api import models

QUANTITY_BOUNDARIES = [71, 143, 287, 575, 863]


# calculates price of order based on a number of parameters
def calculate_price(style_id, quantities, ink_colors, addons):
    # style
    # quantity
    # ink colors
    # addons

    # separate comma separated quantities into array
    # order is XS, S, M, L, XL, 2XL
    quantities_list = quantities.split(',')
    quantities_total = sum(quantities_list)

    # calculate base price
    price = models.StylePrice.objects.get(style=style_id)
    base_price = 0

    if quantities_total < QUANTITY_BOUNDARIES[0]:
        base_price = price.price1
    elif quantities_total < QUANTITY_BOUNDARIES[1]:
        base_price = price.price2
    elif quantities_total < QUANTITY_BOUNDARIES[2]:
        base_price = price.price3
    elif quantities_total < QUANTITY_BOUNDARIES[3]:
        base_price = price.price4
    else:
        base_price = price.price5

    # TODO: Figure out how ink colors fit in to the equation

    addon_ids = addons.split(',')
    addon_list = []
    addon_price = 0

    for id in addon_ids:
        addon = models.Addon.objects.get(id)
        addon_list.append(addon)
        addon_price += addon.cost

    total_price_per = base_price + addon_price

    # total price is the sum of the first 5 sizes * price per + number of 2XL * total price + 1
    total_price = sum(quantities_list[:5]) * total_price_per + quantities_list[5] * (total_price_per + 1.0)

    return total_price
