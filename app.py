import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="مكتب الحسنين - جرد الحساسات", layout="wide")

st.title("نظام جرد الحساسات التفاعلي - الطابق الأول")
st.write("انقر على موقع الحساس في المخطط لتسجيل رقمه (واقع الحال)")

# وظيفة لفتح الصورة وتجاوز خطأ التوافق في الـ Cloud
def get_image(path):
    try:
        return Image.open(path)
    except:
        return None

img = get_image("floor_plan.png")

if img:
    # إعدادات اللوحة التفاعلية
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        background_image=img,
        update_streamlit=True,
        height=img.height,
        width=img.width,
        drawing_mode="point",
        point_display_radius=6,
        key="fire_alarm_final",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        if not objects.empty:
            st.subheader("سجل الحساسات (واقع الحال)")
            
            # حفظ البيانات في الذاكرة المؤقتة
            if 'audit_data' not in st.session_state:
                st.session_state.audit_data = {}

            results = []
            for i, row in objects.iterrows():
                # إدخال رقم الحساس
                label = f"حساس موقع {i+1} (X:{int(row['left'])}, Y:{int(row['top'])}):"
                val = st.text_input(label, key=f"s_{i}", value=st.session_state.audit_data.get(f"s_{i}", ""))
                st.session_state.audit_data[f"s_{i}"] = val
                
                results.append({
                    "التسلسل": i + 1,
                    "رقم الحساس (واقع الحال)": val,
                    "الإحداثي الأفقي": row['left'],
                    "الإحداثي الرأسي": row['top']
                })
            
            df = pd.DataFrame(results)
            st.table(df)

            # زر الحفظ وتصدير الملف
            if st.button("تصدير إلى Excel"):
                df.to_excel("final_audit.xlsx", index=False)
                st.success("تم توليد الملف بنجاح باسم final_audit.xlsx")
else:
    st.error("تنبيه: لم يتم العثور على صورة المخطط باسم floor_plan.png في المستودع.")
