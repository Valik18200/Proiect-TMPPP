# main.py
from Lab6.Strategy.strategy import SauceCatalog, SortByPrice, SortByPriceDesc, SortByName, SortByScoville, SortByScovilleDesc
from Lab6.Observer.observer import HotSauceStore, EmailSubscriber, SMSSubscriber, DashboardLogger
from Lab6.Command.command import Inventory, AddStockCommand, RemoveStockCommand, UpdatePriceCommand, CommandHistory
from Lab6.Memento.memento import ShoppingCart, CartHistory
from Lab6.Iterator.iterator import HotSauce, SauceCollection


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


# ========== INITIALIZARE DATE ==========
catalog = SauceCatalog()
catalog.add_sauce("Sos Habanero Extreme", 34.99, 350000)
catalog.add_sauce("Sos Carolina Reaper", 49.99, 2200000)
catalog.add_sauce("Sos Ghost Pepper", 44.99, 1000000)
catalog.add_sauce("Sos Jalapeno Classic", 24.99, 5000)
catalog.add_sauce("Sos Scorpion Blood", 59.99, 1500000)
catalog.add_sauce("Pudra Carolina Reaper", 29.99, 1600000)

store = HotSauceStore()
email_sub = EmailSubscriber("iute@ardeirosu.ro")
sms_sub = SMSSubscriber("+37369123456")
dashboard = DashboardLogger()
store.attach(email_sub)
store.attach(sms_sub)
store.attach(dashboard)

inv = Inventory()
inv.add("Sos Habanero Extreme", 15)
inv.add("Sos Carolina Reaper", 8)
inv.add("Sos Ghost Pepper", 12)
inv.add("Sos Jalapeno Classic", 20)
inv.add("Pudra Carolina Reaper", 10)

prices = {
    "Sos Habanero Extreme": 34.99,
    "Sos Carolina Reaper": 49.99,
    "Sos Ghost Pepper": 44.99,
    "Sos Jalapeno Classic": 24.99,
    "Pudra Carolina Reaper": 29.99,
}
cmd_history = CommandHistory()

cart = ShoppingCart()
cart_history = CartHistory()

collection = SauceCollection()
collection.add(HotSauce("Sos Habanero Extreme", 34.99, "Sos iute", 350000))
collection.add(HotSauce("Sos Carolina Reaper", 49.99, "Sos iute", 2200000))
collection.add(HotSauce("Sos Ghost Pepper", 44.99, "Sos iute", 1000000))
collection.add(HotSauce("Sos Jalapeno Classic", 24.99, "Sos iute", 5000))
collection.add(HotSauce("Pudra Carolina Reaper", 29.99, "Condiment", 1600000))
collection.add(HotSauce("Ardei iuti uscati", 19.99, "Ardei uscati", 50000))
collection.add(HotSauce("Set Deluxe 3 sosuri", 99.99, "Set cadou", 0))
collection.add(HotSauce("Set Extreme 5 sosuri", 159.99, "Set cadou", 0))


# ========== FUNCTII MENIU ==========
def strategy_sort():
    header("STRATEGY - Sorteaza catalog Ardeirosu")
    print("\n  Strategie de sortare:")
    print("    [1] Dupa pret (crescator)")
    print("    [2] Dupa pret (descrescator)")
    print("    [3] Dupa nume (A-Z)")
    print("    [4] Dupa Scoville (crescator - mai putin iute)")
    print("    [5] Dupa Scoville (descrescator - cel mai iute)")
    choice = alege_optiune("  Alegeti [1/2/3/4/5]: ", ["1", "2", "3", "4", "5"])
    if choice is None:
        return

    strategies = {
        "1": SortByPrice(),
        "2": SortByPriceDesc(),
        "3": SortByName(),
        "4": SortByScoville(),
        "5": SortByScovilleDesc(),
    }
    catalog.set_sort_strategy(strategies[choice])
    print(catalog.display())
    pause()


def strategy_add():
    header("STRATEGY - Adauga sos nou in catalog")
    name = input("  Nume sos/condiment: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    price = citeste_float("  Pret (LEI): ")
    if price is None:
        return

    scoville = citeste_int("  Scoville (SHU - unitati iuteala): ")
    if scoville is None:
        return

    catalog.add_sauce(name, price, scoville)
    print(f"\n  🌶️ Adaugat: {name} - {price:.2f} LEI (Scoville: {scoville:,} SHU)")
    pause()


def observer_new():
    header("OBSERVER - Produs nou la Ardeirosu")
    name = input("  Nume produs nou: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    price = citeste_float("  Pret (LEI): ")
    if price is None:
        return

    scoville = citeste_int("  Scoville (SHU): ")
    if scoville is None:
        return

    store.new_product(name, price, scoville)
    print("  🔥 Notificare trimisa catre toti iubitorii de iuteala!")
    pause()


def observer_price_drop():
    header("OBSERVER - Reducere pret sos")
    name = input("  Nume produs: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    old = citeste_float("  Pret vechi (LEI): ")
    if old is None:
        return

    new = citeste_float("  Pret nou (LEI): ")
    if new is None:
        return

    store.price_drop(name, old, new)
    print("  🔥 Oferta anuntata tuturor clientilor!")
    pause()


def observer_back_in_stock():
    header("OBSERVER - Produs revenit in stoc")
    name = input("  Nume produs: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    store.back_in_stock(name)
    print("  ✅ Notificare trimisa clientilor care asteptau.")
    pause()


def observer_spicy_challenge():
    header("OBSERVER - Provocare iuteala extrema")
    name = input("  Nume produs provocare: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    scoville = citeste_int("  Scoville (SHU): ")
    if scoville is None:
        return

    store.spicy_challenge(name, scoville)
    print("  ⚠️ Provocarea a fost lansata! Clientii sunt avertizati!")
    pause()


def observer_view():
    header("OBSERVER - Notificari Ardeirosu")
    print("\n  📧 Mesaje Email (iute@ardeirosu.ro):")
    for msg in email_sub.messages[-5:]:
        print(f"    {msg}")

    print(f"\n  📱 Mesaje SMS ({sms_sub.phone}):")
    for msg in sms_sub.messages[-5:]:
        print(f"    {msg}")

    print(f"\n  📊 Dashboard: {len(dashboard.log)} evenimente inregistrate")
    pause()


def command_add():
    header("COMMAND - Adauga stoc Ardeirosu")
    sauce = input("  Nume produs: ").strip()
    if not sauce:
        print("  Numele nu poate fi gol.")
        pause()
        return

    qty = citeste_int("  Cantitate: ")
    if qty is None:
        return

    cmd = AddStockCommand(inv, sauce, qty)
    result = cmd_history.execute(cmd)
    print(f"  {result}")
    print(f"  📦 Stoc: {inv}")
    pause()


def command_remove():
    header("COMMAND - Scoate din stoc")
    sauce = input("  Nume produs: ").strip()
    if not sauce:
        print("  Numele nu poate fi gol.")
        pause()
        return

    qty = citeste_int("  Cantitate: ")
    if qty is None:
        return

    cmd = RemoveStockCommand(inv, sauce, qty)
    result = cmd_history.execute(cmd)
    print(f"  {result}")
    print(f"  📦 Stoc: {inv}")
    pause()


def command_price():
    header("COMMAND - Actualizeaza pret")
    sauce = input("  Nume produs: ").strip()
    if not sauce:
        print("  Numele nu poate fi gol.")
        pause()
        return

    new_price = citeste_float("  Pret nou (LEI): ")
    if new_price is None:
        return

    cmd = UpdatePriceCommand(prices, sauce, new_price)
    result = cmd_history.execute(cmd)
    print(f"  {result}")
    print(f"  💰 Preturi: {prices}")
    pause()


def command_undo_redo():
    header("COMMAND - Undo/Redo")
    print("    [1] Undo")
    print("    [2] Redo")
    choice = alege_optiune("  Alegeti [1/2]: ", ["1", "2"])
    if choice is None:
        return

    if choice == "1":
        print(f"  {cmd_history.undo()}")
    elif choice == "2":
        print(f"  {cmd_history.redo()}")

    print(f"  📦 Stoc: {inv}")
    print(f"  💰 Preturi: {prices}")
    pause()


def memento_add():
    header("MEMENTO - Adauga in cos Ardeirosu")
    name = input("  Nume produs: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    price = citeste_float("  Pret (LEI): ")
    if price is None:
        return

    scoville = citeste_int("  Scoville (SHU): ")
    if scoville is None:
        return

    cart.add_item(name, price, scoville)
    print(f"  🌶️ Adaugat in cos: {name} - {price:.2f} LEI ({scoville:,} SHU)")
    pause()


def memento_save():
    header("MEMENTO - Salveaza cos")
    cart_history.save(cart.save())
    snapshots = cart_history.list_snapshots()
    print(f"  💾 Cos salvat! Total snapshots: {len(snapshots)}")
    pause()


def memento_restore():
    header("MEMENTO - Restaureaza cos")
    snapshots = cart_history.list_snapshots()
    if not snapshots:
        print("  Nu exista snapshots salvate.")
        pause()
        return

    print("\n  Snapshots disponibile:")
    for s in snapshots:
        print(f"    {s}")

    idx = citeste_int("  Index snapshot: ")
    if idx is None:
        return

    try:
        cart.restore(cart_history.get_snapshot(idx))
        print(f"  🛒 Cos restaurat din snapshot #{idx}")
        print(cart)
    except (ValueError, IndexError):
        print("  Index invalid.")
        retry = input("  Incercati din nou? (d/n): ").strip().lower()
        if retry == "d":
            memento_restore()
    pause()


def memento_view():
    header("MEMENTO - Vizualizeaza cos")
    print(cart)
    pause()


def iterator_all():
    header("ITERATOR - Toate produsele Ardeirosu")
    for sauce in collection.iterator():
        print(f"    {sauce}")
    pause()


def iterator_category():
    header("ITERATOR - Filtru categorie")
    print("  Categorii: Sos iute, Condiment, Ardei uscati, Set cadou")
    category = input("  Categorie: ").strip()
    if not category:
        print("  Categoria nu poate fi goala.")
        pause()
        return

    print(f"\n  🌶️ Produse din categoria '{category}':")
    found = False
    for sauce in collection.category_iterator(category):
        print(f"    {sauce}")
        found = True
    if not found:
        print("    Niciun rezultat.")
    pause()


def iterator_price():
    header("ITERATOR - Filtru pret")
    min_p = citeste_float("  Pret minim (LEI): ")
    if min_p is None:
        return

    max_p = citeste_float("  Pret maxim (LEI): ")
    if max_p is None:
        return

    print(f"\n  Produse intre {min_p:.2f} - {max_p:.2f} LEI:")
    found = False
    for sauce in collection.price_range_iterator(min_p, max_p):
        print(f"    {sauce}")
        found = True
    if not found:
        print("    Niciun rezultat.")
    pause()


def iterator_scoville():
    header("ITERATOR - Filtru Scoville (iuteala)")
    min_s = citeste_int("  Scoville minim (SHU): ")
    if min_s is None:
        return

    max_s = citeste_int("  Scoville maxim (SHU): ")
    if max_s is None:
        return

    print(f"\n  Produse intre {min_s:,} - {max_s:,} SHU:")
    found = False
    for sauce in collection.scoville_range_iterator(min_s, max_s):
        print(f"    {sauce}")
        found = True
    if not found:
        print("    Niciun rezultat.")
    pause()


def iterator_extreme():
    header("ITERATOR - Produse extreme (peste 100.000 SHU)")
    print("\n  🔥 Cele mai iuti produse Ardeirosu:")
    for sauce in collection.extreme_iterator():
        print(f"    {sauce}")
    pause()


def show_menu():
    print()
    print("=" * 60)
    print("  🔥 ARDEIROSU - Magazin de sosuri iuti si condimente 🔥")
    print("  Lab 6: Strategy, Observer, Command, Memento, Iterator")
    print("=" * 60)
    print("    [1]  Strategy - Sorteaza catalog")
    print("    [2]  Strategy - Adauga produs in catalog")
    print("    [3]  Observer - Produs nou")
    print("    [4]  Observer - Reducere pret")
    print("    [5]  Observer - Produs revenit in stoc")
    print("    [6]  Observer - Provocare iuteala extrema")
    print("    [7]  Observer - Vizualizeaza notificari")
    print("    [8]  Command - Adauga stoc")
    print("    [9]  Command - Scoate din stoc")
    print("    [10] Command - Actualizeaza pret")
    print("    [11] Command - Undo / Redo")
    print("    [12] Memento - Adauga in cos")
    print("    [13] Memento - Salveaza cos")
    print("    [14] Memento - Restaureaza cos")
    print("    [15] Memento - Vizualizeaza cos")
    print("    [16] Iterator - Toate produsele")
    print("    [17] Iterator - Filtru categorie")
    print("    [18] Iterator - Filtru pret")
    print("    [19] Iterator - Filtru Scoville (iuteala)")
    print("    [20] Iterator - Produse extreme")
    print("    [0]  Iesire")
    print("-" * 60)


def main():
    while True:
        show_menu()
        choice = input("  Optiunea: ").strip()

        if choice == "1":
            strategy_sort()
        elif choice == "2":
            strategy_add()
        elif choice == "3":
            observer_new()
        elif choice == "4":
            observer_price_drop()
        elif choice == "5":
            observer_back_in_stock()
        elif choice == "6":
            observer_spicy_challenge()
        elif choice == "7":
            observer_view()
        elif choice == "8":
            command_add()
        elif choice == "9":
            command_remove()
        elif choice == "10":
            command_price()
        elif choice == "11":
            command_undo_redo()
        elif choice == "12":
            memento_add()
        elif choice == "13":
            memento_save()
        elif choice == "14":
            memento_restore()
        elif choice == "15":
            memento_view()
        elif choice == "16":
            iterator_all()
        elif choice == "17":
            iterator_category()
        elif choice == "18":
            iterator_price()
        elif choice == "19":
            iterator_scoville()
        elif choice == "20":
            iterator_extreme()
        elif choice == "0":
            print("\n  🔥 La revedere! Va asteptam la Ardeirosu pentru iuteala adevarata! 🔥\n")
            break
        else:
            print("  Optiune invalida.")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                print("\n  La revedere!\n")
                break


if __name__ == "__main__":
    main()