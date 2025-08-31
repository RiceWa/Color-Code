# app.py (temporary debug)
import os, sys
import streamlit as st

st.title("Debug: Streamlit is rendering ✅")

st.write("Python:", sys.version)
st.write("CWD:", os.getcwd())
st.write("Files here:", os.listdir("."))

# Try to import your module and report errors visibly
try:
    from color_codec import create_image_from_text, image_to_text
    st.success("Imported color_codec successfully.")
except Exception as e:
    st.error("Failed to import color_codec:")
    st.exception(e)




# import io
# import streamlit as st
# from PIL import Image
# from color_codec import create_image_from_text, image_to_text

# st.set_page_config(page_title="Text ↔ Image", page_icon="🧩", layout="centered")

# tab_encode, tab_decode = st.tabs(["Turn text into image", "Turn image into text"])

# # ---------- Tab 1: Text -> Image ----------
# with tab_encode:
#     st.write("")  # small spacer
#     text = st.text_area("Message", height=150, placeholder="Type or paste text…")
#     convert_enc = st.button("Convert", key="encode_btn")

#     if convert_enc:
#         if not text.strip():
#             st.warning("Please enter some text.")
#         else:
#             img = create_image_from_text(text)
#             # Preview
#             st.image(img, caption="Generated image", use_container_width=True)
#             # Download
#             buf = io.BytesIO()
#             img.save(buf, format="PNG")
#             st.download_button(
#                 "Download image",
#                 data=buf.getvalue(),
#                 file_name="encoded.png",
#                 mime="image/png",
#             )

# # ---------- Tab 2: Image -> Text ----------
# with tab_decode:
#     st.write("")  # small spacer
#     uploaded = st.file_uploader(
#         "Upload a PNG", type=["png"], accept_multiple_files=False, label_visibility="visible"
#     )  # supports drag & drop by default
#     convert_dec = st.button("Convert", key="decode_btn")

#     if convert_dec:
#         if not uploaded:
#             st.warning("Please upload a PNG.")
#         else:
#             try:
#                 text_out = image_to_text(uploaded)
#                 st.success("Decoded text:")
#                 st.text_area("Result", text_out, height=150)
#             except Exception as e:
#                 st.error(f"Failed to decode: {e}")
