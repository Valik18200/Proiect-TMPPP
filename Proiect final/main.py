"""
ARDEI ROSU — Demo complet: toate cele 20 de design patterns
"""
# ── Creational ──
from factory_method   import SrirachaFactory, GhostPepperSauceFactory, CayennePowderFactory, JalapenoWholePepperFactory, PinkHimalayaSaltFactory
from abstract_factory import MildPackageFactory, MediumPackageFactory, InfernoPackageFactory
from builder          import HotLoversBoxBuilder, GourmetSpiceBoxBuilder, StarterKitBoxBuilder, SpiceDirector
from prototype        import SpiceProductPrototype, SpiceProductRegistry
from singleton        import SpiceStoreConfig
# ── Structural ──
from adapter          import PayPalAdapter, StripeAdapter, CashAdapter, CryptoAdapter
from composite        import SpiceItem, SpiceCategory
from facade           import SpiceOrderFacade
from flyweight        import SpiceTypeFactory, SpiceOnShelf
from decorator        import BasicNotification, EmailDecorator, SMSDecorator, HeatWarningDecorator
from bridge           import PhoneDisplay, WebDisplay, ListCatalogView, HeatScaleCatalogView, DetailCatalogView
from proxy            import RealSpiceService, CachingProxy, AccessControlProxy, LoggingProxy
# ── Behavioral ──
from strategy         import SpiceCatalog, SortByScovilleDesc, BulkDiscount, SeasonalDiscount
from observer         import SpiceInventorySubject, EmailSubscriber, StockAlertObserver, PriceWatchObserver, AuditLogObserver
from command          import ShoppingCart, AddToCartCommand, RemoveFromCartCommand, ApplyDiscountCommand, CartCommandInvoker
from memento          import OrderProfile, OrderHistory
from iterator         import SpiceCatalogCollection
from chain            import OrderRequest, build_validation_chain
from state            import Order as StateOrder
from mediator         import SpiceStoreMediator
from template_method  import SalesReport, StockReport, HeatProfileReport
from visitor          import HotSauceElement, SpiceElement2, DriedPepperElement, HotSaltElement, TaxCalculatorVisitor, LabelGeneratorVisitor, CSVExportVisitor


SEP = "─" * 55

def section(title: str):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")

def sub(label: str):
    print(f"\n  {SEP}")
    print(f"  {label}")
    print(f"  {SEP}")


def demo_factory_method():
    section("1. FACTORY METHOD")
    factories = [
        SrirachaFactory(), GhostPepperSauceFactory(),
        CayennePowderFactory(), JalapenoWholePepperFactory(), PinkHimalayaSaltFactory()
    ]
    for f in factories:
        p = f.order_product()
        print(f"  → {p}")


def demo_abstract_factory():
    section("2. ABSTRACT FACTORY")
    for label, factory in [
        ("🟢 Mild",   MildPackageFactory()),
        ("🟡 Medium", MediumPackageFactory()),
        ("🔴 Inferno",InfernoPackageFactory()),
    ]:
        pkg = factory.create_package()
        print(f"\n  Pachet {label}:")
        print(f"    Sos:       {pkg['sauce']}")
        print(f"    Condiment: {pkg['spice_blend']}")
        print(f"    Ardei:     {pkg['pepper_sample']}")


def demo_builder():
    section("3. BUILDER")
    for label, builder in [
        ("Hot Lovers 🔥",   HotLoversBoxBuilder()),
        ("Gourmet 🍽️",     GourmetSpiceBoxBuilder()),
        ("Starter Kit 🌿", StarterKitBoxBuilder()),
    ]:
        box = SpiceDirector(builder).build_full_box()
        print(f"\n  {label}:\n  {box}")


def demo_prototype():
    section("4. PROTOTYPE")
    registry = SpiceProductRegistry()
    registry.register("sriracha",  SpiceProductPrototype("Sriracha Original", 39.99, "sos_iute", {"scoville": 2200}))
    registry.register("cayenne",   SpiceProductPrototype("Cayenne Pudra",     24.99, "condiment", {"scoville": 40000}))

    clone = registry.clone("sriracha")
    clone.name  = "Sriracha Extra Hot"
    clone.price = 44.99
    print(f"  Original : {registry.clone('sriracha')}")
    print(f"  Clona    : {clone}")

    shallow = registry.clone("cayenne", deep=False)
    print(f"  Shallow  : {shallow}")


def demo_singleton():
    section("5. SINGLETON")
    c1, c2 = SpiceStoreConfig(), SpiceStoreConfig()
    print(f"  c1 is c2 : {c1 is c2}")
    print(f"  Config   : {c1}")
    c1.set_setting("promotie", "Halloween -20%")
    print(f"  Setare din c2: {c2.get_setting('promotie')}")


def demo_adapter():
    section("6. ADAPTER")
    amount = 69.99
    adapters = [
        ("PayPal",  PayPalAdapter("client@ardei.ro")),
        ("Stripe",  StripeAdapter("tok_visa_4242")),
        ("Cash",    CashAdapter(100.0)),
        ("Crypto",  CryptoAdapter("1A2B3CXY", "BTC")),
    ]
    for label, adapter in adapters:
        print(f"  {label:8}: {adapter.pay(amount)}")


def demo_composite():
    section("7. COMPOSITE")
    catalog = SpiceCategory("Catalog ARDEI ROSU")
    sosuri  = SpiceCategory("Sosuri Iuti")
    sosuri.add(SpiceItem("Sriracha Original",    39.99, 2200))
    sosuri.add(SpiceItem("Ghost Pepper Inferno", 69.99, 100_000))
    condimente = SpiceCategory("Condimente")
    condimente.add(SpiceItem("Cayenne Pudra",    24.99, 40_000))
    condimente.add(SpiceItem("Amestec Cajun",    29.99,  5_000))
    catalog.add(sosuri)
    catalog.add(condimente)
    print(catalog.display())
    print(f"\n  Total catalog: {catalog.get_price():.2f} LEI")


def demo_facade():
    section("8. FACADE")
    facade = SpiceOrderFacade()
    for product, disc, gift in [
        ("Sriracha Original",     0.10, True),
        ("Ghost Pepper Inferno",  0.00, False),
        ("Carolina Reaper Pudra", 0.20, True),
    ]:
        print(f"\n  Comanda: {product}")
        print(f"    {facade.place_order(product, discount=disc, gift_wrap=gift)}")


def demo_flyweight():
    section("9. FLYWEIGHT")
    SpiceTypeFactory.clear()
    shelf = []
    data = [
        ("Sriracha Original",    39.99, 2_200,     "sos_iute",  "lichid",  "medium"),
        ("Ghost Pepper Inferno", 69.99, 100_000,   "sos_iute",  "lichid",  "inferno"),
        ("Habanero Mango Blast", 54.99, 8_000,     "sos_iute",  "lichid",  "hot"),
        ("Cayenne Pudra",        24.99, 40_000,    "condiment", "pudra",   "hot"),
        ("Amestec Cajun",        29.99, 5_000,     "condiment", "granule", "medium"),
        ("Fulgi Ardei",          19.99, 30_000,    "condiment", "fulgi",   "hot"),
        ("Jalapeno Intreg",      27.99, 8_000,     "ardei",     "intreg",  "hot"),
        ("Carolina Reaper",      79.99, 2_200_000, "ardei",     "pudra",   "inferno"),
    ]
    for name, price, shu, cat, form, heat in data:
        st = SpiceTypeFactory.get_spice_type(cat, form, heat)
        shelf.append(SpiceOnShelf(name, price, shu, st))

    for item in shelf:
        print(f"  {item.display()}")
    print(f"\n  Produse: {len(shelf)} | Tipuri flyweight: {SpiceTypeFactory.get_count()}")


def demo_decorator():
    section("10. DECORATOR")
    n = HeatWarningDecorator(EmailDecorator(SMSDecorator(BasicNotification("client@ardei.ro"))))
    print(n.send("Comanda Carolina Reaper Pudra confirmata!"))


def demo_bridge():
    section("11. BRIDGE")
    products = ["Sriracha", "Ghost Pepper", "Cayenne", "Jalapeno"]
    heat_data = [("Sriracha", 2200), ("Cayenne", 40000), ("Ghost Pepper", 100000), ("Carolina Reaper", 2_200_000)]

    print(f"\n  {ListCatalogView(PhoneDisplay(), products).show()}")
    print(f"  {ListCatalogView(WebDisplay(), products).show()}")
    from bridge import HeatScaleCatalogView, TabletDisplay
    print(f"  {HeatScaleCatalogView(TabletDisplay(), heat_data).show()}")
    print(f"  {DetailCatalogView(WebDisplay(), 'Ghost Pepper Inferno', 69.99, 100_000).show()}")


def demo_proxy():
    section("12. PROXY")
    service = RealSpiceService()

    cache_proxy = CachingProxy(service)
    print(f"  {cache_proxy.get_product_info('HS001')}")
    print(f"  {cache_proxy.get_product_info('HS001')}  (din cache)")

    access_guest = AccessControlProxy(RealSpiceService(), "guest")
    access_admin = AccessControlProxy(RealSpiceService(), "admin")
    print(f"  Guest update: {access_guest.update_price('HS001', 45.0)}")
    print(f"  Admin update: {access_admin.update_price('HS001', 45.0)}")

    log_proxy = LoggingProxy(RealSpiceService())
    log_proxy.get_product_info("HS002")
    log_proxy.update_price("SP001", 27.99)
    print(f"  Loguri: {log_proxy.logs}")


def demo_strategy():
    section("13. STRATEGY")
    products = [
        {"name": "Sriracha Original",    "price": 39.99, "scoville": 2_200},
        {"name": "Ghost Pepper Inferno", "price": 69.99, "scoville": 100_000},
        {"name": "Cayenne Pudra",        "price": 24.99, "scoville": 40_000},
        {"name": "Sweet Chili",          "price": 34.99, "scoville": 1_500},
    ]
    catalog = SpiceCatalog(products)

    catalog.set_sort_strategy(SortByScovilleDesc())
    print("  Sortat dupa iuteala (desc):")
    for p in catalog.get_sorted():
        print(f"    {p['name']:<28} {p['scoville']:>9} SHU")

    catalog.set_discount_strategy(BulkDiscount())
    total = catalog.calculate_total("Ghost Pepper Inferno", 6)
    print(f"\n  BulkDiscount (6x Ghost Pepper): {total:.2f} LEI")

    catalog.set_discount_strategy(SeasonalDiscount())
    total = catalog.calculate_total("Sriracha Original", 3)
    print(f"  SeasonalDiscount (3x Sriracha): {total:.2f} LEI")


def demo_observer():
    section("14. OBSERVER")
    subject = SpiceInventorySubject()
    email   = EmailSubscriber("fan@ardei.ro")
    stock   = StockAlertObserver(threshold=5)
    price   = PriceWatchObserver("Client VIP")
    audit   = AuditLogObserver()

    for obs in [email, stock, price, audit]:
        subject.subscribe(obs)

    subject.sell("Ghost Pepper Inferno", 8)   # scade sub 5 → alert
    subject.update_price("Sriracha Original", 44.99)
    subject.add_product("Pasta Harissa", 35.99, 20)

    print("  Email primit:")
    for m in email.received:
        print(f"    {m}")
    print("  Alerte stoc:")
    for a in stock.alerts:
        print(f"    {a}")
    print("  Price Watch:")
    for c in price.price_changes:
        print(f"    {c}")


def demo_command():
    section("15. COMMAND")
    cart     = ShoppingCart()
    invoker  = CartCommandInvoker()

    invoker.execute(AddToCartCommand(cart, "Sriracha Original", 2))
    invoker.execute(AddToCartCommand(cart, "Ghost Pepper Inferno", 1))
    invoker.execute(AddToCartCommand(cart, "Cayenne Pudra", 3))
    invoker.execute(ApplyDiscountCommand(cart, "Ghost Pepper Inferno", 0.10))

    print(cart.display())

    print(f"\n  Undo: {invoker.undo()}")
    print(f"  Undo: {invoker.undo()}")
    print(f"  Redo: {invoker.redo()}")
    print(f"\n  Istoric: {invoker.history()}")


def demo_memento():
    section("16. MEMENTO")
    profile = OrderProfile()
    history = OrderHistory()

    profile.add_item("Sriracha Original", 2)
    profile.set_discount(0.10)
    profile.set_note("Comanda saptamanala")
    history.save(profile, "v1 - initial")
    print(f"  Stare v1: {profile.display()}")

    profile.add_item("Ghost Pepper Inferno", 1)
    profile.set_discount(0.20)
    history.save(profile, "v2 - cu ghost pepper")
    print(f"  Stare v2: {profile.display()}")

    history.restore(profile, index=0)
    print(f"  Restaurat: {profile.display()}")
    print(f"  Snapshots: {history.list_snapshots()}")


def demo_iterator():
    section("17. ITERATOR")
    col = SpiceCatalogCollection()

    sub("Toate produsele:")
    it = col.all_iterator()
    while it.has_next():
        p = it.next()
        print(f"    {p['name']:<30} {p['price']:>7.2f} LEI | {p['scoville']:>9} SHU")

    sub("Doar sosuri iuti:")
    it = col.category_iterator("sos_iute")
    while it.has_next():
        p = it.next()
        print(f"    {p['name']}")

    sub("Produse 5.000-50.000 SHU:")
    it = col.heat_range_iterator(5_000, 50_000)
    while it.has_next():
        p = it.next()
        print(f"    {p['name']} ({p['scoville']} SHU)")

    sub("Buget max 25 LEI:")
    it = col.budget_iterator(25.0)
    while it.has_next():
        p = it.next()
        print(f"    {p['name']} — {p['price']:.2f} LEI")


def demo_chain():
    section("18. CHAIN OF RESPONSIBILITY")
    stock = {
        "Ghost Pepper Inferno":   10,
        "Carolina Reaper Pudra":   8,
        "Sriracha Original":      30,
    }
    chain = build_validation_chain(stock)

    requests = [
        OrderRequest("Sriracha Original",     2, 25, 200.0, 2_200,     39.99),
        OrderRequest("Carolina Reaper Pudra", 1, 16, 200.0, 2_200_000, 79.99),  # varsta
        OrderRequest("Ghost Pepper Inferno",  1, 30, 10.0,  100_000,   69.99),  # buget
        OrderRequest("Ghost Pepper Inferno",  1, 30, 500.0, 100_000,   69.99),  # ok + warning
    ]
    for req in requests:
        result = chain.handle(req)
        print(f"\n  {req.product} | varsta {req.customer_age} | buget {req.budget:.0f} LEI")
        print(f"  → {result}")
        if req.notes:
            for n in req.notes:
                print(f"    • {n}")


def demo_state():
    section("19. STATE")
    order = StateOrder("ORD-001", "Ghost Pepper Inferno x2", 139.98)
    print(f"  {order}")
    print(f"  → {order.confirm()}")
    print(f"  → {order.prepare()}")
    print(f"  → {order.ship()}")
    print(f"  → {order.deliver()}")
    print(f"  Stare finala: {order.get_state_name()}")

    order2 = StateOrder("ORD-002", "Sriracha Original x1", 39.99)
    print(f"\n  {order2}")
    print(f"  → {order2.confirm()}")
    print(f"  → {order2.cancel()}")
    print(f"  → {order2.ship()}")  # nu e permis


def demo_mediator():
    section("20. MEDIATOR")
    mediator = SpiceStoreMediator()
    mediator.setup()

    mediator.inventory.sell("Ghost Pepper Inferno", 8)
    mediator.inventory.restock("Ghost Pepper Inferno", 50)
    mediator.pricing.update_price("Sriracha Original", 44.99)

    print("  Notificari trimise:")
    for msg in mediator.notification.sent:
        print(f"    {msg}")
    print(f"\n  {mediator.analytics.summary()}")


def demo_template_method():
    section("21. TEMPLATE METHOD")
    sales = [
        {"product": "Sriracha Original",    "qty": 15, "total": 599.85},
        {"product": "Ghost Pepper Inferno", "qty":  5, "total": 349.95},
        {"product": "Cayenne Pudra",        "qty": 20, "total": 499.80},
    ]
    print(SalesReport(sales).generate())

    print()
    stock = {"Sriracha Original": 30, "Ghost Pepper Inferno": 3, "Cayenne Pudra": 40}
    print(StockReport(stock).generate())

    print()
    products = [
        {"name": "Sweet Chili", "scoville": 1_500},
        {"name": "Sriracha",    "scoville": 2_200},
        {"name": "Cayenne",     "scoville": 40_000},
        {"name": "Ghost Pepper","scoville": 100_000},
        {"name": "Carolina Reaper","scoville": 2_200_000},
    ]
    print(HeatProfileReport(products).generate())


def demo_visitor():
    section("22. VISITOR")
    elements = [
        HotSauceElement("Sriracha Original",    39.99, 2_200,     250),
        SpiceElement2("Cayenne Pudra",          24.99, 40_000,    100),
        DriedPepperElement("Jalapeno Intreg",   27.99, 8_000,     True),
        HotSaltElement("Sare Roz cu Chili",     18.99, 5_000,     150),
        HotSauceElement("Ghost Pepper Inferno", 69.99, 100_000,   100),
    ]

    for visitor, label in [
        (TaxCalculatorVisitor(),  "Calcul taxe"),
        (LabelGeneratorVisitor(), "Etichete"),
        (CSVExportVisitor(),      "Export CSV"),
    ]:
        sub(label)
        for el in elements:
            print(f"  {el.accept(visitor)}")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

def main():
    print("\n" + "=" * 55)
    print("  ARDEI ROSU — 20 Design Patterns Demo")
    print("=" * 55)

    demo_factory_method()
    demo_abstract_factory()
    demo_builder()
    demo_prototype()
    demo_singleton()
    demo_adapter()
    demo_composite()
    demo_facade()
    demo_flyweight()
    demo_decorator()
    demo_bridge()
    demo_proxy()
    demo_strategy()
    demo_observer()
    demo_command()
    demo_memento()
    demo_iterator()
    demo_chain()
    demo_state()
    demo_mediator()
    demo_template_method()
    demo_visitor()

    print("\n" + "=" * 55)
    print("  Demo complet! 22 pattern-uri demonstrate.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
