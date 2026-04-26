import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد تفاعلي", layout="wide")

st.title("نظام جرد الحساسات - الطابق الأول")

# 1. تحميل الصورة محلياً من المستودع لضمان ظهورها
try:
    bg_image = Image.open("floor_plan.png")
except:
    st.error("تنبيه: لم يتم العثور على ملف floor_plan.png. تأكد من رفعه في نفس المستودع.")
    st.stop()

# 2. إعداد اللوحة التفاعلية (بإصدار متوافق)
st.write("انقر على موقع الحساس في المخطط أدناه:")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # لون النقطة عند النقر
    stroke_width=2,
    background_image=bg_image,
    update_streamlit=True,
    height=bg_image.height,
    width=bg_image.width,
    drawing_mode="point", # وضع النقر فقط
    point_display_radius=5,
    key="fire_alarm_audit",
)

# 3. معالجة النقاط التي تم النقر عليها
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    if not objects.empty:
        st.subheader("سجل الحساسات (واقع الحال)")
        
        if 'audit_results' not in st.session_state:
            st.session_state.audit_results = {}

        final_data = []
        for index, row in objects.iterrows():
            # إنشاء مفتاح فريد لكل نقطة بناءً على مكانها
            pos_id = f"pos_{int(row['left'])}_{int(row['top'])}"
            
            # حقل إدخال رقم الحساس بجانب إحداثياته
            val = st.text_input(
                f"أدخل رقم الحساس للنقطة في الموقع ({int(row['left'])}, {int(row['top'])}):",
                key=pos_id,
                value=st.session_state.audit_results.get(pos_id, "")
            )
            st.session_state.audit_results[pos_id] = val
            
            final_data.append({
                "رقم الحساس": val,
                "إحداثي X": row['left'],
                "إحداثي Y": row['top']
            })

        # 4. عرض الجدول وتصديره
        df = pd.DataFrame(final_data)
        st.dataframe(df)

        if st.button("تصدير النتائج إلى Excel"):
            df.to_excel("sensor_audit_final.xlsx", index=False)
            st.success("تم توليد الملف بنجاح")
