import mathutils
import sys


KILOMETER_ft = 3280.8398950131233596
METER_ft = KILOMETER_ft / 1000.0

FOOT_m = 1.0 / METER_ft
KILOMETER_m = 1000.0

STATUTE_MILE_nmi = 0.8689762419006479

KILOMETER_mi = 0.621371192237334
NAUTICAL_MILE_mi = 1.1507794480235425

STATUTE_MILE_ft = 5280.0
NAUTICAL_MILE_ft = 6076.1154855643044619

STATUTE_MILE_km = 1.609344
NAUTICAL_MILE_km = 1.852
ASTRONOMICAL_UNIT_km = 149597871.0
LIGHT_YEAR_km = 9460730472580.8
PARSEC_km = 30856775670468.0

LIGHT_YEAR_au = 63241.0770880709446742
PARSEC_au = 206264.80624709635488

PARSEC_ly = PARSEC_au / LIGHT_YEAR_au


UNITS = ('ft', 'm', 'km', 'mi', 'nmi', 'au', 'ly', 'pc')


# terrestrial units

def ft_to_au(d):
    return km_to_au(ft_to_km(d))

def ft_to_km(d):
    return d / KILOMETER_ft

def ft_to_ly(d):
    return km_to_ly(ft_to_km(d))

def ft_to_m(d):
    return d * FOOT_m

def ft_to_mi(d):
    return d / STATUTE_MILE_ft

def ft_to_nmi(d):
    return d / NAUTICAL_MILE_ft

def ft_to_pc(d):
    return km_to_pc(ft_to_km(d))

def km_to_au(d):
    return d / ASTRONOMICAL_UNIT_km

def km_to_ft(d):
    return d * KILOMETER_ft

def km_to_ly(d):
    return d / LIGHT_YEAR_km

def km_to_m(d):
    return d * KILOMETER_m

def km_to_mi(d):
    return d * KILOMETER_mi

def km_to_nmi(d):
    return d / NAUTICAL_MILE_km

def km_to_pc(d):
    return d / PARSEC_km

def m_to_au(d):
    return d / ASTRONOMICAL_UNIT_km

def m_to_ft(d):
    return d / FOOT_m

def m_to_km(d):
    return d / KILOMETER_m

def m_to_ly(d):
    return m_to_km(d) / LIGHT_YEAR_km

def m_to_mi(d):
    return m_to_km(d) / STATUTE_MILE_km

def m_to_nmi(d):
    return m_to_km(d) / NAUTICAL_MILE_km

def m_to_pc(d):
    return m_to_km(d) / PARSEC_km

def mi_to_au(d):
    return km_to_au(mi_to_km(d))

def mi_to_ft(d):
    return d * STATUTE_MILE_ft

def mi_to_km(d):
    return d * STATUTE_MILE_km

def mi_to_ly(d):
    return km_to_ly(mi_to_km(d))

def mi_to_m(d):
    return km_to_m(mi_to_km(d))

def mi_to_nmi(d):
    return d * NAUTICAL_MILE_mi

def mi_to_pc(d):
    return km_to_pc(mi_to_km(d))

def nmi_to_au(d):
    return km_to_au(nmi_to_km(d))

def nmi_to_ft(d):
    return d * NAUTICAL_MILE_ft

def nmi_to_km(d):
    return d * NAUTICAL_MILE_km

def nmi_to_ly(d):
    return km_to_ly(nmi_to_km(d))

def nmi_to_m(d):
    return km_to_m(nmi_to_km(d))

def nmi_to_mi(d):
    return d * NAUTICAL_MILE_mi

def nmi_to_pc(d):
    return km_to_pc(nmi_to_km(d))

# astronomical units

def au_to_ft(d):
    return km_to_ft(au_to_km(d))

def au_to_km(d):
    return d * ASTRONOMICAL_UNIT_km

def au_to_ly(d):
    return d / LIGHT_YEAR_au

def au_to_m(d):
    return km_to_m(d * ASTRONOMICAL_UNIT_km)

def au_to_mi(d):
    return km_to_mi(au_to_km(d))

def au_to_nmi(d):
    return km_to_nmi(au_to_km(d))

def au_to_pc(d):
    return d / PARSEC_au

def ly_to_au(d):
    return d * LIGHT_YEAR_au

def ly_to_ft(d):
    return km_to_ft(ly_to_km(d))

def ly_to_km(d):
    return d * LIGHT_YEAR_km

def ly_to_m(d):
    return km_to_m(ly_to_km(d))

def ly_to_mi(d):
    return km_to_mi(ly_to_km(d))

def ly_to_nmi(d):
    return km_to_nmi(ly_to_km(d))

def ly_to_pc(d):
    return d * PARSEC_ly

def pc_to_au(d):
    return d * PARSEC_au

def pc_to_ft(d):
    return km_to_ft(d / PARSEC_km)

def pc_to_m(d):
    return km_to_m(d / PARSEC_km)

def pc_to_mi(d):
    return km_to_mi(d / PARSEC_km)

def pc_to_nmi(d):
    return km_to_nmi(d / PARSEC_km)

def pc_to_ly(d):
    return d * PARSEC_ly


def convert(v, fr, to, defaultValue=None):
    v = mathutils.to_float(v, defaultValue)
    if fr == to:
        return v
    if fr not in UNITS:
        raise ValueError("Invalid from type! Unknown type '{}'".format(fr))
    if to not in UNITS:
        raise ValueError("Invalid from type! Unknown type '{}'".format(to))
    name = "{}_to_{}".format(fr, to)
    func = getattr(sys.modules[__name__], name)
    return func(v)
