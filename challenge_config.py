import random
from typing import List, Dict

FALLBACK_CHALLENGES: List[Dict[str, str]] = [
    # WASTE
    {
        "challenge": "Avoid single-use plastics today",
        "why_it_matters": "Single-use plastics like bags, bottles, and cutlery are used for a few minutes but can persist in the environment for hundreds of years. They often end up in oceans, harming wildlife and breaking down into microplastics.",
        "impact_estimate": "Skipping single-use plastics for a day can prevent several items from entering landfills or waterways, especially if repeated regularly.",
        "category": "Waste",
    },
    {
        "challenge": "Bring a reusable bag when you shop",
        "why_it_matters": "Plastic bags are rarely recycled and can easily blow into rivers and oceans. Reusable bags reduce the need for new plastic production and help keep litter out of the environment.",
        "impact_estimate": "One reusable bag can replace hundreds of plastic bags over its lifetime.",
        "category": "Waste",
    },

    # WATER
    {
        "challenge": "Take a 5-minute shower instead of a long one",
        "why_it_matters": "Shorter showers conserve fresh water and reduce the energy needed to heat that water. This supports both water security and lower household emissions.",
        "impact_estimate": "Reducing your shower by 5 minutes can save 10–15 gallons of water per shower.",
        "category": "Water",
    },
    {
        "challenge": "Turn off the tap while brushing your teeth",
        "why_it_matters": "Leaving the tap running wastes clean, treated water that required energy and infrastructure to deliver. Turning it off is a simple way to cut daily water waste.",
        "impact_estimate": "You can save up to 4 gallons of water each time you brush with the tap off.",
        "category": "Water",
    },

    # ENERGY
    {
        "challenge": "Unplug chargers and devices you’re not using",
        "why_it_matters": "Many devices draw power even when they’re in standby mode. Reducing this 'phantom load' cuts energy waste and lowers your carbon footprint.",
        "impact_estimate": "Phantom loads can account for 5–10% of household electricity use in some homes.",
        "category": "Energy",
    },
    {
        "challenge": "Turn off lights when leaving a room",
        "why_it_matters": "Lighting is a significant portion of home and office energy use. Turning off unused lights reduces electricity demand and associated emissions.",
        "impact_estimate": "Consistently turning off lights can save dozens of kWh per year per household.",
        "category": "Energy",
    },

    # FOOD
    {
        "challenge": "Eat one plant-based meal today",
        "why_it_matters": "Plant-based meals generally require fewer resources and emit less greenhouse gases than meat-heavy meals. Even small shifts in diet can add up over time.",
        "impact_estimate": "Swapping one beef-based meal for a plant-based option can cut that meal’s emissions by several kilograms of CO₂-equivalent.",
        "category": "Food",
    },
    {
        "challenge": "Use leftovers instead of throwing them away",
        "why_it_matters": "Food waste means wasted water, land, energy, and labor used to produce it. Using leftovers reduces waste and stretches your food budget.",
        "impact_estimate": "If many households reduced food waste by just 25%, it would significantly cut global food-related emissions.",
        "category": "Food",
    },

    # TRANSPORT
    {
        "challenge": "Walk or bike for one short trip instead of driving",
        "why_it_matters": "Short car trips are fuel-inefficient and add up to significant emissions. Walking or biking improves health and reduces pollution.",
        "impact_estimate": "Replacing a 2–3 mile car trip with walking or biking can save around 1 kg of CO₂.",
        "category": "Transport",
    },
    {
        "challenge": "Carpool or use public transit for one commute",
        "why_it_matters": "Sharing rides or using public transit reduces the number of vehicles on the road, lowering emissions and traffic congestion.",
        "impact_estimate": "Carpooling with one other person can cut that trip’s per-person emissions almost in half.",
        "category": "Transport",
    },

    # DIGITAL
    {
        "challenge": "Unsubscribe from newsletters you never read",
        "why_it_matters": "Every email stored and sent uses data center energy. Decluttering your inbox reduces unnecessary digital storage and processing.",
        "impact_estimate": "Reducing unwanted emails has a small but real impact when millions of users do it together.",
        "category": "Digital",
    },
    {
        "challenge": "Lower the brightness on your screens today",
        "why_it_matters": "Screens consume more power at higher brightness levels. Lowering brightness slightly can reduce energy use without sacrificing usability.",
        "impact_estimate": "Lowering screen brightness can reduce a device’s display power consumption by 20–30%.",
        "category": "Digital",
    },
]


def get_random_fallback(focus_areas: List[str]) -> Dict[str, str]:
    """
    Returns a single fallback challenge.
    If focus_areas is provided, it tries to pick a challenge whose category
    matches one of those focus areas. If none match, it falls back to any category.
    """
    if focus_areas:
        normalized_focus = {area.strip().lower() for area in focus_areas}
        filtered = [
            c for c in FALLBACK_CHALLENGES
            if c["category"].strip().lower() in normalized_focus
        ]
    else:
        filtered = []

    pool = filtered if filtered else FALLBACK_CHALLENGES
    return random.choice(pool)


if __name__ == "__main__":
    print("Test 1: ['Waste']")
    print(get_random_fallback(["Waste"]), "\n")

    print("Test 2: ['Energy']")
    print(get_random_fallback(["Energy"]), "\n")

    print("Test 3: [] (no focus)")
    print(get_random_fallback([]), "\n")
