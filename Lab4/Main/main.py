# main.py
from Lab4.Adapter.adapter import PayPalAdapter, StripeAdapter, CashAdapter
from Lab4.Composite.composite import HotSauceItem, SauceCategory
from Lab4.Facade.facade import OrderFacade


def pause():
    input("\n  Apasa ENTER pentru a continua...")


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
    print(f"  {title}")
    print(f"{'='*60}")


catalog = SauceCategory("Catalog ARDEIROSU")

sosuri_iuti = SauceCategory("Sosuri iuti")
sosuri_iuti.add(HotSauceItem("Sos Habanero Extreme", 34.99))
sosuri_iuti.add(HotSauceItem("Sos Carolina Reaper", 49.99))
sosuri_iuti.add(HotSauceItem("Sos Ghost Pepper", 44.99))
sosuri_iuti.add(HotSauceItem("Sos Jalapeno Classic", 24.99))

ardei_uscat = SauceCategory("Ardei uscati si condimente")
ardei_uscat.add(HotSauceItem("Ardei iuti uscati", 19.99))
ardei_uscat.add(HotSauceItem("Pudra de ardei iute", 15.99))
ardei_uscat.add(HotSauceItem("Fulgi de ardei iute", 12.99))
ardei_uscat.add(HotSauceItem("Sare cu ardei iute", 9.99))

set_cadou = SauceCategory("Seturi cadou")
set_cadou.add(HotSauceItem("Set 3 sosuri iuti", 99.99))
set_cadou.add(HotSauceItem("Set Deluxe 5 sosuri", 159.99))
set_cadou.add(HotSauceItem("Set condimente extreme", 49.99))

catalog.add(sosuri_iuti)
catalog.add(ardei_uscat)
catalog.add(set_cadou)


def adapter_paypal():
    header("ADAPTER - Plata PayPal")
    email = input("  Email PayPal: ").strip()
    if not email:
        print("  Email-ul nu poate fi gol.")
        pause()
        return

    amount = citeste_float("  Suma de plata (LEI): ")
    if amount is None:
        return

    adapter = PayPalAdapter(email)
    print(f"\n  {adapter.pay(amount)}")
    pause()


def adapter_stripe():
    header("ADAPTER - Plata Stripe")
    token = input("  Token Stripe (ex: tok_visa_4242): ").strip()
    if not token:
        print("  Token-ul nu poate fi gol.")
        pause()
        return

    amount = citeste_float("  Suma de plata (LEI): ")
    if amount is None:
        return

    adapter = StripeAdapter(token)
    print(f"\n  {adapter.pay(amount)}")
    pause()


def adapter_cash():
    header("ADAPTER - Plata Cash")
    amount = citeste_float("  Suma de plata (LEI): ")
    if amount is None:
        return

    received = citeste_float("  Suma primita (LEI): ")
    if received is None:
        return

    adapter = CashAdapter(received)
    print(f"\n  {adapter.pay(amount)}")
    pause()


def composite_display():
    header("COMPOSITE - Catalog complet Ardeirosu")
    print(catalog.display())
    pause()


def composite_add():
    header("COMPOSITE - Adauga produs nou")
    categories = []
    for child in catalog.get_children():
        if isinstance(child, SauceCategory):
            categories.append(child)

    if not categories:
        print("  Nu exista categorii.")
        pause()
        return

    print("\n  Categorii disponibile:")
    for i, cat in enumerate(categories, 1):
        print(f"    [{i}] {cat.name}")

    idx = citeste_int("\n  Alege categoria (numar): ")
    if idx is None:
        return

    while idx < 1 or idx > len(categories):
        print(f"  Index invalid. Alegeti intre 1 si {len(categories)}.")
        retry = input("  Incercati din nou? (d/n): ").strip().lower()
        if retry != "d":
            return
        idx = citeste_int("\n  Alege categoria (numar): ")
        if idx is None:
            return

    name = input("  Nume produs: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    price = citeste_float("  Pret (LEI): ")
    if price is None:
        return

    categories[idx - 1].add(HotSauceItem(name, price))
    print(f"\n  Adaugat '{name}' in '{categories[idx - 1].name}'")
    pause()


def composite_total():
    header("COMPOSITE - Pret total catalog Ardeirosu")
    print(f"\n  Pret total catalog: {catalog.get_price():.2f} LEI\n")
    for child in catalog.get_children():
        if isinstance(child, SauceCategory):
            print(f"    {child.name}: {child.get_price():.2f} LEI")
    pause()


def facade_order():
    header("FACADE - Comanda rapida Ardeirosu")
    facade = OrderFacade()
    products = ["Sos Habanero Extreme", "Sos Carolina Reaper", "Sos Ghost Pepper",
                "Ardei iuti uscati", "Pudra de ardei iute", "Set 3 sosuri iuti"]

    print("\n  Produse disponibile:")
    for i, p in enumerate(products, 1):
        print(f"    [{i}] {p}")

    print("\n  Alegeti produsul (numar sau scrieti numele):")
    custom = input("  Alegeti: ").strip()
    try:
        idx = int(custom) - 1
        if 0 <= idx < len(products):
            product_name = products[idx]
        else:
            print(f"  Index invalid.")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                return
            product_name = input("  Scrieti numele produsului: ").strip()
    except ValueError:
        product_name = custom

    disc = citeste_float("  Reducere % (0 pentru fara): ")
    if disc is None:
        return
    disc = disc / 100

    print("  Ambalare cadou?")
    print("    [1] Da (cutie speciala Ardeirosu + trusa de iuteala)")
    print("    [2] Nu")
    gift_choice = alege_optiune("  Alegeti [1/2]: ", ["1", "2"])
    if gift_choice is None:
        return
    gift = gift_choice == "1"

    result = facade.place_order(product_name, discount=disc, gift_pack=gift)
    print(f"\n  {result}")
    pause()


def show_menu():
    print()
    print("=" * 60)
    print("  ARDEIROSU - Magazin de sosuri iuti si condimente")
    print("  Lab 4: Adapter, Composite, Facade")
    print("=" * 60)
    print("    [1] Adapter - Plata cu PayPal")
    print("    [2] Adapter - Plata cu Stripe")
    print("    [3] Adapter - Plata Cash")
    print("    [4] Composite - Afiseaza catalog complet")
    print("    [5] Composite - Adauga produs in catalog")
    print("    [6] Composite - Pret total catalog")
    print("    [7] Facade - Plaseaza comanda rapida")
    print("    [0] Iesire")
    print("-" * 60)


def main():
    while True:
        show_menu()
        choice = input("  Optiunea: ").strip()

        if choice == "1":
            adapter_paypal()
        elif choice == "2":
            adapter_stripe()
        elif choice == "3":
            adapter_cash()
        elif choice == "4":
            composite_display()
        elif choice == "5":
            composite_add()
        elif choice == "6":
            composite_total()
        elif choice == "7":
            facade_order()
        elif choice == "0":
            print("\n  La revedere! Va asteptam la Ardeirosu pentru iuteala!\n")
            break
        else:
            print("  Optiune invalida.")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                print("\n  La revedere!\n")
                break


if __name__ == "__main__":
    main()