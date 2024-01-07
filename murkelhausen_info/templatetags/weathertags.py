from django import template

register = template.Library()


@register.filter
def rain_color(rain, *args, **kwargs) -> str:
    """
        leichter Sprühregen: < 0,1 mm (jeweils innerhalb von 60 Minuten)
    mäßiger Sprühregen: ≥ 0,1 mm
    starker Sprühregen: ≥ 0,5 mm
    leichter Regen: < 2,5 mm (jeweils innerhalb von 60 Minuten)
    mäßiger Regen: ≥ 2,5 mm bis < 10,0 mm
    starker Regen: ≥ 10,0 mm
    sehr starker Regen: ≥ 50,0 mm
    """
    if rain >= 50:  # sehr starker Regen
        return "rgba(255,50,50,0.9)"
    elif rain >= 10:  # starker Regen
        return "rgba(0,0,255,0.9)"
    elif rain >= 2.5:  # maessiger Regen
        return "rgba(50,50,255,0.75)"
    elif rain >= 1:  # leichter Regen
        return "rgba(100,100,255,0.5)"
    elif rain >= 0.5:  # sehr leichter Regen
        return "rgba(200,200,255,0.5)"
    else:  # minimaler Regen
        return "rgba(200,200,255,0.25)"
