from flyweight import HotPepperTypeFactory, ProductOnShelf
from decorator import BasicNotification, EmailDecorator, SMSDecorator, PushDecorator, SpicyPackDecorator
from bridge import PhoneDisplay, TabletDisplay, WebDisplay, ListCatalogView, GridCatalogView, DetailCatalogView
from proxy import RealProductService, CachingProxy, AccessControlProxy, LoggingProxy


def pause():
    input("\n  🔥 Apasa ENTER pentru a continua...")


def citeste_float(prompt, error_msg="Valoare invalida. Introduceti un numar."):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print(f"  {error_msg}")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                return None


def citeste_int(prompt, error_msg="Valoare invalida. Introduceti un numar intreg."):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print(f"  {error_msg}")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                return None


def alege_optiune(prompt, optiuni_valide, error_msg="Optiune invalida."):
    while True:
        choice = input(prompt).strip()
        if choice in optiuni_valide:
            return choice
        print(f"  {error_msg} Optiuni valide: {', '.join(optiuni_valide)}")
        retry = input("  Incercati din nou? (d/n): ").strip().lower()
        if retry != "d":
            return None


def header(title):
    print(f"\n{'='*60}")
    print(f"  🌶️ {title}")
    print(f"{'='*60}")


HotPepperTypeFactory.clear()
shelf = []
products_data = [
    ("Ardei iute Jalapeno", 15.99, "Ardei iute", "Mild", "Mexic"),
    ("Ardei iute Serrano", 19.99, "Ardei iute", "Mediu", "Mexic"),
    ("Ardei iute Habanero", 29.99, "Ardei iute", "Picant", "Caraibe"),
    ("Ardei iute Ghost Pepper", 49.99, "Ardei iute", "Extra-Picant", "India"),
    ("Sos iute Sriracha", 24.99, "Sos iute", "Mediu", "Tailanda"),
    ("Sos iute Tabasco", 22.99, "Sos iute", "Picant", "SUA"),
    ("Sos iute Carolina Reaper", 59.99, "Sos iute", "Inferno", "SUA"),
    ("Pasta iute Gochujang", 34.99, "Pasta iute", "Mediu", "Coreea"),
    ("Pasta iute Harissa", 29.99, "Pasta iute", "Picant", "Tunisia"),
    ("Usturoi iute fermentat", 39.99, "Condiment iute", "Picant", "Romania"),
]
for name, price, cat, heat, origin in products_data:
    pepper_type = HotPepperTypeFactory.get_pepper_type(cat, heat, origin)
    shelf.append(ProductOnShelf(name, price, pepper_type))

real_service = RealProductService()
caching_proxy = CachingProxy(RealProductService())
logging_proxy = LoggingProxy(RealProductService())


def flyweight_display():
    header("FLYWEIGHT - Raft cu produse iuti")
    if not shelf:
        print("  Raftul este gol.")
    else:
        for product in shelf:
            print(f"  {product.display()}")
        print(f"\n  Total produse: {len(shelf)}")
        print(f"  Tipuri unice (flyweight): {HotPepperTypeFactory.get_count()}")
    pause()


def flyweight_add():
    header("FLYWEIGHT - Adauga produs iute")
    name = input("  Nume produs: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    price = citeste_float("  Pret (LEI): ")
    if price is None:
        return

    print("  Categorie produs:")
    print("    [1] Ardei iute")
    print("    [2] Sos iute")
    print("    [3] Pasta iute")
    print("    [4] Condiment iute")
    cat_choice = alege_optiune("  Alegeti [1/2/3/4]: ", ["1", "2", "3", "4"])
    if cat_choice is None:
        return
    cat_map = {"1": "Ardei iute", "2": "Sos iute", "3": "Pasta iute", "4": "Condiment iute"}
    category = cat_map[cat_choice]

    print("\n  Nivel iuteala (Scoville):")
    print("    [1] Mild (usor iute)")
    print("    [2] Mediu")
    print("    [3] Picant")
    print("    [4] Extra-Picant")
    print("    [5] Inferno (foarte iute)")
    heat_choice = alege_optiune("  Alegeti [1/2/3/4/5]: ", ["1", "2", "3", "4", "5"])
    if heat_choice is None:
        return
    heat_map = {"1": "Mild", "2": "Mediu", "3": "Picant", "4": "Extra-Picant", "5": "Inferno"}
    heat_level = heat_map[heat_choice]

    origin = input("  Origine (ex: Romania, Mexic, India): ").strip()
    if not origin:
        origin = "Necunoscuta"

    pepper_type = HotPepperTypeFactory.get_pepper_type(category, heat_level, origin)
    shelf.append(ProductOnShelf(name, price, pepper_type))
    print(f"\n  ✅ Adaugat: {name} - {price:.2f} LEI {pepper_type}")
    print(f"  Tipuri unice acum: {HotPepperTypeFactory.get_count()}")
    pause()


def flyweight_stats():
    header("FLYWEIGHT - Statistici eficienta")
    print(f"  Total produse pe raft: {len(shelf)}")
    print(f"  Tipuri unice partajate: {HotPepperTypeFactory.get_count()}")
    saved_memory = len(shelf) - HotPepperTypeFactory.get_count()
    if saved_memory >= 0:
        print(f"  💾 Memorie salvata: {saved_memory} obiecte tip reutilizate")
    pause()


def decorator_notify():
    header("DECORATOR - Notificare iute")
    recipient = input("  Destinatar (email/telefon): ").strip()
    if not recipient:
        print("  Destinatarul nu poate fi gol.")
        pause()
        return

    message = input("  Mesaj (ex: 'Stoc nou de ardei iuti!'): ").strip()
    if not message:
        message = "🔥 Produse noi iuti in stoc la ARDEIROSU!"

    print("\n  Selectati canalele (mai multe separate prin virgula):")
    print("    [1] Email")
    print("    [2] SMS")
    print("    [3] Push")
    print("    [4] Pachet gratuit ardei iuti")
    choices_str = input("  Alegeti: ").strip()
    choices = [c.strip() for c in choices_str.split(",")]

    notification = BasicNotification(recipient)
    for c in choices:
        if c == "1":
            notification = EmailDecorator(notification)
        elif c == "2":
            notification = SMSDecorator(notification)
        elif c == "3":
            notification = PushDecorator(notification)
        elif c == "4":
            notification = SpicyPackDecorator(notification)
        else:
            print(f"  Canal '{c}' ignorat (invalid).")

    print(f"\n  {notification.send(message)}")
    pause()


def bridge_display():
    header("BRIDGE - Catalog iute pe dispozitiv")
    print("\n  Alege dispozitivul:")
    print("    [1] Telefon")
    print("    [2] Tableta")
    print("    [3] Web")
    dev_choice = alege_optiune("  Alegeti [1/2/3]: ", ["1", "2", "3"])
    if dev_choice is None:
        return

    print("\n  Alege tipul vizualizare:")
    print("    [1] Lista")
    print("    [2] Grid")
    print("    [3] Detaliu")
    view_choice = alege_optiune("  Alegeti [1/2/3]: ", ["1", "2", "3"])
    if view_choice is None:
        return

    devices = {"1": PhoneDisplay(), "2": TabletDisplay(), "3": WebDisplay()}
    device = devices[dev_choice]

    product_names = [p.name for p in shelf[:8]]

    if view_choice == "1":
        view = ListCatalogView(device, product_names)
    elif view_choice == "2":
        view = GridCatalogView(device, product_names)
    elif view_choice == "3":
        name = input("  Nume produs pentru detaliu: ").strip()
        price_val = 0.0
        heat_val = ""
        for p in shelf:
            if p.name.lower() == name.lower():
                price_val = p.price
                heat_val = p.pepper_type.heat_level
                name = p.name
                break
        view = DetailCatalogView(device, name, price_val, heat_val)

    print(f"\n  {view.show()}")
    pause()


def proxy_caching():
    header("PROXY - Caching (optimizare interogari)")
    print("\n  🔥 ID-uri disponibile: HP001, HP002, HP003, SS001, PA001, US001")
    print("     HP001 - Ardei iute Habanero")
    print("     HP002 - Ardei iute Carolina Reaper (INFERNO)")
    print("     SS001 - Sos iute Ghost Pepper")
    product_id = input("  Introduceti ID produs: ").strip().upper()
    if not product_id:
        print("  ID-ul nu poate fi gol.")
        pause()
        return

    print(f"\n  📡 Prima cerere: {caching_proxy.get_product_info(product_id)}")
    print(f"  ⚡ A doua cerere (din cache): {caching_proxy.get_product_info(product_id)}")
    pause()


def proxy_access():
    header("PROXY - Access Control (securitate)")
    print("\n  Alege rolul:")
    print("    [1] Guest (oaspete - doar citire)")
    print("    [2] Admin (administrator - modificari)")
    role_choice = alege_optiune("  Alegeti [1/2]: ", ["1", "2"])
    if role_choice is None:
        return
    role = "admin" if role_choice == "2" else "guest"

    proxy = AccessControlProxy(RealProductService(), role)

    print(f"\n  👤 Rol: {role}")
    print(f"  📖 Citire HP001: {proxy.get_product_info('HP001')}")

    new_price = citeste_float("  💰 Pret nou pentru HP001 (LEI): ")
    if new_price is None:
        return
    print(f"  ✏️ Modificare pret: {proxy.update_price('HP001', new_price)}")
    pause()


def proxy_logging():
    header("PROXY - Logging (audit operatii)")
    print("\n  🔥 ID-uri disponibile: HP001, HP002, HP003, SS001, PA001, US001")
    product_id = input("  Introduceti ID produs: ").strip().upper()
    if not product_id:
        print("  ID-ul nu poate fi gol.")
        pause()
        return

    result = logging_proxy.get_product_info(product_id)
    print(f"  📋 Rezultat: {result}")
    print(f"  📝 Loguri acumulate: {logging_proxy.logs}")
    pause()


def show_menu():
    print()
    print("=" * 60)
    print("  🌶️🌶️🌶️  ARDEIROSU - Magazin de ardei iuti si sosuri picante  🌶️🌶️🌶️")
    print("=" * 60)
    print("  🏗️ Patternuri: Flyweight | Decorator | Bridge | Proxy")
    print("-" * 60)
    print("    [1] Flyweight - Afiseaza raftul cu produse iuti")
    print("    [2] Flyweight - Adauga produs iute")
    print("    [3] Flyweight - Statistici economie memorie")
    print("    [4] Decorator - Trimite notificare iute")
    print("    [5] Bridge - Afiseaza catalog pe dispozitiv")
    print("    [6] Proxy - Caching (optimizare)")
    print("    [7] Proxy - Access Control (securitate)")
    print("    [8] Proxy - Logging (audit)")
    print("    [0] Iesire din ARDEIROSU")
    print("-" * 60)


def main():
    print("\n" + "=" * 60)
    print("  🌶️🌶️🌶️  BUN VENIT LA ARDEIROSU!  🌶️🌶️🌶️")
    print("  Magazin specializat in ardei iuti, sosuri picante")
    print("  si derivate incendiare!")
    print("=" * 60)

    while True:
        show_menu()
        choice = input("  🔥 Optiunea: ").strip()

        if choice == "1":
            flyweight_display()
        elif choice == "2":
            flyweight_add()
        elif choice == "3":
            flyweight_stats()
        elif choice == "4":
            decorator_notify()
        elif choice == "5":
            bridge_display()
        elif choice == "6":
            proxy_caching()
        elif choice == "7":
            proxy_access()
        elif choice == "8":
            proxy_logging()
        elif choice == "0":
            print("\n  🔥 La revedere! Nu uita: viața e ca ardeiul iute -")
            print("  cu cat e mai picanta, cu atat e mai interesanta! 🌶️\n")
            break
        else:
            print("  Optiune invalida.")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                print("\n  La revedere! 🌶️\n")
                break


if __name__ == "__main__":
    main()