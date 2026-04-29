from builder import HotLoversBoxBuilder, GourmetSpiceBoxBuilder, StarterKitBoxBuilder, SpiceDirector
from prototype import SpiceProductPrototype, SpiceProductRegistry
from singleton import SpiceStoreConfig


def pause():
    input("\n  Apasa ENTER pentru a continua...")


def citeste_int(prompt, error_msg="Valoare invalida. Introduceti un numar intreg."):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print(f"  {error_msg}")
            retry = input("  Incercati din nou? (d/n): ").strip().lower()
            if retry != "d":
                return None


def citeste_float(prompt, error_msg="Valoare invalida. Introduceti un numar."):
    while True:
        try:
            return float(input(prompt).strip())
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


def init_registry():
    registry = SpiceProductRegistry()
    registry.register("sriracha", SpiceProductPrototype(
        "Sriracha Original", 39.99, "sos_iute",
        {"aroma": "clasic", "volum_ml": 250, "scoville": 2200}
    ))
    registry.register("ghost_pepper", SpiceProductPrototype(
        "Ghost Pepper Inferno", 69.99, "sos_iute",
        {"aroma": "habanero", "volum_ml": 100, "scoville": 100000}
    ))
    registry.register("cayenne", SpiceProductPrototype(
        "Cayenne Pudra", 24.99, "condiment",
        {"forma": "pudra", "greutate_g": 100, "scoville": 40000}
    ))
    registry.register("jalapeno", SpiceProductPrototype(
        "Jalapeno Intreg", 27.99, "ardei_deshidratat",
        {"soi": "jalapeno", "intreg": True, "scoville": 8000}
    ))
    registry.register("sare_roz", SpiceProductPrototype(
        "Sare Roz cu Chili", 18.99, "sare_iute",
        {"baza": "roz himalaya", "greutate_g": 150, "scoville": 5000}
    ))
    return registry


# ─────────────────────────────────────────
#  BUILDER — meniuri
# ─────────────────────────────────────────

BUILDERS = {
    "1": ("Hot Lovers Box  🔥 (iuteala extrema)",    HotLoversBoxBuilder()),
    "2": ("Gourmet Spice Box 🍽️ (arome fine)",       GourmetSpiceBoxBuilder()),
    "3": ("Starter Kit Box 🌿 (incepatori)",          StarterKitBoxBuilder()),
}


def builder_pachet_complet():
    header("BUILDER — Pachet complet")
    print("\n  Tipuri de pachete:\n")
    for key, (label, _) in BUILDERS.items():
        print(f"    [{key}] {label}")

    tip = alege_optiune("\n  Alege tipul [1/2/3]: ", ["1", "2", "3"])
    if tip is None:
        return

    label, builder = BUILDERS[tip]
    director = SpiceDirector(builder)
    box = director.build_full_box()

    print(f"\n  Pachet complet: {label}\n")
    print(f"  {box}")
    pause()


def builder_pachet_minimal():
    header("BUILDER — Pachet minimal")
    print("\n  Tipuri de pachete:\n")
    for key, (label, _) in BUILDERS.items():
        print(f"    [{key}] {label}")

    tip = alege_optiune("\n  Alege tipul [1/2/3]: ", ["1", "2", "3"])
    if tip is None:
        return

    # Cream builder-e noi pentru a evita starea anterioara
    fresh_builders = {
        "1": ("Hot Lovers Box  🔥",   HotLoversBoxBuilder()),
        "2": ("Gourmet Spice Box 🍽️", GourmetSpiceBoxBuilder()),
        "3": ("Starter Kit Box 🌿",   StarterKitBoxBuilder()),
    }

    label, builder = fresh_builders[tip]
    director = SpiceDirector(builder)
    box = director.build_minimal_box()

    print(f"\n  Pachet minimal: {label}\n")
    print(f"  {box}")
    pause()


# ─────────────────────────────────────────
#  PROTOTYPE — meniuri
# ─────────────────────────────────────────

def prototype_lista(registry):
    header("PROTOTYPE — Prototipuri inregistrate")
    keys = registry.list_prototypes()
    if not keys:
        print("  Niciun prototip inregistrat.")
    else:
        for i, key in enumerate(keys, 1):
            clone = registry.clone(key)
            print(f"    [{i}] {key:<15} -> {clone}")
    pause()


def prototype_cloneaza(registry):
    header("PROTOTYPE — Cloneaza produs")
    keys = registry.list_prototypes()
    if not keys:
        print("  Niciun prototip disponibil.")
        pause()
        return

    print("\n  Prototipuri disponibile:")
    for i, key in enumerate(keys, 1):
        clone = registry.clone(key)
        print(f"    [{i}] {key:<15} -> {clone.name} ({clone.category}) - {clone.price:.2f} LEI")

    idx = citeste_int("\n  Numarul prototipului de clonat: ")
    if idx is None:
        return

    while idx < 1 or idx > len(keys):
        print(f"  Index invalid. Alegeti intre 1 si {len(keys)}.")
        retry = input("  Incercati din nou? (d/n): ").strip().lower()
        if retry != "d":
            return
        idx = citeste_int("\n  Numarul prototipului de clonat: ")
        if idx is None:
            return

    selected_key = keys[idx - 1]

    print("\n  Tip clonare:")
    print("    [1] Deep copy  (copie completa independenta)")
    print("    [2] Shallow copy (copie superficiala)")
    clone_type = alege_optiune("  Alegeti [1/2]: ", ["1", "2"])
    if clone_type is None:
        return

    deep = clone_type == "1"
    clone = registry.clone(selected_key, deep=deep)

    new_name = input(f"  Nume nou (ENTER = pastreaza '{clone.name}'): ").strip()
    if new_name:
        clone.name = new_name

    new_price_str = input(f"  Pret nou (ENTER = pastreaza {clone.price:.2f} LEI): ").strip()
    if new_price_str:
        new_price = citeste_float("  Confirmati pretul (LEI): ")
        if new_price is not None:
            clone.price = new_price

    print(f"\n  Clona creata cu succes!")
    print(f"    Nume:      {clone.name}")
    print(f"    Categorie: {clone.category}")
    print(f"    Pret:      {clone.price:.2f} LEI")
    print(f"    Atribute:  {clone.attributes}")
    print(f"    Metoda:    {'Deep copy' if deep else 'Shallow copy'}")
    pause()


def prototype_inregistreaza(registry):
    header("PROTOTYPE — Inregistreaza prototip nou")

    key = input("  Cheie unica (ex: habanero_mango): ").strip()
    if not key:
        print("  Cheia nu poate fi goala.")
        pause()
        return

    name = input("  Nume produs: ").strip()
    if not name:
        print("  Numele nu poate fi gol.")
        pause()
        return

    price = citeste_float("  Pret (LEI): ")
    if price is None:
        return

    print("  Categorie:")
    print("    [1] sos_iute")
    print("    [2] condiment")
    print("    [3] ardei_deshidratat")
    print("    [4] sare_iute")
    cat_choice = alege_optiune("  Alegeti [1/2/3/4]: ", ["1", "2", "3", "4"])
    if cat_choice is None:
        return
    categories = {"1": "sos_iute", "2": "condiment", "3": "ardei_deshidratat", "4": "sare_iute"}
    category = categories[cat_choice]

    attributes = {}
    print("\n  Adaugati atribute (tastati 'gata' pentru a finaliza):")
    while True:
        attr_key = input("    Cheie atribut (sau 'gata'): ").strip()
        if attr_key.lower() == "gata" or attr_key == "":
            break
        attr_val = input(f"    Valoare pentru '{attr_key}': ").strip()
        attributes[attr_key] = attr_val

    proto = SpiceProductPrototype(name, price, category, attributes)
    registry.register(key, proto)

    print(f"\n  Prototipul '{key}' inregistrat cu succes!")
    print(f"    {proto}")
    pause()


# ─────────────────────────────────────────
#  SINGLETON — meniuri
# ─────────────────────────────────────────

def singleton_configuratie():
    header("SINGLETON — Configuratie magazin")
    config = SpiceStoreConfig()

    print(f"\n  Nume magazin:            {config.store_name}")
    print(f"  Moneda:                  {config.currency}")
    print(f"  TVA:                     {config.tax_rate*100:.0f}%")
    print(f"  Reducere maxima:         {config.max_discount*100:.0f}%")
    print(f"  Avertisment iuteala:     {config.max_scoville_warning} SHU")
    print(f"\n  Instanta: {config}")
    pause()


def singleton_modifica():
    header("SINGLETON — Modifica setare custom")
    config = SpiceStoreConfig()

    key = input("  Cheie setare: ").strip()
    if not key:
        print("  Cheia nu poate fi goala.")
        pause()
        return

    value = input(f"  Valoare pentru '{key}': ").strip()
    config.set_setting(key, value)

    print(f"\n  Setarea '{key}' = '{value}' salvata.")
    pause()


def singleton_citeste():
    header("SINGLETON — Citeste setare custom")
    config = SpiceStoreConfig()

    key = input("  Cheie setare: ").strip()
    if not key:
        print("  Cheia nu poate fi goala.")
        pause()
        return

    value = config.get_setting(key)
    if value is None:
        print(f"  Setarea '{key}' nu exista.")
    else:
        print(f"  {key} = {value}")
    pause()


def singleton_verifica_instanta():
    header("SINGLETON — Verifica instanta unica")
    c1 = SpiceStoreConfig()
    c2 = SpiceStoreConfig()
    print(f"  config1: {id(c1)}")
    print(f"  config2: {id(c2)}")
    print(f"  Sunt aceeasi instanta: {c1 is c2}")
    pause()


# ─────────────────────────────────────────
#  MENIU PRINCIPAL
# ─────────────────────────────────────────

def show_menu():
    print()
    print("=" * 60)
    print("  ARDEI ROSU — Lab 3: Builder, Prototype, Singleton")
    print("=" * 60)
    print("    [1] Builder   — Pachet cadou complet")
    print("    [2] Builder   — Pachet cadou minimal")
    print("    [3] Prototype — Lista prototipuri")
    print("    [4] Prototype — Cloneaza produs")
    print("    [5] Prototype — Inregistreaza prototip nou")
    print("    [6] Singleton — Configuratie magazin")
    print("    [7] Singleton — Modifica setare custom")
    print("    [8] Singleton — Citeste setare custom")
    print("    [9] Singleton — Verifica instanta unica")
    print("    [0] Iesire")
    print("-" * 60)


def main():
    registry = init_registry()

    while True:
        show_menu()
        choice = input("  Optiunea: ").strip()

        if choice == "1":
            builder_pachet_complet()
        elif choice == "2":
            builder_pachet_minimal()
        elif choice == "3":
            prototype_lista(registry)
        elif choice == "4":
            prototype_cloneaza(registry)
        elif choice == "5":
            prototype_inregistreaza(registry)
        elif choice == "6":
            singleton_configuratie()
        elif choice == "7":
            singleton_modifica()
        elif choice == "8":
            singleton_citeste()
        elif choice == "9":
            singleton_verifica_instanta()
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
