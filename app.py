# app.py
import streamlit as st
st.set_page_config(page_title="Text ↔ Image", page_icon="🧩", layout="centered")

try:
    import io
    from color_codec import create_image_from_text, image_to_text

    tab_encode, tab_decode = st.tabs(["Turn text into image", "Turn image into text"])

    # ---- Tab 1: Text -> Image ----
    with tab_encode:
        text = st.text_area("Message", height=150, placeholder="Type or paste text…")
        if st.button("Convert", key="encode_btn"):
            if not text.strip():
                st.warning("Please enter some text.")
            else:
                img = create_image_from_text(text)
                st.image(img, caption="Generated image", width=True)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("Download image", buf.getvalue(),
                                   file_name="encoded.png", mime="image/png")

    # ---- Tab 2: Image -> Text ----
    with tab_decode:
        uploaded = st.file_uploader("Upload a PNG", type=["png"])
        if st.button("Convert", key="decode_btn"):
            if not uploaded:
                st.warning("Please upload a PNG.")
            else:
                try:
                    text_out = image_to_text(uploaded)
                    st.success("Decoded text:")
                    st.text_area("Result", text_out, height=150)
                except Exception as e:
                    st.error("Failed to decode:")
                    st.exception(e)

except Exception as e:
    st.error("App failed to load:")
    st.exception(e)
