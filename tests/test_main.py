import unittest
import scraper as sc


def generate_all_pairs_even():
    pairs = [('catcoin', 16853.7), ('piesełcoin', 1257.29), ('mommycoin', 1.0), ('ilovecheesecoin', 282.8)]
    return pairs


def response_all_pairs_even():
    pair1 = [('catcoin', 16853.7), ('piesełcoin', 1257.29)]
    pair2 = [('mommycoin', 1.0), ('ilovecheesecoin', 282.8)]
    return pair1, pair2


def generate_all_pairs_odd():
    pairs = [('catcoin', 16853.7), ('piesełcoin', 1257.29), ('mommycoin', 1.0), ('ilovecheesecoin', 282.8),
             ('givemejobcoin', 666.0)]
    return pairs


def response_all_pairs_odd():
    pair1 = [('catcoin', 16853.7), ('piesełcoin', 1257.29)]
    pair2 = [('mommycoin', 1.0), ('ilovecheesecoin', 282.8), ('givemejobcoin', 666.0)]
    return pair1, pair2


class TestScraper(unittest.TestCase):

    def test_message_split_even(self):
        result = sc.message_split(generate_all_pairs_even())
        self.assertEqual(result, response_all_pairs_even())

    def test_message_split_odd(self):
        result = sc.message_split(generate_all_pairs_odd())
        self.assertEqual(result, response_all_pairs_odd())

    def test_coin_supported_by_bot_true(self):
        self.assertTrue(sc.coin_supported_by_bot("bitcoin"))

    def test_coin_supported_by_bot_false(self):
        self.assertFalse(sc.coin_supported_by_bot("please"))

    def test_increase_alert_smaller(self):
        result = sc.increase_alert(5, [6, 66, 666])
        self.assertEqual(result, [])

    def test_increase_alert_equal(self):
        result = sc.increase_alert(5, [2, 5, 6])
        self.assertEqual(result, [2, 5])

    def test_increase_alert_bigger(self):
        result = sc.increase_alert(5, [2, 4, 6])
        self.assertEqual(result, [2, 4])

    def test_decrease_alert_smaller(self):
        result = sc.decrease_alert(5, [2, 4, 6])
        self.assertEqual(result, [6])

    def test_decrease_alert_equal(self):
        result = sc.decrease_alert(5, [2, 5, 6])
        self.assertEqual(result, [6, 5])

    def test_decrease_alert_bigger(self):
        result = sc.decrease_alert(5, [2, 3, 4])
        self.assertEqual(result, [])

    def test_trend_start_smaller_than_end(self):
        result = sc.trend(0, 5, [2, 4, 6])
        self.assertEqual(result, [2, 4])

    def test_trend_start_equal_to_end(self):
        result = sc.trend(5, 5, [2, 4, 6])
        self.assertEqual(result, [])

    def test_trend_start_bigger_to_end(self):
        result = sc.trend(5, 0, [2, 4, 6])
        self.assertEqual(result, [6, 4, 2])

    def test_get_price_helper_function_coin_exists(self):
        self.assertTrue(sc.get_price_helper_function('bitcoin'))

    def test_get_price_helper_function_coin_exists_not(self):
        result = sc.get_price_helper_function('pixelek')
        self.assertEqual(result, None)
