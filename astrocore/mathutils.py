
    
def fix(v, prec):
    """
    Round the provided value to the specified precision.

    :param v:       the value to fix
    :param prec:    the precision to fix the value to (number of digits after the decimal)
    :return:        the fixed value
    """
    v = to_float(v, None)
    if (v is not None) and (prec >= 0):
        sf = pow(10.0, prec)
        v = int((float(v) * sf) + 0.5)
        v = float(v) / sf
    return v
    
def make_float_readable(s):
    """
    Make a float into a readable string.
    
    :param s:   the value to make readable
    :return:    the formatted value
    """
    if not type(s) is float:
        d = float(s)
    else:
        d = s
    return "{:,.4f}".format(d)

def make_int_readable(s):
    """
    Make an integer into a readable string.
    
    :param s:   the value to make readable
    :return:    the formatted value
    """
    if not type(s) is int:
        d = int(s)
    else:
        d = s
    return "{:,d}".format(d)

def normalize_float(f, min_f, max_f):
    diff_f = max_f - min_f
    while f >= max_f:
        f -= diff_f
    while f < min_f:
        f += diff_f
    return f

def normalize_degrees(dgs, min_d=0, max_d=360):
    """
    Normalize a value (in degrees).
    
    :param dgs:    the value to normalize
    :param min_d:  the minimum value (defaults to 0)
    :param max_d:  the maximum value (defaults to 360)
    :return:       the normalized value
    """
    return normalize_float(dgs, min_d, max_d)

def normalize_hours(hrs, min_h=0, max_h=24):
    """
    Normalize a value (in hours).
    
    :param hrs:    the value to normalize
    :param min_h:  the minimum value (defaults to 0)
    :param max_h:  the maximum value (defaults to 24)
    :return:       the normalized value
    """
    return normalize_float(hrs, min_h, max_h)
    
def pick_float(collection, index, defaultValue=None):
    """
    Pick a float from a list collection.

    :param collection:  the list collection to access
    :param index:       index of the item to pick
    :param defaultValue:    the default value to return on error (default is None)
    :return:            the float value
    """
    if (index >= 0) and (index < len(collection)):
        return to_float(collection[index], defaultValue)
    return defaultValue

def pick_int(collection, index, defaultValue=None):
    """
    Pick an int from a list collection.

    :param collection:  the list collection to access
    :param index:       index of the item to pick
    :param defaultValue:    the default value to return on error (default is None)
    :return:            the int value
    """
    if (index >= 0) and (index < len(collection)):
        return to_int(collection[index], defaultValue)
    return defaultValue

def to_float(s, defaultValue=0.0):
    """
    Make a value a float.
    
    :param s:   value to make into a float
    :param defaultValue:    value to use if the initial value cannot be made into a float
    :return:    the value as an float
    """
    try:
        if (type(s) is str) or (type(s) is float) or (type(s) is int) or (type(s) is long):
            return float(s)
    except Exception:
        pass
    return defaultValue

def to_int(s, defaultValue=0):
    """
    Make a value an int.
    
    :param s:   value to make into an int
    :param defaultValue:    value to use if the initial value cannot be made into an int
    :return:    the value as an int
    """
    try:
        if (type(s) is str) or (type(s) is float) or (type(s) is int) or (type(s) is long):
            return int(s)
    except Exception:
        pass
    return defaultValue
