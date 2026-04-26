import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.set_page_config(page_title="مكتب الحسنين - جرد الحساسات", layout="wide")

st.title("نظام جرد الحساسات التفاعلي - الطابق الأول")
st.write("انقر على موقع الحساس في المخطط لتسجيل رقمه (واقع الحال)")

# وظيفة لتحميل الصورة بشكل متوافق مع Streamlit Cloud
def load_image(image_path):
    try:
        img = Image.open(image_path)
        # تحويل الصورة لتكون متوافقة مع العرض
        return img
    except FileNotFoundError:
        return None

bg_image = load_image("floor_plan.png")

if bg_image:
    # إعدادات لوحة الرسم التفاعلية المحدثة
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        background_image=bg_image,
        update_streamlit=True,
        height=bg_image.height,
        width=bg_image.width,
        drawing_mode="point",
        point_display_radius=5,
        key="fire_alarm_canvas",
    )

    # معالجة البيانات المسجلة
    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        if not objects.empty:
            st.subheader("قائمة الحساسات المسجلة")
            
            # استخدام session_state لحفظ الأرقام أثناء العمل
            if 'sensors' not in st.session_state:
                st.session_state.sensors = {}

            export_data = []
            for index, row in objects.iterrows():
                key = f"pt_{index}"
                st.session_state.sensors[key] = st.text_input(
                    f"رقم الحساس للنقطة {index+1}:", 
                    value=st.session_state.sensors.get(key, ""),
                    key=f"input_{key}"
                )
                export_data.append({
                    "رقم اللوب والحساس": st.session_state.sensors[key],
                    "إحداثيات X": row['left'],
                    "إحداثيات Y": row['top']
                })
            
            df = pd.DataFrame(export_data)
            st.table(df)

            # تصدير البيانات
            if st.button("تصدير الجدول إلى Excel"):
                df.to_excel("audit_results.xlsx", index=False)
                st.success("تم حفظ النتائج في ملف audit_results.xlsx")
else:
    st.error("لم يتم العثory على ملف floor_plan.png. تأكد من وجود الصورة في المستودع بنفس الاسم.")
