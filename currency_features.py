CURRENCY_FEATURES = {
    2000: {
        'description': """
        The ₹2000 note features the Mangalyaan on the reverse side. 
        Key RBI security features include:
        - Color-shifting windowed security thread with RBI and ₹2000
        - Portrait watermark of Mahatma Gandhi
        - Micro letters 'RBI' and '2000'
        - See-through register in denomination numeral
        """,
        'security_features': [
            'Color-shifting windowed security thread with RBI inscription',
            'Portrait and electrotype watermarks',
            'Micro lettering "RBI" and "2000"',
            'See-through register with denominational numeral',
            'Color-shifting windowed security thread',
            'Latent image of denomination',
            'Optically variable ink on denomination numeral'
        ],
        'detection_params': {
            'thread_width_range': (0.8, 1.2),  # mm
            'thread_color': 'green_to_blue',
            'micro_text_size': 0.2  # mm
        }
    },
    500: {
        'description': """
        The ₹500 note features the Red Fort on the reverse side.
        Key RBI security features include:
        - Color-shifting windowed security thread with RBI and ₹500
        - Portrait watermark of Mahatma Gandhi
        - Micro letters 'RBI' and '500'
        - See-through register in denomination numeral
        """,
        'security_features': [
            'Color-shifting windowed security thread with RBI inscription',
            'Portrait and electrotype watermarks',
            'Micro lettering "RBI" and "500"',
            'See-through register with denominational numeral',
            'Color-shifting windowed security thread',
            'Latent image of denomination'
        ],
        'detection_params': {
            'thread_width_range': (0.7, 1.1),  # mm
            'thread_color': 'green_to_blue',
            'micro_text_size': 0.18  # mm
        }
    },
    200: {
        'description': """
        The ₹200 note features Sanchi Stupa on the reverse side.
        Key RBI security features include:
        - Color-shifting windowed security thread with RBI and ₹200
        - Portrait watermark of Mahatma Gandhi
        - Micro letters 'RBI' and '200'
        - See-through register in denomination numeral
        """,
        'security_features': [
            'Color-shifting windowed security thread with RBI inscription',
            'Portrait and electrotype watermarks',
            'Micro lettering "RBI" and "200"',
            'See-through register with denominational numeral',
            'Latent image of denomination'
        ],
        'detection_params': {
            'thread_width_range': (0.7, 1.0),  # mm
            'thread_color': 'orange_to_green',
            'micro_text_size': 0.18  # mm
        }
    },
    100: {
        'description': """
        The ₹100 note features Rani ki Vav on the reverse side.
        Key RBI security features include:
        - Color-shifting windowed security thread with RBI and ₹100
        - Portrait watermark of Mahatma Gandhi
        - Micro letters 'RBI' and '100'
        - See-through register in denomination numeral
        """,
        'security_features': [
            'Windowed security thread with inscriptions',
            'Portrait and electrotype watermarks',
            'Micro lettering "RBI" and "100"',
            'See-through register with denominational numeral',
            'Latent image of denomination'
        ],
        'detection_params': {
            'thread_width_range': (0.6, 0.9),  # mm
            'thread_color': 'green_to_blue',
            'micro_text_size': 0.15  # mm
        }
    }
}

SECURITY_FEATURES = {
    'security_thread': {
        'description': 'Color-shifting windowed security thread with RBI inscriptions',
        'detection_params': {
            'threshold': 0.7,
            'min_area': 1000,
            'aspect_ratio': (8, 12),  # Length to width ratio
            'color_shift_detection': True
        },
        'rbi_guidelines': """
        The security thread is a windowed thread that changes color when viewed from different angles.
        It contains micro-printed text 'RBI' and the denomination value.
        """
    },
    'watermark': {
        'description': 'Portrait watermark of Mahatma Gandhi and electrotype denomination',
        'detection_params': {
            'threshold': 0.6,
            'min_contrast': 0.3,
            'portrait_area_ratio': 0.15,  # Relative to note size
            'electrotype_present': True
        },
        'rbi_guidelines': """
        The watermark should show a portrait of Mahatma Gandhi and an electrotype denomination numeral.
        The portrait should be visible when held against light.
        """
    },
    'micro_lettering': {
        'description': 'Micro letters RBI and denomination value',
        'detection_params': {
            'threshold': 0.8,
            'min_size': 5,
            'text_pattern': r'(RBI|\d{3,4})',
            'min_confidence': 0.7
        },
        'rbi_guidelines': """
        Micro letters 'RBI' and the denomination value should be present.
        These are visible under a magnifying glass.
        """
    }
}