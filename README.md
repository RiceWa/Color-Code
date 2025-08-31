Color Code

An app that encodes text into PNG images and decode PNGs back into text.


Features

- Text → Image: Enter text, convert to PNG, download.
- Image → Text: Upload PNG, decode original text.
- Uses RGB pixels to store UTF-8 data with a simple header.


How It Works

- Encoding: Text → bytes → RGB pixels → minimal square PNG.
- Decoding: Reads header for length, reconstructs exact text.
- UI: Two tabs: Encode (textbox) and Decode (upload + drag-and-drop).

---
If you want to run it locally

```
git clone https://github.com/RiceWa/Color-Code.git
cd Color-Code
pip install -r requirements.txt
streamlit run app.py
```
