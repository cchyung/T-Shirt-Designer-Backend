from api import models

QUANTITY_BOUNDARIES = [71, 143, 287, 575, 863]


# calculates price of order based on a number of parameters
def calculate_price(style_id, quantities, ink_colors, addons):
    style = models.Style.objects.get(style_id=style_id)

    quantities_total = sum(quantities)

    # calculate base price
    price = models.StylePrice.objects.get(style=style)
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

    # parse addons and calculate total add on price
    addon_price = 0

    for id in addons:
        addon = models.Addon.objects.get(id)
        addon_price += addon.cost

    total_price_per = base_price + addon_price

    # total price is the sum of the first 5 sizes * price per + (number of 2XL * price per + 1)
    total_price = '%.2f'%sum(quantities[:5]) * total_price_per + quantities[5] * (total_price_per + 1)

    return total_price
