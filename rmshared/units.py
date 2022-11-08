class TimeUnit(int):
    multiplier: int

    def __new__(cls, count):
        return super(TimeUnit, cls).__new__(cls, count * cls.multiplier)


class Seconds(TimeUnit):
    multiplier = 1


class Minutes(TimeUnit):
    multiplier = 60 * Seconds.multiplier


class Hours(TimeUnit):
    multiplier = 60 * Minutes.multiplier


class Days(TimeUnit):
    multiplier = 24 * Hours.multiplier
