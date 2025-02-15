import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import base64
from datetime import datetime
from currency_features import CURRENCY_FEATURES, SECURITY_FEATURES
from image_processor import process_image, analyze_features

# Create storage directory if it doesn't exist
if not os.path.exists("captured_images"):
    os.makedirs("captured_images")

st.set_page_config(
    page_title="Fake Currency Detector",
    page_icon="🔍",
    layout="wide"
)

def capture_image():
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
        # Save image to local storage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"captured_images/currency_{timestamp}.jpg"
        with open(save_path, "wb") as f:
            f.write(img_file_buffer.getvalue())
        return Image.open(img_file_buffer)
    return None

def main():
    st.title("Fake Currency Detector 🔍")
    st.markdown("""
    ### Instant Currency Note Verification
    Upload an image or capture a photo to verify currency authenticity.
    For best results:
    - Ensure good lighting
    - Capture the entire note clearly
    - Keep the note flat and well-aligned
    """)

    # Input method selection
    input_method = st.radio(
        "Select input method",
        ["Upload Image", "Use Camera"],
        horizontal=True
    )

    # Denomination selection
    denomination = st.selectbox(
        "Select Currency Denomination",
        list(CURRENCY_FEATURES.keys()),
        format_func=lambda x: f"₹{x}"
    )

    image = None
    if input_method == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    else:
        image = capture_image()

    if image is not None:
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("Currency Image")
            st.image(image, use_container_width=True)

            # Show reference features
            st.markdown("### Expected Security Features")
            st.markdown(CURRENCY_FEATURES[denomination]['description'])

        with col2:
            st.subheader("Verification Process")

            # Check button
            if st.button("🔍 Check Note", type="primary"):
                try:
                    img_array = np.array(image)
                    processed_img = process_image(img_array)
                    features_found = analyze_features(processed_img, img_array)

                    # Overall confidence calculation
                    total_confidence = sum(f['confidence'] for f in features_found.values()) / len(features_found)

                    # Display confidence meter
                    st.progress(total_confidence)
                    st.metric(
                        "Overall Authenticity Score", 
                        f"{total_confidence * 100:.1f}%"
                    )

                    # Display final verdict first
                    if total_confidence > 0.7:
                        st.success("✅ HIGH CONFIDENCE: Note appears to be genuine!")
                        can_submit = True
                    elif total_confidence > 0.4:
                        st.warning("⚠️ MEDIUM CONFIDENCE: Some features need manual verification")
                        can_submit = True
                    else:
                        st.error("❌ LOW CONFIDENCE: Note requires thorough verification!")
                        can_submit = False

                    # Detailed feature analysis
                    st.markdown("### Detailed Analysis")
                    for feature, details in features_found.items():
                        with st.expander(f"{feature} Analysis"):
                            status = "✅ VERIFIED" if details['confidence'] > 0.7 else "⚠️ UNCLEAR" if details['confidence'] > 0.4 else "❌ NOT VERIFIED"
                            st.write(f"Status: {status}")
                            st.write(f"Confidence: {details['confidence']*100:.1f}%")
                            st.write(f"RBI Guideline: {SECURITY_FEATURES[feature.lower().replace(' ', '_')]['rbi_guidelines']}")

                    # Submit button (only show if confidence is medium or high)
                    if can_submit:
                        if st.button("📥 Submit Verification", type="secondary"):
                            # Save verification result
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            verification_record = {
                                'timestamp': timestamp,
                                'denomination': denomination,
                                'confidence': total_confidence,
                                'features': features_found
                            }
                            st.success("✅ Verification submitted successfully!")
                            st.balloons()

                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                    st.info("Please ensure the image is clear and properly lit.")

    # Show recent scans in a collapsible section
    if os.path.exists("captured_images") and os.listdir("captured_images"):
        st.markdown("---")
        with st.expander("Recent Scans"):
            recent_files = sorted(
                os.listdir("captured_images"),
                key=lambda x: os.path.getctime(os.path.join("captured_images", x)),
                reverse=True
            )[:5]

            cols = st.columns(len(recent_files))
            for idx, file in enumerate(recent_files):
                with cols[idx]:
                    st.image(
                        f"captured_images/{file}",
                        caption=f"Scan {idx + 1}",
                        use_container_width=True
                    )

    # Educational section
    st.markdown("---")
    with st.expander("RBI Security Features Guide"):
        st.markdown("""
        ### Official Security Features
        Learn about the key security features in different denominations:
        """)

        for denom, features in CURRENCY_FEATURES.items():
            st.markdown(f"#### ₹{denom} Note")
            st.write(features['description'])
            for feature in features['security_features']:
                st.write(f"• {feature}")

if __name__ == "__main__":
    main()