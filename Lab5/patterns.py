import unittest
from Flyweight.flyweight import HotPepperTypeFactory, ProductOnShelf
from Decorator.decorator import BasicNotification, EmailDecorator, SMSDecorator, PushDecorator, SpicyPackDecorator
from  import PhoneDisplay, WebDisplay, ListCatalogView, GridCatalogView
from proxy import RealProductService, CachingProxy, AccessControlProxy, LoggingProxy


class TestFlyweight(unittest.TestCase):

    def setUp(self):
        HotPepperTypeFactory.clear()

    def test_shared_instances(self):
        p1 = HotPepperTypeFactory.get_pepper_type("Sos iute", "Picant", "Mexic")
        p2 = HotPepperTypeFactory.get_pepper_type("Sos iute", "Picant", "Mexic")
        self.assertIs(p1, p2)

    def test_different_types(self):
        HotPepperTypeFactory.get_pepper_type("Ardei iute", "Mild", "Mexic")
        HotPepperTypeFactory.get_pepper_type("Sos iute", "Inferno", "SUA")
        self.assertEqual(HotPepperTypeFactory.get_count(), 2)

    def test_product_on_shelf(self):
        pt = HotPepperTypeFactory.get_pepper_type("Ardei iute", "Picant", "Romania")
        product = ProductOnShelf("Ardei iute de acasa", 25.99, pt)
        self.assertIn("Ardei iute de acasa", product.display())
        self.assertIn("🌶️", product.display())


class TestDecorator(unittest.TestCase):

    def test_basic(self):
        n = BasicNotification("client@mail.com")
        self.assertIn("client@mail.com", n.send("Comanda confirmata"))

    def test_email_sms(self):
        n = EmailDecorator(SMSDecorator(BasicNotification("client")))
        result = n.send("Stoc nou")
        self.assertIn("Email", result)
        self.assertIn("SMS", result)

    def test_all_decorators(self):
        n = PushDecorator(EmailDecorator(SMSDecorator(BasicNotification("client"))))
        result = n.send("Oferta iute")
        self.assertIn("Push", result)
        self.assertIn("Email", result)
        self.assertIn("SMS", result)

    def test_spicy_pack_decorator(self):
        n = SpicyPackDecorator(BasicNotification("client"))
        result = n.send("Comanda ta")
        self.assertIn("Pachet gratuit", result)
        self.assertIn("ardei iute", result)


class TestBridge(unittest.TestCase):

    def test_list_phone(self):
        view = ListCatalogView(PhoneDisplay(), ["Habanero", "Jalapeno"])
        self.assertIn("Telefon", view.show())
        self.assertIn("Habanero", view.show())

    def test_grid_web(self):
        view = GridCatalogView(WebDisplay(), ["Ghost Pepper", "Carolina Reaper"])
        self.assertIn("Web", view.show())
        self.assertIn("Grid", view.show())


class TestProxy(unittest.TestCase):

    def test_caching(self):
        service = CachingProxy(RealProductService())
        r1 = service.get_product_info("HP001")
        r2 = service.get_product_info("HP001")
        self.assertIn("[DB]", r1)
        self.assertIn("[CACHE]", r2)

    def test_access_denied(self):
        service = AccessControlProxy(RealProductService(), "guest")
        result = service.update_price("HP001", 100.0)
        self.assertIn("Acces refuzat", result)

    def test_access_admin(self):
        service = AccessControlProxy(RealProductService(), "admin")
        result = service.update_price("HP001", 100.0)
        self.assertIn("actualizat", result)

    def test_logging(self):
        service = LoggingProxy(RealProductService())
        service.get_product_info("HP001")
        service.update_price("HP002", 150.0)
        self.assertEqual(len(service.logs), 2)


if __name__ == "__main__":
    unittest.main()