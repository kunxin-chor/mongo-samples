def add_two(x, y):
    total = x + y
    return total
    
def subtract_from(x, y):
    result = x - y
    return result
    
def calculate_gst(price, gst):
    if price < 0:
        return 0
    return round(gst * price, 2)