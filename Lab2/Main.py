from Factory.Factory_method import (
    SrirachaFactory, HabaneroMangoFactory, GhostPepperSauceFactory,
    CayennePowderFactory, CajunBlendFactory,
    JalapenoWholePepperFactory, CarolinaReaperFactory,
    PinkHimalayaSaltFactory, BlackSaltGhostFactory,
)
from Abstract.Abstract_factory import MildPackageFactory, MediumPackageFactory, InfernoPackageFactory


def pause():
    input("\n  Apasa ENTER pentru a continua...")


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


created_products = []

# ─────────────────────────────────────────
#  FACTORY METHOD — meniuri
# ─────────────────────────────────────────

FACTORIES = {
    "1": ("Sriracha Original      [sos]",         SrirachaFactory()),
    "2": ("Habanero Mango Blast   [sos]",          HabaneroMangoFactory()),
    "3": ("Ghost Pepper Inferno   [sos]",          GhostPepperSauceFactory()),
    "4": ("Cayenne Pudra          [condiment]",    CayennePowderFactory()),
    "5": ("Amestec Cajun          [condiment]",    CajunBlendFactory()),
    "6": ("Jalapeno Intreg        [ardei]",        JalapenoWholePepperFactory()),
    "7": ("Carolina Reaper Pudra  [ardei]",        CarolinaReaperFactory()),
    "8": ("Sare Roz cu Chili      [sare]",         PinkHimalayaSaltFactory()),
    "9": ("Sare Neagra Ghost      [sare]",         BlackSaltGhostFactory()),
}


def factory_comanda_produs():
    header("FACTORY METHOD — Comanda produs")
    print("\n  Fabrici disponibile:\n")
    for key, (label, _) in FACTORIES.items():
        print(f"    [{key}] {label}")

    tip = alege_optiune("\n  Alege fabrica [1-9]: ", list(FACTORIES.keys()))
    if tip is None:
        return

    label, factory = FACTORIES[tip]
    product = factory.order_product()
    created_products.append(product)

    print(f"\n  Produs creat:")
    print(f"    Tip:      {type(product).__name__}")
    print(f"    Nume:     {product.name}")
    print(f"    Pret:     {product.price:.2f} LEI")
    print(f"    Iuteala:  {product.scoville} SHU")
    print(f"    Descriere:{product.get_description()}")
    pause()


def factory_toate_fabricile():
    header("FACTORY METHOD — Toate fabricile")
    print()
    for key, (label, factory) in FACTORIES.items():
        product = factory.order_product()
        created_products.append(product)
        print(f"    [{key}] {label}")
        print(f"         -> {product}")
        print()
    pause()


def factory_lista():
    header("FACTORY METHOD — Produse create")
    if not created_products:
        print("  Niciun produs creat inca.")
    else:
        for i, product in enumerate(created_products, 1):
            print(f"    [{i}] {product}")
    pause()


# ─────────────────────────────────────────
#  ABSTRACT FACTORY — meniuri
# ─────────────────────────────────────────

PACKAGE_FACTORIES = {
    "1": ("🟢 Mild   — pana la 5.000 SHU  (incepatori)",    MildPackageFactory()),
    "2": ("🟡 Medium — 5.000–50.000 SHU   (cunoscatori)",   MediumPackageFactory()),
    "3": ("🔴 Inferno — peste 50.000 SHU  (aventurieri)",   InfernoPackageFactory()),
}


def abstract_pachet():
    header("ABSTRACT FACTORY — Pachet dupa nivel de iuteala")
    print("\n  Niveluri disponibile:\n")
    for key, (label, _) in PACKAGE_FACTORIES.items():
        print(f"    [{key}] {label}")

    tip = alege_optiune("\n  Alege nivelul [1/2/3]: ", ["1", "2", "3"])
    if tip is None:
        return

    label, factory = PACKAGE_FACTORIES[tip]
    package = factory.create_package()

    print(f"\n  Pachet: {label}\n")
    print(f"    Sos:        {package['sauce']}")
    print(f"    Condiment:  {package['spice_blend']}")
    print(f"    Ardei:      {package['pepper_sample']}")
    pause()


def abstract_toate_pachetele():
    header("ABSTRACT FACTORY — Toate pachetele")
    print()
    for key, (label, factory) in PACKAGE_FACTORIES.items():
        package = factory.create_package()
        print(f"  {'─'*54}")
        print(f"  Pachet: {label}")
        print(f"    Sos:        {package['sauce']}")
        print(f"    Condiment:  {package['spice_blend']}")
        print(f"    Ardei:      {package['pepper_sample']}")
        print()
    pause()


# ─────────────────────────────────────────
#  MENIU PRINCIPAL
# ─────────────────────────────────────────

def show_menu():
    print()
    print("=" * 60)
    print("  ARDEI ROSU — Lab 2: Factory Method & Abstract Factory")
    print("=" * 60)
    print("    [1] Factory Method  — Comanda un produs")
    print("    [2] Factory Method  — Toate fabricile")
    print("    [3] Factory Method  — Lista produse create")
    print("    [4] Abstract Factory — Pachet dupa nivel iuteala")
    print("    [5] Abstract Factory — Toate pachetele")
    print("    [0] Iesire")
    print("-" * 60)


def main():
    while True:
        show_menu()
        choice = input("  Optiunea: ").strip()

        if choice == "1":
            factory_comanda_produs()
        elif choice == "2":
            factory_toate_fabricile()
        elif choice == "3":
            factory_lista()
        elif choice == "4":
            abstract_pachet()
        elif choice == "5":
            abstract_toate_pachetele()
        elif choice == "0":
            print("\n  La revedere! Pofta mare si mult curaj! 🌶️\n")
            break
        else:
            print("  Optiune invalida.")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                print("\n  La revedere!\n")
                break


if __name__ == "__main__":
    main()
