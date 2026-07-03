import streamlit as st
import io
import base64
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import segno

# =====================================================================
# GLOBAL CONFIGURATION & STYLING
# =====================================================================
st.set_page_config(
    page_title="Production Studio & QR Engine",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for professional UI rendering
st.markdown("""
    <style>
    .reportview-container { background: #f5f7f9; }
    .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)


# =====================================================================
# UTILITY & FILTER ENGINE FUNCTIONS
# =====================================================================
def apply_sepia(img):
    """Applies a high-fidelity matrix-based sepia tone filter."""
    img = img.convert("RGB")
    sepia_matrix = (
        0.393, 0.769, 0.189, 0,
        0.349, 0.686, 0.168, 0,
        0.272, 0.534, 0.131, 0
    )
    return img.convert("RGB", sepia_matrix)


# =====================================================================
# WORKSPACE NAVIGATION
# =====================================================================
st.sidebar.title("🚀 Navigation Control")
workspace_mode = st.sidebar.radio(
    "Select Workspace Environment:",
    ["🎨 Advanced Image Studio", "🔮 Universal QR Engine"]
)
st.sidebar.markdown("---")


# =====================================================================
# MODE A: ADVANCED IMAGE STUDIO
# =====================================================================
if workspace_mode == "🎨 Advanced Image Studio":
    st.title("🎨 Advanced Image Studio")
    st.markdown("Perform high-fidelity structural transformations, color grading operations, and real-time payload compression benchmarks.")
    st.markdown("---")

    uploaded_image_file = st.file_uploader(
        "Upload Source Asset", 
        type=["png", "jpg", "jpeg"],
        help="Supported formats: PNG, JPG, JPEG"
    )

    if uploaded_image_file is not None:
        try:
            # Load initial image configuration
            original_img = Image.open(uploaded_image_file)
            orig_w, orig_h = original_img.size
            
            # Setup layout grids for control canvas
            control_col, display_col = st.columns([1, 2])
            
            with control_col:
                st.subheader("🛠️ Studio Canvas Controls")
                
                # 1. Filter Panel Selector
                st.markdown("### 1. Filter Pipelines")
                filter_state = st.selectbox(
                    "Choose Creative Filter State:",
                    [
                        "Original", "Black & White", "Sepia Tone", 
                        "Gaussian Blur", "Contour Sketch", 
                        "Vibrant Saturation", "Retro Negative", "Emboss Art"
                    ]
                )
                
                # 2. Structural Manipulation Tools (Crop)
                st.markdown("### 2. Direct Slice Boundaries (Crop)")
                crop_left = st.number_input("Left Cut (px)", min_value=0, max_value=orig_w-1, value=0)
                crop_top = st.number_input("Top Cut (px)", min_value=0, max_value=orig_h-1, value=0)
                crop_right = st.number_input("Right Boundary (px)", min_value=crop_left+1, max_value=orig_w, value=orig_w)
                crop_bottom = st.number_input("Bottom Boundary (px)", min_value=crop_top+1, max_value=orig_h, value=orig_h)
                
                # 3. Scale Layout Tools (Resize)
                st.markdown("### 3. Canvas Resizing dimensions")
                resize_w = st.number_input("Target Width (px)", min_value=1, max_value=8000, value=orig_w)
                resize_h = st.number_input("Target Height (px)", min_value=1, max_value=8000, value=orig_h)
                
                # 4. Storage Engine & Dynamic Compression Optimization
                st.markdown("### 4. Byte Weight Optimization")
                compression_quality = st.slider(
                    "Target Quality Metric (1-100):", 
                    min_value=1, 
                    max_value=100, 
                    value=85,
                    help="Lower values reduce file size significantly at the cost of fidelity."
                )

            with display_col:
                st.subheader("📋 Studio Pipeline Pipeline Monitoring")
                
                # Execution Shield Block for heavy operations
                try:
                    # Step A: Apply Crop Slicing safely
                    working_img = original_img.crop((crop_left, crop_top, crop_right, crop_bottom))
                    
                    # Step B: Apply Matrix Resizing
                    working_img = working_img.resize((resize_w, resize_h), Image.Resampling.LANCZOS)
                    
                    # Step C: Apply Selected Image Convolution Filters
                    if filter_state == "Black & White":
                        working_img = ImageOps.grayscale(working_img)
                    elif filter_state == "Sepia Tone":
                        working_img = apply_sepia(working_img)
                    elif filter_state == "Gaussian Blur":
                        working_img = working_img.filter(ImageFilter.GaussianBlur(radius=4))
                    elif filter_state == "Contour Sketch":
                        working_img = working_img.filter(ImageFilter.CONTOUR)
                    elif filter_state == "Vibrant Saturation":
                        working_img = ImageEnhance.Color(working_img).enhance(2.5)
                    elif filter_state == "Retro Negative":
                        working_img = ImageOps.invert(working_img.convert("RGB"))
                    elif filter_state == "Emboss Art":
                        working_img = working_img.filter(ImageFilter.EMBOSS)
                    
                    # Compute Dynamic Compression Metrics
                    output_buffer = io.BytesIO()
                    # Convert to RGB if saving as JPEG to avoid format errors
                    save_img = working_img.convert("RGB") if filter_state != "Black & White" else working_img
                    save_img.save(output_buffer, format="JPEG", quality=compression_quality)
                    processed_bytes = output_buffer.getvalue()
                    
                    original_size_kb = uploaded_image_file.size / 1024
                    processed_size_kb = len(processed_bytes) / 1024
                    
                    # Render Metric Analysis Trackers
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    metric_col1.metric("Original Data Weight", f"{original_size_kb:.2f} KB")
                    metric_col2.metric("Optimized Data Weight", f"{processed_size_kb:.2f} KB")
                    metric_col3.metric("Data Footprint Delta", f"{(processed_size_kb - original_size_kb):.2f} KB")
                    
                    # Comparative Visual Display Frame
                    view_col1, view_col2 = st.columns(2)
                    with view_col1:
                        st.markdown("**Original Reference Grid:**")
                        st.image(original_img, use_container_width=True)
                    with view_col2:
                        st.markdown("**Processed Production Output:**")
                        st.image(working_img, use_container_width=True)
                        
                    # Export Action Interface
                    st.markdown("---")
                    st.download_button(
                        label="💾 Download Processed Output File",
                        data=processed_bytes,
                        file_name="studio_production_output.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                    
                except Exception as processing_error:
                    st.error(f"🚨 Pipeline Processing Disruption: {str(processing_error)}")
                    
        except Exception as file_read_error:
            st.error(f"🚨 Source File Parse Fault: {str(file_read_error)}")
    else:
        st.info("💡 Awaiting source configuration. Upload a target graphic file to initialize the workspace.")


# =====================================================================
# MODE B: UNIVERSAL QR ENGINE
# =====================================================================
else:
    st.title("🔮 Universal QR Engine")
    st.markdown("Generate highly stable, high-density matrix configurations supporting raw literals, URL targets, and inline Base64 graphics data pools.")
    st.markdown("---")
    
    # Styling Overrides via Sidebar Color Panels
    st.sidebar.subheader("🎨 Matrix Styling Configurations")
    line_color = st.sidebar.color_picker("Line / Matrix Module Color (Dark)", value="#000000")
    bg_color = st.sidebar.color_picker("Background Canvas Color (Light)", value="#FFFFFF")
    
    # Engine Pipeline Selection Layout
    qr_pipeline = st.tabs(["📝 Text to QR", "🔗 Link to QR", "🖼️ Image to QR Pipeline"])
    
    payload_string = ""
    is_pipeline_ready = False
    
    # Pipeline 1: Text to QR
    with qr_pipeline[0]:
        st.markdown("### Raw Structural Text Matrix")
        raw_text_input = st.text_area(
            "Enter Literal Paragraph Payload:", 
            placeholder="Type your safe alphanumeric string content here..."
        )
        if raw_text_input.strip() != "":
            payload_string = raw_text_input
            is_pipeline_ready = True
            
    # Pipeline 2: Link to QR
    with qr_pipeline[1]:
        st.markdown("### Native URI Link Engine Target")
        url_input = st.text_input(
            "Enter Absolute Target URL:", 
            placeholder="https://example.com/production-portal"
        )
        if url_input.strip() != "":
            payload_string = url_input
            is_pipeline_ready = True
            
    # Pipeline 3: Image to QR Engine (Base64 Inline Data Block Converter)
    with qr_pipeline[2]:
        st.markdown("### Binary Image to High-Capacity Data URI Encoder")
        st.warning(
            "⚠️ Architecture Notice: QR matrices have a definitive absolute upper limit storage footprint (~2.9 KB). "
            "Uploaded assets will automatically be heavily optimized and scaled to safely compile inside the matrix architecture."
        )
        qr_image_file = st.file_uploader(
            "Select Sub-Asset Image Element", 
            type=["png", "jpg", "jpeg"],
            key="qr_image_uploader"
        )
        
        if qr_image_file is not None:
            try:
                # Shield block to process image downscaling for QR compliance
                temp_img = Image.open(qr_image_file)
                # Scale down aggressively to fit QR matrix size restrictions
                temp_img.thumbnail((40, 40)) 
                
                img_ram_buffer = io.BytesIO()
                temp_img.save(img_ram_buffer, format="JPEG", quality=50)
                b64_encoded_str = base64.b64encode(img_ram_buffer.getvalue()).decode("utf-8")
                
                payload_string = f"data:image/jpeg;base64,{b64_encoded_str}"
                is_pipeline_ready = True
                
                st.success("🎉 Asset successfully compressed and converted into standard inline Base64 URI layout string.")
                st.text_area("Generated Matrix Payload String Preview", value=payload_string, height=100, disabled=True)
            except Exception as b64_fault:
                st.error(f"🚨 Matrix String Compilation Failure: {str(b64_fault)}")

    # Unified Generation and Rendering Engine Pipeline
    if is_pipeline_ready:
        st.markdown("### 🔍 Matrix Compilation Engine Status")
        
        try:
            # Build QR Code using Segno matrix layouts
            compiled_qr = segno.make(payload_string, error='L')
            
            # Write out to visual RAM pipeline stream
            qr_render_stream = io.BytesIO()
            compiled_qr.save(
                qr_render_stream, 
                kind='png', 
                scale=10, 
                dark=line_color, 
                light=bg_color
            )
            qr_bytes = qr_render_stream.getvalue()
            
            # Display Outputs structured cleanly on UI
            out_col1, out_col2 = st.columns([1, 2])
            with out_col1:
                st.markdown("**Compiled QR Target Card:**")
                st.image(qr_bytes, width=320, output_format="PNG")
            
            with out_col2:
                st.markdown("**Engine Compilation Properties:**")
                st.info(f"🔹 **Matrix Version Size:** {compiled_qr.version}")
                st.info(f"🔹 **Error Mitigation Threshold:** Level L (Low Standard)")
                st.info(f"🔹 **Raw Payload String Footprint Size:** {len(payload_string)} Characters")
                
                # Download Action block wrapper
                st.download_button(
                    label="💾 Download Generated Matrix Asset (.png)",
                    data=qr_bytes,
                    file_name="universal_qr_matrix.png",
                    mime="image/png",
                    use_container_width=True
                )
                
        except segno.DataOverflowError:
            st.error("🚨 Matrix Compilation Error: The input data block weight is too massive to structurally reside inside a unified QR matrix array.")
        except Exception:
