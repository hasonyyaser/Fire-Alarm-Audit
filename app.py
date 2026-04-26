import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد تفاعلي", layout="wide")

st.title("نظام جرد الحساسات بالنقر - الطابق الأول")

# 1. إعداد مخزن البيانات في المتصفح
if 'points' not in st.session_state:
    st.session_state.points = []

# 2. تحميل ومعالجة الصورة
try:
    img = Image.open("floor_plan.png")
    
    # عرض الصورة وجعلها قابلة للنقر (استخدام خاصية on_click)
    # ملاحظة: سنستخدم واجهة بسيطة تلتقط إحداثيات النقر
    value = st.components.v1.html(
        f"""
        <div style="position: relative; display: inline-block;">
            <img src="https://raw.githubusercontent.com/{st.secrets.get('GITHUB_USER', 'your_user')}/{st.secrets.get('REPO_NAME', 'Fire-Alarm-Audit')}/main/floor_plan.png" 
                 style="width: 100%; cursor: crosshair;" onclick="getCoords(event)">
            <script>
                function getCoords(event) {{
                    var bounds = event.target.getBoundingClientRect();
                    var x = event.clientX - bounds.left;
                    var y = event.clientY - bounds.top;
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: {{x: x, y: y}}}}, '*');
                }}
            </script>
        </div>
        """,
        height=600,
    )
except:
    st.error("تأكد من وجود ملف floor_plan.png")

st.divider()

# 3. تسجيل البيانات بناءً على "واقع الحال"
with st.sidebar:
    st.header("تسجيل الحساس")
    st.info("انقر على مكان الحساس في المخطط أولاً، ثم اكتب الرقم هنا")
    
    sensor_id = st.text_input("رقم الحساس المختار:")
    sensor_type = st.selectbox("النوع:", ["Smoke", "Heat", "MCP", "Sounder"])
    
    if st.button("حفظ النقطة"):
        if sensor_id:
            st.session_state.points.append({
                "العنوان": sensor_id,
                "النوع": sensor_type,
                "المشروع": "الطابق الأول"
            })
            st.success(f"تم تسجيل الحساس {sensor_id}")

# 4. عرض النتائج وتصديرها
if st.session_state.points:
    df = pd.DataFrame(st.session_state.points)
    st.subheader("جدول الجرد الحالي")
    st.table(df)
    
    if st.button("تصدير إلى Excel"):
        df.to_excel("field_audit.xlsx", index=False)
        st.download_button("تحميل ملف الإكسل", data=open("field_audit.xlsx", "rb"), file_name="field_audit.xlsx")
