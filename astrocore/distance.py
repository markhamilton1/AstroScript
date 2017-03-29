
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

# terrestrial units

def ft_to_km(d):
    return d / KILOMETER_ft

def ft_to_m(d):
    return d * FOOT_m

def ft_to_mi(d):
    return d / STATUTE_MILE_ft

def ft_to_nmi(d):
    return d / NAUTICAL_MILE_ft

def km_to_ft(d):
    return d * KILOMETER_ft

def km_to_m(d):
    return d * KILOMETER_m

def km_to_mi(d):
    return d * KILOMETER_mi

def km_to_nmi(d):
    return d / NAUTICAL_MILE_km

def m_to_ft(d):
    return d / FOOT_m

def m_to_km(d):
    return d / KILOMETER_m

def m_to_mi(d):
    return m_to_km(d) / STATUTE_MILE_km

def m_to_nmi(d):
    return m_to_km(d) / NAUTICAL_MILE_km

def mi_to_ft(d):
    return d * STATUTE_MILE_ft

def mi_to_km(d):
    return d * STATUTE_MILE_km

def mi_to_m(d):
    return mi_to_km(d) * KILOMETER_m

def mi_to_nmi(d):
    return d * NAUTICAL_MILE_mi

def nmi_to_ft(d):
    return d * NAUTICAL_MILE_ft

def nmi_to_km(d):
    return d * NAUTICAL_MILE_km

def nmi_to_m(d):
    return nmi_to_km(d) * KILOMETER_m

def nmi_to_mi(d):
    return d * NAUTICAL_MILE_mi

# astronomical units

def au_to_km(d):
    return d * ASTRONOMICAL_UNIT_km

def au_to_mi(d):
    return km_to_mi(au_to_km(d))

def au_to_nmi(d):
    return km_to_nmi(au_to_km(d))

def au_to_ly(d):
    return d / LIGHT_YEAR_au

def au_to_pc(d):
    return d / PARSEC_au

def ly_to_au(d):
    return d * LIGHT_YEAR_au

def ly_to_km(d):
    return d * LIGHT_YEAR_km

def ly_to_mi(d):
    return km_to_mi(ly_to_km(d))

def ly_to_nmi(d):
    return km_to_nmi(ly_to_km(d))

def ly_to_pc(d):
    return d * PARSEC_ly