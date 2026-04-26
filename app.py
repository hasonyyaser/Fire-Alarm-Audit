import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد الحساسات", layout="wide")

st.title("نظام جرد الحساسات التفاعلي - الطابق الأول")
st.write("انقر على موقع الحساس في المخطط لتسجيل رقمه (واقع الحال)")

# تحميل صورة المخطط مع التأكد من وجودها
try:
    bg_image = Image.open("floor_plan.png")
except FileNotFoundError:
    st.error("خطأ: لم يتم العثور على ملف floor_plan.png. تأكد من رفعه على GitHub بنفس المجلد.")
    st.stop()

# إعدادات لوحة الرسم التفاعلية (نسخة محدثة)
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=2,
    background_image=bg_image,
    update_streamlit=True,
    height=bg_image.height,
    width=bg_image.width,
    drawing_mode="point",
    point_display_radius=5,
    key="canvas",
)

# معالجة البيانات المسجلة
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    if not objects.empty:
        st.subheader("قائمة الحساسات المسجلة")
        
        # إنشاء جدول لتخزين أرقام الحساسات
        if 'sensor_data' not in st.session_state:
            st.session_state.sensor_data = {}

        for index, row in objects.iterrows():
            pos_key = f"{row['left']}_{row['top']}"
            st.session_state.sensor_data[pos_key] = st.text_input(
                f"أدخل رقم الحساس للنقطة في الموقع ({int(row['left'])}, {int(row['top'])}):", 
                value=st.session_state.sensor_data.get(pos_key, ""),
                key=f"input_{pos_key}"
            )
        
        # تحويل البيانات لجدول قابل للتصدير
        export_data = []
        for index, row in objects.iterrows():
            pos_key = f"{row['left']}_{row['top']}"
            export_data.append({
                "X": row['left'],
                "Y": row['top'],
                "Sensor_ID": st.session_state.sensor_data.get(pos_key, "")
            })
        
        df_final = pd.DataFrame(export_data)
        st.dataframe(df_final)

        if st.button("تصدير جدول الحساسات إلى Excel"):
            df_final.to_excel("sensor_audit.xlsx", index=False)
            st.success("تم حفظ الملف باسم sensor_audit.xlsx")
