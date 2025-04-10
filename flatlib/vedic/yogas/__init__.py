"""
    This file is part of flatlib - (C) FlatAngle
    Modified for Vedic Astrology
    
    This module implements Yogas (planetary combinations) calculations
    for Vedic astrology. It includes functions to identify and analyze
    various types of Yogas in a chart.
"""

from flatlib import const
from flatlib.chart import Chart
from flatlib.vedic.yogas.core import (
    get_yoga_summary, get_yoga_strength,
    get_yoga_effects, get_strongest_yoga
)

# Import specific yoga calculation functions
from flatlib.vedic.yogas.mahapurusha import (
    get_mahapurusha_yogas, has_ruchaka_yoga,
    has_bhadra_yoga, has_hamsa_yoga,
    has_malavya_yoga, has_sasa_yoga
)
from flatlib.vedic.yogas.raja import (
    get_raja_yogas, has_dharmakarmaadhipati_yoga,
    has_gajakesari_yoga, has_amala_yoga,
    has_sreenatha_yoga, has_chandra_mangala_yoga
)
from flatlib.vedic.yogas.dhana import (
    get_dhana_yogas, has_lakshmi_yoga,
    has_kubera_yoga, has_kalanidhi_yoga,
    has_vasumati_yoga, has_mridanga_yoga
)
from flatlib.vedic.yogas.nabhasa import (
    get_nabhasa_yogas, has_rajju_yoga,
    has_musala_yoga, has_nala_yoga,
    has_mala_yoga, has_sarpa_yoga
)
from flatlib.vedic.yogas.dosha import (
    get_dosha_yogas, has_kemadruma_yoga,
    has_daridra_yoga, has_shakat_yoga,
    has_kalasarpa_yoga, has_graha_yuddha
)
from flatlib.vedic.yogas.chandra import (
    get_chandra_yogas, has_adhi_yoga,
    has_sunapha_yoga, has_anapha_yoga,
    has_durudhura_yoga, has_kemadruma_yoga
)
from flatlib.vedic.yogas.analysis import (
    analyze_yogas, get_yoga_predictions,
    get_yoga_compatibility, get_yoga_strength_score
)

# Constants for Yoga types
MAHAPURUSHA_YOGA = 'Mahapurusha Yoga'
RAJA_YOGA = 'Raja Yoga'
DHANA_YOGA = 'Dhana Yoga'
NABHASA_YOGA = 'Nabhasa Yoga'
DOSHA_YOGA = 'Dosha Yoga'
CHANDRA_YOGA = 'Chandra Yoga'

# List of all Yoga types
LIST_YOGA_TYPES = [
    MAHAPURUSHA_YOGA, RAJA_YOGA, DHANA_YOGA,
    NABHASA_YOGA, DOSHA_YOGA, CHANDRA_YOGA
]


def get_all_yogas(chart):
    """
    Identify all Yogas in a chart
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with all Yoga information
    """
    # Initialize the result
    result = {
        'mahapurusha_yogas': get_mahapurusha_yogas(chart),
        'raja_yogas': get_raja_yogas(chart),
        'dhana_yogas': get_dhana_yogas(chart),
        'nabhasa_yogas': get_nabhasa_yogas(chart),
        'dosha_yogas': get_dosha_yogas(chart),
        'chandra_yogas': get_chandra_yogas(chart),
        'summary': None
    }
    
    # Generate summary information
    result['summary'] = get_yoga_summary(result)
    
    return result


def get_yoga_analysis(chart):
    """
    Analyze the Yogas in a chart
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Yoga analysis
    """
    # Get all Yogas
    yogas = get_all_yogas(chart)
    
    # Analyze the Yogas
    analysis = analyze_yogas(chart, yogas)
    
    return analysis


def has_yoga(chart, yoga_name):
    """
    Check if a chart has a specific Yoga
    
    Args:
        chart (Chart): The birth chart
        yoga_name (str): The name of the Yoga to check
    
    Returns:
        bool: True if the chart has the Yoga, False otherwise
    """
    # Get all Yogas
    yogas = get_all_yogas(chart)
    
    # Check each type of Yoga
    for yoga_type, yoga_list in yogas.items():
        if yoga_type != 'summary':
            for yoga in yoga_list:
                if yoga['name'] == yoga_name:
                    return True
    
    return False


def get_yoga_predictions(chart):
    """
    Generate predictions based on Yogas in a chart
    
    Args:
        chart (Chart): The birth chart
    
    Returns:
        dict: Dictionary with Yoga predictions
    """
    # Get all Yogas
    yogas = get_all_yogas(chart)
    
    # Generate predictions
    predictions = get_yoga_predictions(chart, yogas)
    
    return predictions
