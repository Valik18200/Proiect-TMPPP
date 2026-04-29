# test_patterns.py
import unittest
from Lab4.Adapter.adapter import PayPalAdapter, StripeAdapter, CashAdapter
from Lab4.Composite.composite import HotSauceItem, SauceCategory
from Lab4.Facade.facade import OrderFacade


class TestAdapter(unittest.TestCase):

    def test_paypal_adapter(self):
        processor = PayPalAdapter("client@ardeirosu.ro")
        result = processor.pay(34.99)
        self.assertIn("PayPal", result)
        self.assertIn("34.99", result)

    def test_stripe_adapter(self):
        processor = StripeAdapter("tok_123abc")
        result = processor.pay(49.99)
        self.assertIn("Stripe", result)
        self.assertIn("4999", result)

    def test_cash_adapter(self):
        processor = CashAdapter(50.0)
        result = processor.pay(34.99)
        self.assertIn("Cash", result)
        self.assertIn("rest", result)


class TestComposite(unittest.TestCase):

    def test_single_item(self):
        item = HotSauceItem("Sos Habanero", 34.99)
        self.assertEqual(item.get_price(), 34.99)

    def test_category_price(self):
        cat = SauceCategory("Sosuri iuti")
        cat.add(HotSauceItem("Sos Habanero", 34.99))
        cat.add(HotSauceItem("Sos Jalapeno", 24.99))
        self.assertAlmostEqual(cat.get_price(), 59.98, places=2)

    def test_nested_categories(self):
        root = SauceCategory("Catalog Ardeirosu")
        sosuri = SauceCategory("Sosuri")
        sosuri.add(HotSauceItem("Sos Carolina", 49.99))
        condimente = SauceCategory("Condimente")
        condimente.add(HotSauceItem("Pudra iute", 15.99))
        root.add(sosuri)
        root.add(condimente)
        self.assertAlmostEqual(root.get_price(), 65.98, places=2)

    def test_display(self):
        cat = SauceCategory("Sosuri iuti")
        cat.add(HotSauceItem("Sos Habanero", 34.99))
        result = cat.display()
        self.assertIn("Sosuri iuti", result)
        self.assertIn("Habanero", result)


class TestFacade(unittest.TestCase):

    def test_successful_order(self):
        facade = OrderFacade()
        result = facade.place_order("Sos Habanero Extreme", 0.10, True)
        self.assertIn("Plata", result)
        self.assertIn("ambalat cadou", result)

    def test_out_of_stock(self):
        facade = OrderFacade()
        result = facade.place_order("Sos Super Iute Inexistent")
        self.assertIn("nu este in stoc", result)

    def test_no_discount(self):
        facade = OrderFacade()
        result = facade.place_order("Sos Carolina Reaper")
        self.assertIn("49.99", result)


if __name__ == "__main__":
    unittest.main()