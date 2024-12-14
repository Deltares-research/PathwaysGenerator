# pylint: disable=too-many-return-statements
import dataclasses
from enum import Enum


class MetricEstimate(Enum):
    MANUAL = 1
    SUM = 2
    AVERAGE = 3
    MINIMUM = 4
    MAXIMUM = 5
    LAST = 6

    def __repr__(self) -> str:
        match self:
            case MetricEstimate.MANUAL:
                return "Manual"
            case MetricEstimate.SUM:
                return "Sum"
            case MetricEstimate.AVERAGE:
                return "Average"
            case MetricEstimate.MINIMUM:
                return "Minimum"
            case MetricEstimate.MAXIMUM:
                return "Max"
            case MetricEstimate.LAST:
                return "Last"
            case _:
                return "Unknown"


@dataclasses.dataclass
class MetricUnit:
    name: str
    symbol: str
    short_name: str | None = None
    symbol_plural: str | None = None
    place_after_value: bool = True
    value_format: str = "n"

    @property
    def display_name(self):
        if self.short_name is not None:
            return self.short_name

        return self.symbol

    def get_symbol(self, value: float):
        return (
            self.symbol_plural
            if value > 1 and self.symbol_plural is not None
            else self.symbol
        )

    def format(self, value: float):
        symbol = self.get_symbol(value)

        if self.place_after_value:
            return f"{value:{self.value_format}}{symbol}"

        return f"{symbol}{value:{self.value_format}}"


@dataclasses.dataclass
class Metric:
    id: str
    name: str
    current_value: float
    estimate: MetricEstimate
    unit_or_default: MetricUnit | str

    @property
    def unit(self) -> MetricUnit:
        if isinstance(self.unit_or_default, str):
            default_unit = default_units.find(self.unit_or_default)
            if default_unit is None:
                return MetricUnit(
                    name=self.unit_or_default, symbol=self.unit_or_default
                )
            return default_unit
        return self.unit_or_default

    def __hash__(self) -> int:
        return self.id.__hash__()


@dataclasses.dataclass
class MetricValue:
    value: float
    is_estimate: bool = False


class DefaultUnits:
    FORMAT_SLIDER = "n"

    class Length:
        si = (
            MetricUnit(name="Millimeter", symbol="mm"),
            MetricUnit(name="Centimeter", symbol="cm"),
            MetricUnit(name="Meter", symbol="m"),
            MetricUnit(name="Kilometer", symbol="km"),
        )
        imperial = [
            MetricUnit(name="Inch", symbol="in"),
            MetricUnit(name="Foot", symbol="ft"),
            MetricUnit(name="Yard", symbol="yd"),
            MetricUnit(name="Mile", symbol="mi"),
        ]

    length = Length()

    class Area:
        si = [
            MetricUnit(name="Square Meter", symbol="m^2"),
            MetricUnit(name="Square Kilometer", symbol="km^2"),
            MetricUnit(name="Hectare", symbol="ha"),
        ]
        imperial = [
            MetricUnit(name="Square Feet", symbol="ft^2"),
            MetricUnit(name="Acre", symbol="acre", symbol_plural="acres"),
            MetricUnit(name="Square Mile", symbol="sq mi"),
        ]

    area = Area()

    class Volume:
        si = [
            MetricUnit(name="Milliliter", symbol="ml"),
            MetricUnit(name="Liter", symbol="l"),
            MetricUnit(name="Cubic Centimeter", symbol="cm^3"),
            MetricUnit(name="Cubic Meter", symbol="m^3"),
        ]
        imperial = [
            MetricUnit(name="Fluid Ounce", symbol="fl oz"),
            MetricUnit(name="Pint", symbol="pt"),
            MetricUnit(name="Quart", symbol="qt"),
            MetricUnit(name="Gallon", symbol="gal"),
        ]

    volume = Volume()

    class Temperature:
        si = [
            MetricUnit(name="Celsius", symbol="°C"),
            MetricUnit(name="Kelvin", symbol="K"),
        ]
        imperial = [
            MetricUnit(name="Fahrenheit", symbol="°F"),
        ]

    temperature = Temperature()

    class Velocity:
        si = [
            MetricUnit(name="Meters/Second", symbol="m/s"),
            MetricUnit(name="Kilometers/Hour", symbol="km/h"),
            MetricUnit(name="Meters/Second^2", symbol="m/s^2"),
        ]
        imperial = [
            MetricUnit(name="Miles/Hour", symbol="mph"),
            MetricUnit(name="Feet/Second^2", symbol="ft/s^2"),
        ]

    velocity = Velocity()

    class Acceleration:
        si = [
            MetricUnit(name="Meters/Second^2", symbol="m/s^2"),
        ]
        imperial = [
            MetricUnit(name="Feet/Second^2", symbol="ft/s^2"),
        ]

    acceleration = Acceleration()

    class MassWeight:
        si = [
            MetricUnit(name="Milligram", symbol="mg"),
            MetricUnit(name="Gram", symbol="g"),
            MetricUnit(name="Kilogram", symbol="kg"),
            MetricUnit(name="Tonne", symbol="t"),
        ]
        imperial = [
            MetricUnit(name="Pound", symbol="lb"),
            MetricUnit(name="Ounce", symbol="oz"),
            MetricUnit(name="Ton", symbol="ton"),
        ]

    mass_weight = MassWeight()

    time = [
        MetricUnit(name="Millisecond", symbol="ms"),
        MetricUnit(name="Second", symbol="s"),
        MetricUnit(name="Minute", symbol="min"),
        MetricUnit(name="Hour", symbol="hr"),
        MetricUnit(name="Day", symbol="day"),
        MetricUnit(name="Year", symbol="yr"),
    ]

    currency = [
        MetricUnit(
            name="US Dollar", short_name="$ USD", symbol="$", place_after_value=False
        ),
        MetricUnit(
            name="Euro", short_name="€ EUR", symbol="€", place_after_value=False
        ),
        MetricUnit(
            name="British Pound",
            short_name="£ GBP",
            symbol="£",
            place_after_value=False,
        ),
    ]

    relative = [
        MetricUnit(name="Percent", symbol="%", value_format=".2%"),
        MetricUnit(
            name="Impact", symbol="", short_name="Impact", value_format=FORMAT_SLIDER
        ),
    ]

    def all(self):
        yield from self.length.si
        yield from self.length.imperial
        yield from self.area.si
        yield from self.area.imperial
        yield from self.volume.si
        yield from self.volume.imperial
        yield from self.temperature.si
        yield from self.temperature.imperial
        yield from self.velocity.si
        yield from self.velocity.imperial
        yield from self.acceleration.si
        yield from self.acceleration.imperial
        yield from self.mass_weight.si
        yield from self.mass_weight.imperial
        yield from self.time
        yield from self.currency
        yield from self.relative

    def find(self, symbol) -> MetricUnit | None:
        for unit in self.all():
            if symbol in (unit.symbol, unit.short_name):
                return unit

        return None


default_units = DefaultUnits()
