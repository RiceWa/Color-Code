Color Code

An app that encodes text into PNG images and decode PNGs back into text.


Features

- Text → Image: Enter text, convert to PNG, download.
- Image → Text: Upload PNG, decode text.
- Uses RGB to store UTF-8 characters.


How It Works

- Encoding: Text → bytes → RGB pixels → stores as a minimal square PNG.
- Decoding: Reads header for length and reconstructs the exact text.

---
If you want to run it locally

```
git clone https://github.com/RiceWa/Color-Code.git
cd Color-Code
pip install -r requirements.txt
streamlit run app.py
```
