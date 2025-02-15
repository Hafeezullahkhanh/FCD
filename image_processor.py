import cv2
import numpy as np

def process_image(image):
    """
    Enhanced image processing for more accurate feature detection
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # Denoise image
    denoised = cv2.fastNlMeansDenoising(enhanced)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

    return thresh

def detect_security_thread(image):
    """
    Enhanced security thread detection with color shift analysis
    """
    # Convert to HSV for color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for security thread (green-blue shift)
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    # Create masks for both colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Combine masks
    combined_mask = cv2.bitwise_or(mask_green, mask_blue)

    # Morphological operations to enhance thread detection
    kernel = np.ones((3,3), np.uint8)
    refined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(refined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours for thread-like properties
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = h/w if w > 0 else 0
        area = cv2.contourArea(contour)

        # Check for vertical line characteristics
        if (aspect_ratio > 8 and area > 1000 and area < 15000 and 
            cv2.arcLength(contour, True) / area < 0.5):
            return True, 0.9

    return False, 0.2

def detect_watermark(image):
    """
    Enhanced watermark detection with portrait recognition
    """
    # Apply contrast enhancement
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced_l = clahe.apply(l)
    enhanced_lab = cv2.merge([enhanced_l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Calculate local contrast
    blur = cv2.GaussianBlur(enhanced, (15, 15), 0)
    contrast = cv2.absdiff(enhanced, blur)

    # Analyze contrast patterns
    gray_contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    mean, stddev = cv2.meanStdDev(gray_contrast)

    # Look for portrait-like patterns
    high_contrast = cv2.threshold(
        gray_contrast, 
        0.3 * stddev[0][0], 
        255, 
        cv2.THRESH_BINARY
    )[1]

    contours, _ = cv2.findContours(high_contrast, cv2.RETR_EXTERNAL, 
                                 cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > image.size * 0.05:  # Minimum size threshold
            # Analyze contour shape for portrait-like characteristics
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            if 0.3 < circularity < 0.7:  # Portrait-like shape
                return True, 0.85

    return False, 0.3

def detect_micro_lettering(image):
    """
    Enhanced micro lettering detection with pattern analysis
    """
    # Enhance micro details
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.equalizeHist(gray)

    # Multi-scale edge detection
    edges1 = cv2.Canny(enhanced, 50, 150)
    edges2 = cv2.Canny(enhanced, 100, 200)

    # Combine edge detections
    edges = cv2.bitwise_or(edges1, edges2)

    # Analyze edge patterns
    kernel = np.ones((2,2), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)

    # Calculate pattern density
    pattern_size = cv2.countNonZero(dilated)
    h, w = dilated.shape
    density = pattern_size / (h * w)

    # Analyze pattern distribution
    if density > 0.15:
        # Check for regular spacing (characteristic of text)
        y_projection = np.sum(dilated, axis=1)
        x_projection = np.sum(dilated, axis=0)

        # Calculate variation in projections
        y_std = np.std(y_projection)
        x_std = np.std(x_projection)

        if y_std > 100 and x_std > 100:  # Indicates regular patterns
            return True, 0.8

    return False, 0.25

def analyze_features(processed_image, original_image):
    """
    Comprehensive security feature analysis with confidence scores
    """
    # Detect security thread
    thread_detected, thread_conf = detect_security_thread(original_image)

    # Detect watermark
    watermark_detected, watermark_conf = detect_watermark(original_image)

    # Detect micro lettering
    micro_detected, micro_conf = detect_micro_lettering(original_image)

    features = {
        'Security Thread': {
            'detected': thread_detected,
            'confidence': thread_conf,
            'description': 'Color-shifting security thread with RBI text'
        },
        'Watermark': {
            'detected': watermark_detected,
            'confidence': watermark_conf,
            'description': 'Gandhi portrait watermark'
        },
        'Micro Lettering': {
            'detected': micro_detected,
            'confidence': micro_conf,
            'description': 'Micro printed RBI text'
        }
    }

    return features