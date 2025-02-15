# Fake Currency Detector

This is a web-based application that verifies the authenticity of currency notes using advanced image processing and computer vision techniques. The app is built with Streamlit and OpenCV, providing a user-friendly interface that works on both desktops and mobile devices.

---

## Tech Stack Summary

- **Programming Language:**  
  Python 3.11

- **Web Framework & UI:**  
  [Streamlit](https://streamlit.io)  
  - Provides a rapid, interactive, and responsive web interface.

- **Image Processing & Computer Vision:**  
  - **OpenCV (opencv-python / opencv-python-headless):**  
    Used for image processing tasks such as grayscale conversion, contrast enhancement (using CLAHE), denoising, adaptive thresholding, and feature detection (security thread, watermark, and micro lettering).
  - **Pillow:**  
    For loading and manipulating images.

- **Numerical Computations:**  
  **NumPy**  
  - Powers efficient array operations and image data manipulation.

- **Additional Libraries:**  
  - **Twilio:** (Optional)  
    Can be integrated to send notifications or alerts.
  - Various supporting libraries (e.g., altair, attrs, etc.) for enhanced functionality and performance.

---

## How It Works

1. **Image Acquisition:**  
   Users can either upload an image of a currency note or capture one using their device’s camera.

2. **Image Processing:**  
   The app processes the image in memory (without storing previous uploads) by:
   - Converting the image to grayscale.
   - Enhancing contrast with CLAHE.
   - Denoising the image.
   - Applying adaptive thresholding to emphasize key features.

3. **Feature Detection:**  
   The processed image is analyzed to detect important security features:
   - **Security Thread:** Detected via HSV color analysis for the characteristic color shift.
   - **Watermark:** Detected using contrast analysis and contour detection.
   - **Micro Lettering:** Identified through edge detection and pattern analysis.

4. **Result Generation:**  
   Each detection returns a confidence score, which are then aggregated to generate an overall authenticity score. The app displays:
   - A progress bar and metric for the overall score.
   - Detailed analysis for each security feature along with RBI guidelines for reference.

5. **User Feedback:**  
   An educational section explains the official security features of various currency denominations, helping users understand what to look for.

---



