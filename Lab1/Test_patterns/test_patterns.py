import unittest
from factory_method import (
    SrirachaFactory, HabaneroMangoFactory, GhostPepperSauceFactory,
    CayennePowderFactory, CajunBlendFactory,
    JalapenoWholePepperFactory, CarolinaReaperFactory,
    PinkHimalayaSaltFactory, BlackSaltGhostFactory,
    HotSauce, Spice, DriedPepper, HotSalt,
)
from abstract_factory import (
    MildPackageFactory, MediumPackageFactory, InfernoPackageFactory,
    MildSauce, MildSpiceBlend, MildPepperSample,
    MediumSauce, MediumSpiceBlend, MediumPepperSample,
    InfernoSauce, InfernoSpiceBlend, InfernoPepperSample,
)


# ─────────────────────────────────────────
#  TESTE FACTORY METHOD
# ─────────────────────────────────────────

class TestFactoryMethod(unittest.TestCase):

    # --- Tipuri returnate ---

    def test_sriracha_factory_returns_hot_sauce(self):
        product = SrirachaFactory().create_product()
        self.assertIsInstance(product, HotSauce)

    def test_habanero_mango_factory_returns_hot_sauce(self):
        product = HabaneroMangoFactory().create_product()
        self.assertIsInstance(product, HotSauce)

    def test_ghost_pepper_sauce_factory_returns_hot_sauce(self):
        product = GhostPepperSauceFactory().create_product()
        self.assertIsInstance(product, HotSauce)

    def test_cayenne_factory_returns_spice(self):
        product = CayennePowderFactory().create_product()
        self.assertIsInstance(product, Spice)

    def test_cajun_factory_returns_spice(self):
        product = CajunBlendFactory().create_product()
        self.assertIsInstance(product, Spice)

    def test_jalapeno_factory_returns_dried_pepper(self):
        product = JalapenoWholePepperFactory().create_product()
        self.assertIsInstance(product, DriedPepper)

    def test_carolina_reaper_factory_returns_dried_pepper(self):
        product = CarolinaReaperFactory().create_product()
        self.assertIsInstance(product, DriedPepper)

    def test_pink_salt_factory_returns_hot_salt(self):
        product = PinkHimalayaSaltFactory().create_product()
        self.assertIsInstance(product, HotSalt)

    def test_black_salt_factory_returns_hot_salt(self):
        product = BlackSaltGhostFactory().create_product()
        self.assertIsInstance(product, HotSalt)

    # --- Nume produse ---

    def test_sriracha_name(self):
        product = SrirachaFactory().create_product()
        self.assertEqual(product.name, "Sriracha Original")

    def test_habanero_mango_name(self):
        product = HabaneroMangoFactory().create_product()
        self.assertEqual(product.name, "Habanero Mango Blast")

    def test_ghost_pepper_name(self):
        product = GhostPepperSauceFactory().create_product()
        self.assertEqual(product.name, "Ghost Pepper Inferno")

    def test_cayenne_name(self):
        product = CayennePowderFactory().create_product()
        self.assertEqual(product.name, "Cayenne Pudra")

    def test_jalapeno_name(self):
        product = JalapenoWholePepperFactory().create_product()
        self.assertEqual(product.name, "Jalapeno Intreg")

    def test_carolina_reaper_name(self):
        product = CarolinaReaperFactory().create_product()
        self.assertEqual(product.name, "Carolina Reaper Pudra")

    def test_pink_salt_name(self):
        product = PinkHimalayaSaltFactory().create_product()
        self.assertEqual(product.name, "Sare Roz cu Chili")

    def test_black_salt_name(self):
        product = BlackSaltGhostFactory().create_product()
        self.assertEqual(product.name, "Sare Neagra cu Ghost Pepper")

    # --- Valori Scoville corecte ---

    def test_sriracha_scoville(self):
        product = SrirachaFactory().create_product()
        self.assertEqual(product.scoville, 2200)

    def test_carolina_reaper_scoville_is_extreme(self):
        product = CarolinaReaperFactory().create_product()
        self.assertGreater(product.scoville, 1_000_000)

    def test_ghost_pepper_scoville(self):
        product = GhostPepperSauceFactory().create_product()
        self.assertEqual(product.scoville, 100000)

    # --- Preturi pozitive ---

    def test_all_factories_produce_positive_price(self):
        factories = [
            SrirachaFactory(), HabaneroMangoFactory(), GhostPepperSauceFactory(),
            CayennePowderFactory(), CajunBlendFactory(),
            JalapenoWholePepperFactory(), CarolinaReaperFactory(),
            PinkHimalayaSaltFactory(), BlackSaltGhostFactory(),
        ]
        for factory in factories:
            with self.subTest(factory=type(factory).__name__):
                product = factory.create_product()
                self.assertGreater(product.price, 0)

    # --- order_product returneaza produsul corect ---

    def test_order_product_returns_product(self):
        factory = SrirachaFactory()
        product = factory.order_product()
        self.assertIsNotNone(product)
        self.assertIsInstance(product, HotSauce)

    # --- Atribute specifice subclaselor ---

    def test_jalapeno_is_whole(self):
        product = JalapenoWholePepperFactory().create_product()
        self.assertTrue(product.whole)

    def test_carolina_reaper_is_not_whole(self):
        product = CarolinaReaperFactory().create_product()
        self.assertFalse(product.whole)

    def test_sriracha_flavor(self):
        product = SrirachaFactory().create_product()
        self.assertEqual(product.flavor, "clasic")

    def test_cayenne_form_is_pudra(self):
        product = CayennePowderFactory().create_product()
        self.assertEqual(product.form, "pudra")

    def test_cajun_weight(self):
        product = CajunBlendFactory().create_product()
        self.assertEqual(product.weight_g, 250)


# ─────────────────────────────────────────
#  TESTE ABSTRACT FACTORY
# ─────────────────────────────────────────

class TestAbstractFactory(unittest.TestCase):

    # --- Tipuri returnate per pachet ---

    def test_mild_package_types(self):
        factory = MildPackageFactory()
        package = factory.create_package()
        self.assertIsInstance(package["sauce"],         MildSauce)
        self.assertIsInstance(package["spice_blend"],   MildSpiceBlend)
        self.assertIsInstance(package["pepper_sample"], MildPepperSample)

    def test_medium_package_types(self):
        factory = MediumPackageFactory()
        package = factory.create_package()
        self.assertIsInstance(package["sauce"],         MediumSauce)
        self.assertIsInstance(package["spice_blend"],   MediumSpiceBlend)
        self.assertIsInstance(package["pepper_sample"], MediumPepperSample)

    def test_inferno_package_types(self):
        factory = InfernoPackageFactory()
        package = factory.create_package()
        self.assertIsInstance(package["sauce"],         InfernoSauce)
        self.assertIsInstance(package["spice_blend"],   InfernoSpiceBlend)
        self.assertIsInstance(package["pepper_sample"], InfernoPepperSample)

    # --- Pachetul contine toate cele 3 componente ---

    def test_package_has_all_components(self):
        for factory_cls in [MildPackageFactory, MediumPackageFactory, InfernoPackageFactory]:
            with self.subTest(factory=factory_cls.__name__):
                package = factory_cls().create_package()
                self.assertIn("sauce",         package)
                self.assertIn("spice_blend",   package)
                self.assertIn("pepper_sample", package)

    # --- Consistenta intre apeluri repetate ---

    def test_package_consistency(self):
        for factory_cls in [MildPackageFactory, MediumPackageFactory, InfernoPackageFactory]:
            factory = factory_cls()
            pkg1 = factory.create_package()
            pkg2 = factory.create_package()
            with self.subTest(factory=factory_cls.__name__):
                self.assertEqual(type(pkg1["sauce"]),         type(pkg2["sauce"]))
                self.assertEqual(type(pkg1["spice_blend"]),   type(pkg2["spice_blend"]))
                self.assertEqual(type(pkg1["pepper_sample"]), type(pkg2["pepper_sample"]))

    # --- Pachetele diferite nu produc aceleasi tipuri ---

    def test_mild_and_inferno_packages_are_different(self):
        mild_pkg    = MildPackageFactory().create_package()
        inferno_pkg = InfernoPackageFactory().create_package()
        self.assertNotEqual(type(mild_pkg["sauce"]),         type(inferno_pkg["sauce"]))
        self.assertNotEqual(type(mild_pkg["spice_blend"]),   type(inferno_pkg["spice_blend"]))
        self.assertNotEqual(type(mild_pkg["pepper_sample"]), type(inferno_pkg["pepper_sample"]))

    # --- Descrierile nu sunt goale ---

    def test_all_components_have_description(self):
        for factory_cls in [MildPackageFactory, MediumPackageFactory, InfernoPackageFactory]:
            package = factory_cls().create_package()
            for key, component in package.items():
                with self.subTest(factory=factory_cls.__name__, component=key):
                    self.assertTrue(len(component.get_description()) > 0)

    # --- __str__ functioneaza corect ---

    def test_str_matches_description(self):
        for factory_cls in [MildPackageFactory, MediumPackageFactory, InfernoPackageFactory]:
            package = factory_cls().create_package()
            for key, component in package.items():
                with self.subTest(factory=factory_cls.__name__, component=key):
                    self.assertEqual(str(component), component.get_description())


if __name__ == "__main__":
    unittest.main(verbosity=2)
