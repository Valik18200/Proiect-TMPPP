import unittest
import threading
from builder import (
    HotLoversBoxBuilder, GourmetSpiceBoxBuilder, StarterKitBoxBuilder,
    SpiceDirector
)
from prototype import SpiceProductPrototype, SpiceProductRegistry
from singleton import SpiceStoreConfig


# ─────────────────────────────────────────
#  TESTE BUILDER
# ─────────────────────────────────────────

class TestBuilder(unittest.TestCase):

    def test_full_hot_lovers_box(self):
        builder = HotLoversBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_full_box()
        self.assertIn("Ghost Pepper", box.product_name)
        self.assertIsNotNone(box.wrapping)
        self.assertIsNotNone(box.ribbon)
        self.assertIsNotNone(box.card_message)
        self.assertTrue(len(box.extras) > 0)

    def test_full_gourmet_box(self):
        builder = GourmetSpiceBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_full_box()
        self.assertIn("Sriracha", box.product_name)
        self.assertIsNotNone(box.wrapping)
        self.assertIsNotNone(box.ribbon)
        self.assertIsNotNone(box.card_message)
        self.assertTrue(len(box.extras) > 0)

    def test_full_starter_kit_box(self):
        builder = StarterKitBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_full_box()
        self.assertIn("Sweet Chili", box.product_name)
        self.assertIsNotNone(box.wrapping)
        self.assertIsNotNone(box.card_message)

    def test_minimal_box_has_no_ribbon(self):
        builder = StarterKitBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_minimal_box()
        self.assertIsNotNone(box.product_name)
        self.assertIsNotNone(box.wrapping)
        self.assertIsNone(box.ribbon)

    def test_minimal_box_has_no_card(self):
        builder = HotLoversBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_minimal_box()
        self.assertIsNone(box.card_message)

    def test_minimal_box_has_no_extras(self):
        builder = GourmetSpiceBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_minimal_box()
        self.assertEqual(box.extras, [])

    def test_hot_lovers_extras_contains_warning(self):
        builder = HotLoversBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_full_box()
        extras_joined = " ".join(box.extras).lower()
        self.assertIn("avertisment", extras_joined)

    def test_starter_kit_has_guide(self):
        builder = StarterKitBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_full_box()
        extras_joined = " ".join(box.extras).lower()
        self.assertIn("ghid", extras_joined)

    def test_str_contains_produs_label(self):
        builder = GourmetSpiceBoxBuilder()
        director = SpiceDirector(builder)
        box = director.build_full_box()
        self.assertIn("Produs", str(box))

    def test_different_builders_produce_different_products(self):
        box_hot = SpiceDirector(HotLoversBoxBuilder()).build_full_box()
        box_starter = SpiceDirector(StarterKitBoxBuilder()).build_full_box()
        self.assertNotEqual(box_hot.product_name, box_starter.product_name)


# ─────────────────────────────────────────
#  TESTE PROTOTYPE
# ─────────────────────────────────────────

class TestPrototype(unittest.TestCase):

    def test_deep_clone_independence(self):
        original = SpiceProductPrototype(
            "Sriracha", 39.99, "sos_iute",
            {"aroma": "clasic", "variante": ["rosie", "verde"]}
        )
        clone = original.clone_deep()
        clone.name = "Sriracha Extra"
        clone.attributes["variante"].append("neagra")
        # originalul nu trebuie afectat
        self.assertEqual(original.name, "Sriracha")
        self.assertEqual(len(original.attributes["variante"]), 2)

    def test_shallow_clone_shares_attributes(self):
        original = SpiceProductPrototype(
            "Cayenne", 24.99, "condiment",
            {"forme": ["pudra", "fulgi"]}
        )
        clone = original.clone_shallow()
        clone.attributes["forme"].append("granule")
        # shallow copy — lista e impartita
        self.assertEqual(len(original.attributes["forme"]), 3)

    def test_deep_clone_price_independence(self):
        original = SpiceProductPrototype("Ghost Pepper", 69.99, "sos_iute", {})
        clone = original.clone_deep()
        clone.price = 99.99
        self.assertEqual(original.price, 69.99)

    def test_registry_register_and_clone(self):
        registry = SpiceProductRegistry()
        registry.register("sare_roz", SpiceProductPrototype(
            "Sare Roz cu Chili", 18.99, "sare_iute", {"scoville": 5000}
        ))
        clone = registry.clone("sare_roz")
        self.assertEqual(clone.name, "Sare Roz cu Chili")
        self.assertIn("sare_roz", registry.list_prototypes())

    def test_registry_clone_missing_key_raises(self):
        registry = SpiceProductRegistry()
        with self.assertRaises(KeyError):
            registry.clone("inexistent")

    def test_registry_unregister(self):
        registry = SpiceProductRegistry()
        registry.register("temp", SpiceProductPrototype("Temp", 1.0, "sos_iute", {}))
        registry.unregister("temp")
        self.assertNotIn("temp", registry.list_prototypes())

    def test_registry_deep_clone_default(self):
        registry = SpiceProductRegistry()
        registry.register("jalapeno", SpiceProductPrototype(
            "Jalapeno", 27.99, "ardei_deshidratat", {"culori": ["verde"]}
        ))
        clone = registry.clone("jalapeno")  # deep=True implicit
        clone.attributes["culori"].append("rosu")
        original_clone = registry.clone("jalapeno")
        self.assertEqual(len(original_clone.attributes["culori"]), 1)

    def test_registry_shallow_clone(self):
        registry = SpiceProductRegistry()
        registry.register("cajun", SpiceProductPrototype(
            "Cajun", 29.99, "condiment", {"ingrediente": ["paprika"]}
        ))
        clone = registry.clone("cajun", deep=False)
        self.assertEqual(clone.name, "Cajun")

    def test_str_format(self):
        proto = SpiceProductPrototype("Test", 10.0, "sos_iute", {"x": 1})
        self.assertIn("Test", str(proto))
        self.assertIn("10.00 LEI", str(proto))

    def test_multiple_prototypes_in_registry(self):
        registry = SpiceProductRegistry()
        for i in range(5):
            registry.register(f"prod_{i}", SpiceProductPrototype(f"Produs {i}", float(i), "condiment", {}))
        self.assertEqual(len(registry.list_prototypes()), 5)


# ─────────────────────────────────────────
#  TESTE SINGLETON
# ─────────────────────────────────────────

class TestSingleton(unittest.TestCase):

    def setUp(self):
        # Resetam setarile custom intre teste
        config = SpiceStoreConfig()
        config._settings = {}

    def test_same_instance(self):
        c1 = SpiceStoreConfig()
        c2 = SpiceStoreConfig()
        self.assertIs(c1, c2)

    def test_store_name(self):
        config = SpiceStoreConfig()
        self.assertEqual(config.store_name, "ARDEI ROSU")

    def test_currency(self):
        config = SpiceStoreConfig()
        self.assertEqual(config.currency, "LEI")

    def test_tax_rate(self):
        config = SpiceStoreConfig()
        self.assertAlmostEqual(config.tax_rate, 0.19)

    def test_max_discount(self):
        config = SpiceStoreConfig()
        self.assertAlmostEqual(config.max_discount, 0.25)

    def test_max_scoville_warning(self):
        config = SpiceStoreConfig()
        self.assertEqual(config.max_scoville_warning, 100_000)

    def test_set_and_get_setting(self):
        config = SpiceStoreConfig()
        config.set_setting("promotie_activa", "True")
        self.assertEqual(config.get_setting("promotie_activa"), "True")

    def test_setting_shared_across_instances(self):
        c1 = SpiceStoreConfig()
        c1.set_setting("tema", "dark")
        c2 = SpiceStoreConfig()
        self.assertEqual(c2.get_setting("tema"), "dark")

    def test_get_missing_setting_returns_none(self):
        config = SpiceStoreConfig()
        self.assertIsNone(config.get_setting("inexistent"))

    def test_get_missing_setting_returns_default(self):
        config = SpiceStoreConfig()
        self.assertEqual(config.get_setting("inexistent", "default_val"), "default_val")

    def test_thread_safety(self):
        instances = []

        def get_instance():
            instances.append(id(SpiceStoreConfig()))

        threads = [threading.Thread(target=get_instance) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(set(instances)), 1)

    def test_str_contains_store_name(self):
        config = SpiceStoreConfig()
        self.assertIn("ARDEI ROSU", str(config))

    def test_str_contains_scoville(self):
        config = SpiceStoreConfig()
        self.assertIn("SHU", str(config))


if __name__ == "__main__":
    unittest.main(verbosity=2)
