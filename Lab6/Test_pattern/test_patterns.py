# test_patterns.py
import unittest
from Lab6.Strategy.strategy import SauceCatalog, SortByPrice, SortByPriceDesc, SortByName, SortByScoville, SortByScovilleDesc
from Lab6.Observer.observer import HotSauceStore, EmailSubscriber, SMSSubscriber, DashboardLogger
from Lab6.Command.command import Inventory, AddStockCommand, RemoveStockCommand, UpdatePriceCommand, CommandHistory
from Lab6.Memento.memento import ShoppingCart, CartHistory
from Lab6.Iterator.iterator import HotSauce, SauceCollection


class TestStrategy(unittest.TestCase):

    def setUp(self):
        self.catalog = SauceCatalog()
        self.catalog.add_sauce("Sos Carolina Reaper", 49.99, 2200000)
        self.catalog.add_sauce("Sos Habanero Extreme", 34.99, 350000)
        self.catalog.add_sauce("Sos Jalapeno Classic", 24.99, 5000)

    def test_sort_by_price(self):
        self.catalog.set_sort_strategy(SortByPrice())
        result = self.catalog.get_sorted()
        self.assertEqual(result[0]["name"], "Sos Jalapeno Classic")

    def test_sort_by_price_desc(self):
        self.catalog.set_sort_strategy(SortByPriceDesc())
        result = self.catalog.get_sorted()
        self.assertEqual(result[0]["name"], "Sos Carolina Reaper")

    def test_sort_by_name(self):
        self.catalog.set_sort_strategy(SortByName())
        result = self.catalog.get_sorted()
        self.assertEqual(result[0]["name"], "Sos Carolina Reaper")  # C < H < J

    def test_sort_by_scoville(self):
        self.catalog.set_sort_strategy(SortByScoville())
        result = self.catalog.get_sorted()
        self.assertEqual(result[0]["name"], "Sos Jalapeno Classic")

    def test_sort_by_scoville_desc(self):
        self.catalog.set_sort_strategy(SortByScovilleDesc())
        result = self.catalog.get_sorted()
        self.assertEqual(result[0]["name"], "Sos Carolina Reaper")


class TestObserver(unittest.TestCase):

    def test_email_notification_new_product(self):
        store = HotSauceStore()
        sub = EmailSubscriber("client@ardeirosu.ro")
        store.attach(sub)
        store.new_product("Sos Ghost Pepper", 44.99, 1000000)
        self.assertEqual(len(sub.messages), 1)
        self.assertIn("Ghost Pepper", sub.messages[0])

    def test_sms_price_drop(self):
        store = HotSauceStore()
        sms = SMSSubscriber("+37312345678")
        store.attach(sms)
        store.price_drop("Sos Habanero", 34.99, 29.99)
        self.assertIn("OFERTA", sms.messages[0])

    def test_detach(self):
        store = HotSauceStore()
        sub = EmailSubscriber("test@ardeirosu.ro")
        store.attach(sub)
        store.detach(sub)
        store.new_product("Test", 10.0, 1000)
        self.assertEqual(len(sub.messages), 0)

    def test_spicy_challenge(self):
        store = HotSauceStore()
        sms = SMSSubscriber("+37312345678")
        store.attach(sms)
        store.spicy_challenge("Carolina Reaper Extreme", 3000000)
        self.assertIn("PROVOCARE", sms.messages[0])


class TestCommand(unittest.TestCase):

    def setUp(self):
        self.inv = Inventory()
        self.history = CommandHistory()

    def test_add_and_undo(self):
        self.history.execute(AddStockCommand(self.inv, "Sos Habanero", 5))
        self.assertEqual(self.inv.get_stock("Sos Habanero"), 5)
        self.history.undo()
        self.assertEqual(self.inv.get_stock("Sos Habanero"), 0)

    def test_remove_and_undo(self):
        self.history.execute(AddStockCommand(self.inv, "Sos Carolina", 10))
        self.history.execute(RemoveStockCommand(self.inv, "Sos Carolina", 3))
        self.assertEqual(self.inv.get_stock("Sos Carolina"), 7)
        self.history.undo()
        self.assertEqual(self.inv.get_stock("Sos Carolina"), 10)

    def test_redo(self):
        self.history.execute(AddStockCommand(self.inv, "Pudra iute", 3))
        self.history.undo()
        self.history.redo()
        self.assertEqual(self.inv.get_stock("Pudra iute"), 3)

    def test_update_price(self):
        prices = {"Sos Test": 29.99}
        self.history.execute(UpdatePriceCommand(prices, "Sos Test", 39.99))
        self.assertEqual(prices["Sos Test"], 39.99)
        self.history.undo()
        self.assertEqual(prices["Sos Test"], 29.99)


class TestMemento(unittest.TestCase):

    def test_save_restore(self):
        cart = ShoppingCart()
        cart.add_item("Sos Habanero", 34.99, 350000)
        snapshot = cart.save()
        cart.add_item("Sos Carolina", 49.99, 2200000)
        self.assertAlmostEqual(cart.get_total(), 84.98, places=2)
        cart.restore(snapshot)
        self.assertAlmostEqual(cart.get_total(), 34.99, places=2)

    def test_multiple_snapshots(self):
        cart = ShoppingCart()
        history = CartHistory()
        cart.add_item("Sos Jalapeno", 24.99, 5000)
        history.save(cart.save())
        cart.add_item("Sos Habanero", 34.99, 350000)
        history.save(cart.save())
        snapshots = history.list_snapshots()
        self.assertEqual(len(snapshots), 2)

    def test_restore_old_snapshot(self):
        cart = ShoppingCart()
        history = CartHistory()
        cart.add_item("Produs1", 10.0, 1000)
        history.save(cart.save())
        cart.add_item("Produs2", 20.0, 2000)
        history.save(cart.save())
        cart.restore(history.get_snapshot(0))
        self.assertEqual(cart.get_total(), 10.0)


class TestIterator(unittest.TestCase):

    def setUp(self):
        self.collection = SauceCollection()
        self.collection.add(HotSauce("Sos Habanero", 34.99, "Sos iute", 350000))
        self.collection.add(HotSauce("Sos Carolina Reaper", 49.99, "Sos iute", 2200000))
        self.collection.add(HotSauce("Pudra iute", 29.99, "Condiment", 1600000))
        self.collection.add(HotSauce("Set Cadou", 99.99, "Set cadou", 0))

    def test_full_iteration(self):
        count = sum(1 for _ in self.collection.iterator())
        self.assertEqual(count, 4)

    def test_category_filter(self):
        it = self.collection.category_iterator("Sos iute")
        items = list(it)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "Sos Habanero")

    def test_price_range(self):
        it = self.collection.price_range_iterator(30.0, 50.0)
        items = list(it)
        self.assertEqual(len(items), 2)

    def test_scoville_range(self):
        it = self.collection.scoville_range_iterator(100000, 1000000)
        items = list(it)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Sos Habanero")

    def test_extreme_iterator(self):
        it = self.collection.extreme_iterator(1000000)
        items = list(it)
        self.assertEqual(len(items), 2)  # Carolina (2.2M) + Pudra (1.6M)


if __name__ == "__main__":
    unittest.main()