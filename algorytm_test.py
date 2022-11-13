price_alerts = [5, 10, 15]
given_sequence = [4, 5, 7, 11, 13, 9, 4, 17]


def trend(start_price, end_price):
    if start_price > end_price:
        return decrease_alert(end_price) #return min value of notification
    elif start_price < end_price:
        return increase_alert(end_price) #return max value of notification
    else:
        return [] #if start_price == end_price


def increase_alert(end_price):
    notification = []
    for price in price_alerts:
        if end_price >= price:
            notification.append(price)
        else:
            continue
    return notification


def decrease_alert(end_price):
    notification = []
    for price in reversed(price_alerts):
        if end_price <= price:
            notification.append(price)
        else:
            continue
    return notification


print(trend(17, 4))
