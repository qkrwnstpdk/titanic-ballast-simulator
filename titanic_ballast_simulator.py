#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Titanic 700:1 ballast-layout calculator: 6 zones, 1 to 6 marbles."""

from itertools import combinations
from math import sqrt

ZONES = "ABCDEF"
POSITIONS = dict(zip(ZONES, (-2.5, -1.5, -0.5, 0.5, 1.5, 2.5)))


def calculate(layout, dry_mass=110.0, marble_mass=1.31,
              flooding_limit=145.0, inflow_rate=1.5):
    """Return a comparative model's estimated time and longitudinal trim."""
    if (not layout or any(z not in ZONES for z in layout)
            or len(set(layout)) != len(layout)):
        raise ValueError("Choose one or more unique zones A-F.")
    if dry_mass < 0 or marble_mass < 0 or flooding_limit <= 0 or inflow_rate <= 0:
        raise ValueError("Masses must be >= 0; limit and inflow must be > 0.")

    n = len(layout)
    xs = [POSITIONS[z] for z in layout]
    mean_x = sum(xs) / n
    spread = sqrt(sum((x - mean_x) ** 2 for x in xs) / n)
    total_mass = dry_mass + n * marble_mass
    base_time = (flooding_limit - total_mass) / inflow_rate
    time = max(0.0, base_time - 1.45 * abs(mean_x) + 0.12 * (spread / 2.5))
    trim_degrees = 1.6 * mean_x  # negative = bow down; positive = stern down
    return {
        "layout": "".join(z for z in ZONES if z in layout),
        "marble_count": n,
        "total_mass_g": total_mass,
        "estimated_time_s": time,
        "trim_degrees": trim_degrees,
    }


def all_cases(**kwargs):
    """Return all 63 non-empty, unique placement combinations."""
    result = []
    number = 1
    for n in range(1, 7):
        for combo in combinations(ZONES, n):
            result.append({"number": number, **calculate(combo, **kwargs)})
            number += 1
    return result


def main():
    print("Titanic 700:1 Ballast Layout Simulator")
    print("A=bow, F=stern. One marble maximum in each zone.")
    try:
        dry = float(input("Dry model mass in g [110]: ") or 110)
        marble = float(input("One marble mass in g [1.31]: ") or 1.31)
        limit = float(input("Flooding threshold in g [145]: ") or 145)
        flow = float(input("Inflow rate in g/s [1.5]: ") or 1.5)
        print("Enter a layout such as ACF or ABCF. Enter q to quit.")
        while True:
            s = input("Layout> ").strip().upper().replace("-", "").replace(" ", "")
            if s == "Q":
                break
            try:
                r = calculate(s, dry, marble, limit, flow)
                if r["trim_degrees"] < -0.25:
                    trim = f"bow down {abs(r['trim_degrees']):.2f} degrees"
                elif r["trim_degrees"] > 0.25:
                    trim = f"stern down {abs(r['trim_degrees']):.2f} degrees"
                else:
                    trim = f"almost level ({abs(r['trim_degrees']):.2f} degrees)"
                print(f"{r['layout']}: {r['marble_count']} marbles, "
                      f"{r['estimated_time_s']:.2f} s, {trim}")
            except ValueError as exc:
                print(exc)
        print("\\nAll 63 combinations:")
        for r in all_cases(dry_mass=dry, marble_mass=marble,
                           flooding_limit=limit, inflow_rate=flow):
            print(f"{r['number']:02d} | {r['marble_count']} | {r['layout']:<6} | "
                  f"{r['estimated_time_s']:.2f} s | {r['trim_degrees']:.2f} deg")
    except (ValueError, EOFError) as exc:
        print(f"Invalid input: {exc}")


if __name__ == "__main__":
    main()
