def and_items(items):
    if len(items) == 1:
        return str(items[0]) + " "
    elif len(items) == 2:
        return str(items[0]) + " and " + str(items[1]) + " "
    else:
        return ", ".join([str(item) for item in items[:-1]]) + ", and " + str(items[-1]) + " "

def or_items(items):
    if len(items) == 1:
        return str(items[0]) + " "
    elif len(items) == 2:
        return str(items[0]) + " or " + str(items[1]) + " "
    else:
        return ", ".join([str(item) for item in items[:-1]]) + ", or " + str(items[-1]) + " "
