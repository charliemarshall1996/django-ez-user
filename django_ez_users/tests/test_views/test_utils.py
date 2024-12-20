from random import randint

from django_ez_users.views.utils import ConversionCalculator


def test_conversion_calculator_basic_conversion_rate():
    applications = randint(1, 1000)
    interviews_or_offers = randint(applications, 1000)
    answer = (interviews_or_offers / applications) * 100
    assert (
        ConversionCalculator.calculate_basic_conversion_rate(
            applications, interviews_or_offers
        )
        == answer
    )


def test_conversion_calculator_basic_conversion_rate_zero_interviews_or_offers():
    applications = randint(1, 1000)
    interviews_or_offers = 0
    answer = 0
    assert (
        ConversionCalculator.calculate_basic_conversion_rate(
            applications, interviews_or_offers
        )
        == answer
    )


def test_conversion_calculator_conversion_rate():
    applications = randint(1, 1000)
    interviews = randint(applications, 1000)
    offers = randint(applications, 1000)
    answer = ((interviews + offers) / applications) * 100
    assert (
        ConversionCalculator.calculate_conversion_rate(
            applications, interviews, offers)
        == answer
    )


def test_conversion_calculator_conversion_rate_zero_interviews():
    applications = randint(1, 1000)
    interviews = 0
    offers = randint(applications, 1000)
    answer = ((interviews + offers) / applications) * 100
    assert (
        ConversionCalculator.calculate_conversion_rate(
            applications, interviews, offers)
        == answer
    )


def test_conversion_calculator_conversion_rate_zero_offers():
    applications = randint(1, 1000)
    interviews = randint(applications, 1000)
    offers = 0
    answer = ((interviews + offers) / applications) * 100
    assert (
        ConversionCalculator.calculate_conversion_rate(
            applications, interviews, offers)
        == answer
    )


def test_conversion_calculator_conversion_score():
    applications = randint(1, 1000)
    interviews = randint(applications, 1000)
    offers = randint(applications, 1000)
    answer = ((interviews + (offers * 2)) / applications) * 100
    assert (
        ConversionCalculator.calculate_conversion_score(
            applications, interviews, offers
        )
        == answer
    )


def test_conversion_calculator_conversion_score_zero_interviews():
    applications = randint(1, 1000)
    interviews = 0
    offers = randint(applications, 1000)
    answer = ((interviews + (offers * 2)) / applications) * 100
    assert (
        ConversionCalculator.calculate_conversion_score(
            applications, interviews, offers
        )
        == answer
    )


def test_conversion_calculator_conversion_score_zero_offers():
    applications = randint(1, 1000)
    interviews = randint(applications, 1000)
    offers = 0
    answer = ((interviews + (offers * 2)) / applications) * 100
    assert (
        ConversionCalculator.calculate_conversion_score(
            applications, interviews, offers
        )
        == answer
    )
