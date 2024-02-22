import sys

ELEMENTS = [
    "Bq",
    "H",                                                                                                                                                                                     "He",
    "Li", "Be",                                                                                                                                                 "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg",                                                                                                                                                 "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V ", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",                                                                                     "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Te", "Ru", "Rh", "Pd", "Ag", "Cd",                                                                                     "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W ", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U ", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
]

_ANCHOR_OPT = "Geom Opt Step"
_ANCHOR_CONV = "Geometry Convergence"
_ANCHOR_OPT_DONE = " Geometry Optimization Converged"

_SEP_GRAD = " " + "Grad" * 18
_SEP_DASH = " " + "-" * 69

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 AfakeG.py mol.aop")

    aop = sys.argv[1]
    gop = aop.replace(".aop", "_fake.out")

    with open(aop) as f_aop:
        contents = f_aop.readlines()

    while contents:
        line = contents.pop(0)

        if _ANCHOR_OPT in line.rstrip():
            opt_step = int(line.split()[3])
            print(f">>> Found geometry optimization step {opt_step}")

            # parse current geometry
            # blank line
            _ = contents.pop(0)

            # Current Geometry
            _ = contents.pop(0)

            # blank line
            _ = contents.pop(0)

            geom = []

            while line := contents.pop(0).rstrip():
                arr = line.split()
                arr[1:] = [float(x) for x in arr[1:]]
                geom.append(arr)

            # parse geometry convergence
            # find anchor
            while _ANCHOR_CONV not in (line := contents.pop(0).rstrip()):
                pass

            # blank line
            _ = contents.pop(0)

            # current energy
            line = contents.pop(0).rstrip()
            arr = line.split()
            current_energy = float(arr[3])

            # energy change
            line = contents.pop(0).rstrip()
            arr = line.split()
            energy_change = float(arr[3])

            # conv conditions
            while "RMS Force" not in (line := contents.pop(0).rstrip()):
                pass

            # RMS Force, Max Force, RMS Step, & Max Step
            items = []
            thresholds = []

            for _ in range(4):
                arr = line.split()
                items.append(float(arr[2]))
                thresholds.append(float(arr[3]))
                line = contents.pop(0).rstrip()

            # write fake Gaussian output
            if opt_step == 1:
                with open(gop, "w") as f_gop:
                    header = [
                        " ! This file was generated by AfakeG.py\n",
                        " ! https://github.com/mizu-bai/AfakeG\n",
                        "\n",
                        " 0 basis functions\n",
                        " 0 alpha electrons\n",
                        " 0 beta electrons\n",
                        f"{_SEP_GRAD}\n",
                        f"{_SEP_GRAD}\n\n",
                    ]

                    f_gop.writelines(header)

            with open(gop, "a") as f_gop:
                fake_contents = [
                    f"{'Standard orientation:':>46s}\n",
                    f"{_SEP_DASH}\n",
                    " Center     Atomic      Atomic             Coordinates (Angstroms)\n",
                    " Number     Number       Type             X           Y           Z\n",
                    f"{_SEP_DASH}\n",
                ]

                for (atom_idx, atom) in enumerate(geom):
                    fake_contents.append(
                        f"{atom_idx:>7d}{ELEMENTS.index(atom[0]):>11d}{0:>12d}{atom[1]:>16.6f}{atom[2]:>12.6f}{atom[3]:>12.6f}\n"
                    )

                fake_contents.append(f"{_SEP_DASH}\n")
                fake_contents.append(f" SCF Done:{current_energy:>20.8f}\n\n")
                fake_contents.append(f"{_SEP_DASH}\n")

                fake_contents.append(f"{_SEP_GRAD}\n")
                fake_contents.append(f" Step number{opt_step:>4d}\n")
                fake_contents.append(
                    "         Item               Value     Threshold  Converged?\n"
                )

                fake_contents.append(
                    f" Maximum Force       {items[0]:>13.6f}{thresholds[0]:>13.6f}{('YES' if items[0] < thresholds[0] else 'NO'):>8s}\n"
                )
                fake_contents.append(
                    f" RMS     Force       {items[1]:>13.6f}{thresholds[1]:>13.6f}{('YES' if items[1] < thresholds[1] else 'NO'):>8s}\n"
                )
                fake_contents.append(
                    f" Maximum Displacement{items[2]:>13.6f}{thresholds[2]:>13.6f}{('YES' if items[2] < thresholds[2] else 'NO'):>8s}\n"
                )
                fake_contents.append(
                    f" RMS     Displacement{items[3]:>13.6f}{thresholds[3]:>13.6f}{('YES' if items[3] < thresholds[3] else 'NO'):>8s}\n"
                )

                fake_contents.append(
                    f"{_SEP_GRAD}\n\n",
                )

                f_gop.writelines(fake_contents)

        if _ANCHOR_OPT_DONE in line.rstrip():
            with open(gop, "a") as f_gop:
                f_gop.writelines(" Normal termination of Gaussian\n")

    print("大师大法好！")
