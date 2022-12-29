from django import template
register = template.Library()


@register.filter(name="isexistincart")
def isexistincart(product, cart):
    key = cart.keys()
    for id in key:
        if int(id) == product.id:
            return True
    return False


@register.filter(name="cartquantity")
def cartquantity(product, cart):
    key = cart.keys()
    for id in key:
        if int(id) == product.id:
            return cart.get(id)
    return False


@register.filter(name="sub_total")
def sub_total(product, cart):
    st = 1
    for i in cart:
        st = product.price * cartquantity(product, cart)

    return st


@register.filter(name="payable_total")
def payable_total(product, cart):
    sum = 0
    for i in product:
        sum = sum+sub_total(i, cart)
    return sum


@register.filter(name="order_sub_total")
def order_sub_total(price, quantity):
    c = price * quantity

    return c
