"""
config/city_tier.py

City tier configuration and mappings.
Improvement #5: Separation of concerns - config in separate file
"""

# Tier 1 Cities: Major metro areas
TIER_1_CITIES = {
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Chandigarh"
}

# Tier 2 Cities: Second-tier metropolitan areas
TIER_2_CITIES = {
    "Gurgaon",
    "Noida",
    "Jaipur",
    "Indore",
    "Lucknow",
    "Kochi",
    "Surat",
    "Ahmedabad",
    "Bhopal",
    "Visakhapatnam"
}

# Tier 3 Cities: All other cities
# (Cities not in Tier 1 or 2)

"""
Usage:
    from config.city_tier import TIER_1_CITIES, TIER_2_CITIES
    
    if city in TIER_1_CITIES:
        tier = 1
    elif city in TIER_2_CITIES:
        tier = 2
    else:
        tier = 3
"""
