"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements core functionality for Ashtakavarga (eight-source strength)
    calculations in Vedic astrology.
"""

from flatlib import const
from flatlib import angle


def get_ashtakavarga_points(chart, planet_id, contributor_id):
    """
    Calculate Ashtakavarga points contributed by one planet to another
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet receiving the points
        contributor_id (str): The ID of the planet contributing the points
    
    Returns:
        list: List of 12 values (0 or 1) representing points in each sign
    """
    # Get the planets from the chart
    planet = chart.getObject(planet_id)
    contributor = chart.getObject(contributor_id) if contributor_id != const.ASC else chart.getAngle(const.ASC)
    
    # Get the sign numbers (0-11)
    planet_sign_num = get_sign_number(planet.sign)
    contributor_sign_num = get_sign_number(contributor.sign)
    
    # Initialize the points list with 12 zeros
    points = [0] * 12
    
    # Get the benefic positions for this planet-contributor combination
    benefic_positions = get_benefic_positions(planet_id, contributor_id)
    
    # Calculate the relative positions
    for position in benefic_positions:
        # Calculate the absolute position in the zodiac
        absolute_position = (contributor_sign_num + position) % 12
        
        # Set the point to 1 (Bindu)
        points[absolute_position] = 1
    
    return points


def get_ashtakavarga_table(chart, planet_id):
    """
    Generate an Ashtakavarga table for a planet
    
    Args:
        chart (Chart): The birth chart
        planet_id (str): The ID of the planet to analyze
    
    Returns:
        dict: Dictionary with Ashtakavarga table information
    """
    # Initialize the table with empty lists
    table = {
        'signs': [],
        'contributors': {},
        'totals': []
    }
    
    # Add the signs
    for sign in [const.ARIES, const.TAURUS, const.GEMINI, const.CANCER,
                const.LEO, const.VIRGO, const.LIBRA, const.SCORPIO,
                const.SAGITTARIUS, const.CAPRICORN, const.AQUARIUS, const.PISCES]:
        table['signs'].append(sign)
    
    # Add the contributors
    contributors = [const.SUN, const.MOON, const.MARS, const.MERCURY,
                   const.JUPITER, const.VENUS, const.SATURN, const.ASC]
    
    for contributor_id in contributors:
        # Get the points contributed by this planet
        points = get_ashtakavarga_points(chart, planet_id, contributor_id)
        
        # Add to the table
        table['contributors'][contributor_id] = points
    
    # Calculate the totals for each sign
    for i in range(12):
        total = 0
        for contributor_id in contributors:
            total += table['contributors'][contributor_id][i]
        table['totals'].append(total)
    
    return table


def get_ashtakavarga_summary(ashtakavarga_data):
    """
    Generate a summary of Ashtakavarga data
    
    Args:
        ashtakavarga_data (dict): Dictionary with Ashtakavarga data
    
    Returns:
        dict: Dictionary with summary information
    """
    # Initialize the summary
    summary = {
        'total_bindus': 0,
        'planet_totals': {},
        'average_bindus': 0,
        'strongest_planet': None,
        'weakest_planet': None
    }
    
    # Calculate the total bindus for each planet
    max_bindus = -1
    min_bindus = float('inf')
    strongest_planet = None
    weakest_planet = None
    
    for planet_id, bhinna in ashtakavarga_data['bhinnashtakavarga'].items():
        total_bindus = bhinna['total_bindus']
        summary['planet_totals'][planet_id] = total_bindus
        summary['total_bindus'] += total_bindus
        
        if total_bindus > max_bindus:
            max_bindus = total_bindus
            strongest_planet = planet_id
        
        if total_bindus < min_bindus:
            min_bindus = total_bindus
            weakest_planet = planet_id
    
    # Calculate the average bindus per planet
    num_planets = len(ashtakavarga_data['bhinnashtakavarga'])
    summary['average_bindus'] = summary['total_bindus'] / num_planets if num_planets > 0 else 0
    
    # Set the strongest and weakest planets
    summary['strongest_planet'] = strongest_planet
    summary['weakest_planet'] = weakest_planet
    
    return summary


def get_ashtakavarga_strengths(ashtakavarga_data):
    """
    Calculate the strength of each planet based on Ashtakavarga
    
    Args:
        ashtakavarga_data (dict): Dictionary with Ashtakavarga data
    
    Returns:
        dict: Dictionary with strength information for each planet
    """
    # Initialize the strengths dictionary
    strengths = {}
    
    # Calculate the strength for each planet
    for planet_id, bhinna in ashtakavarga_data['bhinnashtakavarga'].items():
        # Get the total bindus
        total_bindus = bhinna['total_bindus']
        
        # Calculate the percentage of maximum possible bindus (56)
        percentage = (total_bindus / 56.0) * 100.0
        
        # Determine the strength category
        if percentage >= 75.0:
            strength_category = 'Very Strong'
        elif percentage >= 50.0:
            strength_category = 'Strong'
        elif percentage >= 25.0:
            strength_category = 'Moderate'
        else:
            strength_category = 'Weak'
        
        # Add to the strengths dictionary
        strengths[planet_id] = {
            'total_bindus': total_bindus,
            'percentage': percentage,
            'category': strength_category
        }
    
    return strengths


def get_sign_number(sign):
    """
    Get the number (0-11) of a sign
    
    Args:
        sign (str): The sign
    
    Returns:
        int: The sign number (0-11)
    """
    sign_numbers = {
        const.ARIES: 0,
        const.TAURUS: 1,
        const.GEMINI: 2,
        const.CANCER: 3,
        const.LEO: 4,
        const.VIRGO: 5,
        const.LIBRA: 6,
        const.SCORPIO: 7,
        const.SAGITTARIUS: 8,
        const.CAPRICORN: 9,
        const.AQUARIUS: 10,
        const.PISCES: 11
    }
    
    return sign_numbers.get(sign, 0)


def get_benefic_positions(planet_id, contributor_id):
    """
    Get the benefic positions for a planet-contributor combination
    
    Args:
        planet_id (str): The ID of the planet receiving the points
        contributor_id (str): The ID of the planet contributing the points
    
    Returns:
        list: List of benefic positions (0-11) relative to the contributor
    """
    # Benefic positions for each planet-contributor combination
    # These are the traditional Ashtakavarga benefic positions
    # The positions are relative to the contributor's position (0-11)
    
    # Sun's Ashtakavarga
    if planet_id == const.SUN:
        if contributor_id == const.SUN:
            return [1, 2, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.MOON:
            return [3, 6, 10, 11]
        elif contributor_id == const.MARS:
            return [1, 2, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.MERCURY:
            return [3, 5, 6, 9, 10, 11, 12]
        elif contributor_id == const.JUPITER:
            return [5, 6, 9, 11]
        elif contributor_id == const.VENUS:
            return [6, 7, 12]
        elif contributor_id == const.SATURN:
            return [1, 2, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.ASC:
            return [3, 4, 6, 10, 11, 12]
    
    # Moon's Ashtakavarga
    elif planet_id == const.MOON:
        if contributor_id == const.SUN:
            return [3, 6, 7, 8, 10, 11]
        elif contributor_id == const.MOON:
            return [1, 3, 6, 7, 10, 11]
        elif contributor_id == const.MARS:
            return [2, 3, 5, 6, 9, 10, 11]
        elif contributor_id == const.MERCURY:
            return [1, 3, 4, 5, 7, 8, 10, 11]
        elif contributor_id == const.JUPITER:
            return [1, 4, 7, 8, 10, 11]
        elif contributor_id == const.VENUS:
            return [3, 4, 5, 7, 9, 10, 11]
        elif contributor_id == const.SATURN:
            return [3, 5, 6, 11]
        elif contributor_id == const.ASC:
            return [3, 6, 10, 11]
    
    # Mars's Ashtakavarga
    elif planet_id == const.MARS:
        if contributor_id == const.SUN:
            return [3, 5, 6, 10, 11]
        elif contributor_id == const.MOON:
            return [3, 6, 11]
        elif contributor_id == const.MARS:
            return [1, 2, 4, 7, 8, 10, 11]
        elif contributor_id == const.MERCURY:
            return [3, 5, 6, 11]
        elif contributor_id == const.JUPITER:
            return [6, 10, 11, 12]
        elif contributor_id == const.VENUS:
            return [6, 8, 11, 12]
        elif contributor_id == const.SATURN:
            return [1, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.ASC:
            return [1, 3, 6, 10, 11]
    
    # Mercury's Ashtakavarga
    elif planet_id == const.MERCURY:
        if contributor_id == const.SUN:
            return [5, 6, 9, 11, 12]
        elif contributor_id == const.MOON:
            return [2, 4, 6, 8, 10, 11]
        elif contributor_id == const.MARS:
            return [1, 2, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.MERCURY:
            return [1, 3, 5, 6, 9, 10, 11, 12]
        elif contributor_id == const.JUPITER:
            return [6, 8, 11, 12]
        elif contributor_id == const.VENUS:
            return [1, 2, 3, 4, 5, 8, 9, 11]
        elif contributor_id == const.SATURN:
            return [1, 2, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.ASC:
            return [1, 2, 4, 6, 8, 10, 11]
    
    # Jupiter's Ashtakavarga
    elif planet_id == const.JUPITER:
        if contributor_id == const.SUN:
            return [1, 2, 3, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.MOON:
            return [2, 5, 7, 9, 11]
        elif contributor_id == const.MARS:
            return [1, 2, 4, 7, 8, 10, 11]
        elif contributor_id == const.MERCURY:
            return [1, 2, 4, 5, 6, 9, 10, 11]
        elif contributor_id == const.JUPITER:
            return [1, 2, 3, 4, 7, 8, 9, 10, 11]
        elif contributor_id == const.VENUS:
            return [2, 5, 6, 9, 10, 11]
        elif contributor_id == const.SATURN:
            return [3, 5, 6, 12]
        elif contributor_id == const.ASC:
            return [1, 2, 4, 5, 6, 7, 9, 10, 11]
    
    # Venus's Ashtakavarga
    elif planet_id == const.VENUS:
        if contributor_id == const.SUN:
            return [8, 11, 12]
        elif contributor_id == const.MOON:
            return [1, 2, 3, 4, 5, 8, 9, 11, 12]
        elif contributor_id == const.MARS:
            return [3, 4, 6, 9, 11, 12]
        elif contributor_id == const.MERCURY:
            return [3, 5, 6, 9, 11]
        elif contributor_id == const.JUPITER:
            return [5, 8, 9, 10, 11]
        elif contributor_id == const.VENUS:
            return [1, 2, 3, 4, 5, 8, 9, 10, 11]
        elif contributor_id == const.SATURN:
            return [3, 4, 5, 8, 9, 10, 11]
        elif contributor_id == const.ASC:
            return [1, 2, 3, 4, 5, 8, 9, 11]
    
    # Saturn's Ashtakavarga
    elif planet_id == const.SATURN:
        if contributor_id == const.SUN:
            return [1, 2, 4, 7, 8, 10, 11]
        elif contributor_id == const.MOON:
            return [3, 6, 11]
        elif contributor_id == const.MARS:
            return [3, 5, 6, 10, 11, 12]
        elif contributor_id == const.MERCURY:
            return [6, 8, 9, 10, 11, 12]
        elif contributor_id == const.JUPITER:
            return [5, 6, 11, 12]
        elif contributor_id == const.VENUS:
            return [6, 11, 12]
        elif contributor_id == const.SATURN:
            return [3, 5, 6, 11]
        elif contributor_id == const.ASC:
            return [1, 3, 4, 6, 10, 11]
    
    # Default: return an empty list
    return []
