import streamlit as st
import io
from PIL import Image
import google.generativeai as genai

# ตั้งค่า API Key
genai.configure(api_key="AIzaSyDnM52XbrNnpqvKWDPThwDTiX7XjcOhRVU")

# โหลดโมเดล
model_vision = genai.GenerativeModel("gemini-pro-vision")
model_translation = genai.GenerativeModel("gemini-pro")

# ตั้งค่า Streamlit
st.title("โปรแกรมแปลภาษาจากรูปภาพ")

# อัพโหลดไฟล์ภาพ
img_file = st.file_uploader("เปิดไฟล์ภาพ")

description = None  # กำหนดค่าเริ่มต้นให้ description เป็น None

if img_file is not None:
    imagefile = io.BytesIO(img_file.read())
    img = Image.open(imagefile)
    st.image(img, channels="BGR")  # แสดงผลภาพ

    # บรรยายภาพ
    prompt = "ในภาพนี้มีข้อความอะไรบ้าง"

    ch = st.selectbox("เลือกภาษาปลายทาง", ("ไทย", "อังกฤษ", "เกาหลี", "ญี่ปุ่น", "จีน"))
    
    if st.button("ค้นหาข้อความและแปลภาษา"):
        try:
            response = model_vision.generate_content([img, prompt])
            if hasattr(response, 'text'):
                description = response.text  # เก็บข้อความบรรยายภาพ
                st.subheader("ข้อความที่พบ")
                st.text(description)
                text_in = description  # ใช้ข้อความบรรยายภาพเป็นค่าเริ่มต้น
            else:
                st.text("ไม่สามารถบรรยายภาพได้")
                description = None
        except Exception as e:
            st.text(f"Error: {e}")
            description = None

# ส่วนของการแปลภาษา
st.subheader("แปลภาษา")

if description is not None:
    try:
        prompt_translation = f"แปลข้อความต่อไปนี้เป็นภาษา {ch} {description}"
        response1 = model_translation.generate_content(prompt_translation)
        if hasattr(response1, 'text'):
            st.text(response1.text)  # แสดงผลข้อความที่ได้จากการแปล
        else:
            st.text("ไม่สามารถแปลข้อความได้")
    except Exception as e:
        st.text(f"Error: {e}")
else:
    st.text("กรุณาอัพโหลดและบรรยายภาพก่อนที่จะแปลภาษา")
