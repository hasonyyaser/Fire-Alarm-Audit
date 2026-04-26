import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد الحساسات", layout="wide")

st.title("نظام جرد الحساسات - الطابق الأول")

# 1. عرض المخطط كمرجع بصري (بدون مكتبات تفاعلية معقدة)
try:
    img = Image.open("floor_plan.png")
    st.image(img, caption="مخطط الحريق - الطابق الأول", use_container_width=True)
except:
    st.error("يرجى التأكد من وجود ملف floor_plan.png في المستودع")

st.divider()

# 2. واجهة إدخال البيانات (واقع الحال)
st.subheader("تسجيل بيانات الحساسات ميدانياً")

if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = []

# نموذج الإدخال
with st.form("audit_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        loop = st.selectbox("اللوب (Loop)", ["3", "4", "5"])
    with col2:
        addr = st.text_input("رقم الحساس (Address)")
    with col3:
        s_type = st.selectbox("النوع", ["Smoke", "Heat", "MCP", "Sounder", "Module"])
    
    note = st.text_input("وصف الموقع (مثلاً: غرفة المدير، الممر الرئيسي)")
    
    if st.form_submit_button("إضافة الحساس للقائمة"):
        if addr:
            st.session_state.sensor_data.append({
                "العنوان الكامل": f"{loop}.{addr}",
                "النوع": s_type,
                "الموقع/الملاحظات": note
            })
            st.success(f"تم تسجيل الحساس {loop}.{addr}")

# 3. عرض الجدول وتصديره
if st.session_state.sensor_data:
    df = pd.DataFrame(st.session_state.sensor_data)
    st.dataframe(df, use_container_width=True)
    
    # زر الحفظ المباشر
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="تحميل ملف الجرد (CSV) للاكسل",
        data=csv,
        file_name='fire_alarm_audit.csv',
        mime='text/csv',
    )

if st.button("مسح البيانات والبدء من جديد"):
    st.session_state.sensor_data = []
    st.rerun()
