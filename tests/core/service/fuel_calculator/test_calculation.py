from core.service.fuel_calculator.calculation import calculation_fuel


class TestCalculationFuel:
    def test_calculation01_computes_price(self):
        # (6.5 / 100) * 6.0 * 100 + 10 = 49.0
        result, err, ok = calculation_fuel(way=100, fuel=6.0, combustion=6.5, remaining_values=10)

        assert ok is True and err is None
        assert result.price == 49.0
        assert result.pattern == "(6.5 / 100) * 6.0 * 100 + 10"

    def test_calculation02_zero_way_gives_only_remaining_values(self):
        result, err, ok = calculation_fuel(way=0, fuel=6.0, combustion=6.5, remaining_values=15)

        assert ok is True
        assert result.price == 15

    def test_calculation03_negative_remaining_values_lowers_price(self):
        result, err, ok = calculation_fuel(way=100, fuel=6.0, combustion=6.5, remaining_values=-10)

        assert ok is True
        assert result.price == 29.0
