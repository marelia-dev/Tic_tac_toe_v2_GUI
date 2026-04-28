from models.cpu import CPUZaidejas
from models.game import Zaidimas
from models.players import Zaidejas
from models.scores import Skaiciuokle
from models.symbols import Symbols


def gauti_skaiciu(pranesimas: str) -> int:
    while True:
        try:
            ivestis = input(pranesimas).strip()
            if not ivestis:
                print("Iveskite skaiciu!")
                continue
            return int(ivestis)
        except ValueError:
            print("Klaida: iveskite sveikaji skaiciu!")

skaiciuokle = Skaiciuokle()

while True:
    veiksmas = gauti_skaiciu(
        "\n1 - naujas zaidimas\n"
        "2 - parodyti statistika\n"
        "3 - prideti zaideja\n"
        "0 - išeiti\n"
        "→ "
    )

    match veiksmas:
        case 1:

            real_zaidejai = list(skaiciuokle.skaicius.keys())

            cpu_variants = [
                ("CPU Lengvas", 1),
                ("CPU Vidutinis", 2),
                ("CPU Sunkus", 3)
            ]

            all_choice = real_zaidejai + [name for name, _ in cpu_variants]

            if not real_zaidejai:
                print("Pirmiausia pridekite bent viena tikra zaideja (punktas 3)!")
                continue

            print("\nGalimi zaidejai:")
            print("Zmones:")
            for idx, name in enumerate(real_zaidejai, 1):
                print(f"{idx}. {name.title()}")

            print("\nKompiuteris:")
            start_idx = len(real_zaidejai) + 1
            for i, (cpu_name, _) in enumerate(cpu_variants, start=start_idx):
                print(f"  {i}. {cpu_name}")

            #pirmo pasirinkimas
            nr1 = None
            while True:
                nr1 = gauti_skaiciu("Pirmo zaidejo numeris: ")
                if 1 <= nr1 <= len(all_choice):
                    break
                print("Netinkamas numeris!")

            nr2 = None
            while True:
                nr2 = gauti_skaiciu("Antro zaidejo numeris: ")
                if 1 <= nr2 <= len(all_choice):
                    break
                print("Netinkamas arba tas pats numeris!")

            #leidimas cpu zaisti tarpusavi
            is_cpu1 = nr1 > len(real_zaidejai)
            is_cpu2 = nr2 > len(real_zaidejai)

            if nr1 == nr2 and not (is_cpu1 and is_cpu2):  # jeigu nors vienas tikras zmogus
                if nr1 == nr2:
                    print("Zaidejai negali buti tie patys! Pasirinkite skirtingus numerius (tik CPU gali zaisti su savimi).")
                    continue

            def get_player(idx):
                name = all_choice[idx - 1]
                if name in real_zaidejai:
                    parts = name.split(maxsplit=1)
                    return Zaidejas(parts[0], parts[1] if len(parts) > 1 else ""), False

                else:
                    for cpu_name, level in cpu_variants:
                        if cpu_name == name:
                            return CPUZaidejas("CPU", cpu_name, level=level), True
                    raise ValueError(f"Neatpazintas CPU {name}")

            zaidejas1, is_cpu1 = get_player(nr1)
            zaidejas2, is_cpu2 = get_player(nr2)

            symbols = Symbols()

            print(f"\nZaidimas: {zaidejas1} {symbols.get_x()} pries {zaidejas2} {symbols.get_o()}\n")


            zaidimas = Zaidimas(zaidejas1, zaidejas2)
            laimejantis = zaidimas.zaisti()

            if not is_cpu1:
                skaiciuokle.prideti_rezultata(
                    zaidejas1, zaidejas2,
                    laimejantis if laimejantis == zaidejas1 else (None if laimejantis is None else zaidejas2)
                )

            if not is_cpu2:
                skaiciuokle.prideti_rezultata(
                    zaidejas1, zaidejas2,
                    laimejantis if laimejantis == zaidejas2 else (None if laimejantis is None else zaidejas1)
                )

        case 2:
            skaiciuokle.rodyti_skaiciu()

        case 3:
            vardas = input("Iveskite varda: ").strip()
            pavarde = input("Iveskite pavarde: ").strip()

            if not vardas or not pavarde:
                print("Vardas ir pavarde negali buti tusti!")
                continue

            naujas_zaidejas = Zaidejas(vardas, pavarde)
            skaiciuokle.prideti_zaideja(naujas_zaidejas)

        case 0:
            print("Viso gero!")
            break
        case _:
            print("Tokio pasirinkimo nera!")

