import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد الحساسات", layout="wide")

st.title("نظام جرد الحساسات - الطابق الأول")

# عرض المخطط للمعاينة
try:
    img = Image.open("floor_plan.png")
    st.image(img, caption="استخدم المخطط لمعرفة مواقع الحساسات", use_container_width=True)
except:
    st.error("تنبيه: ملف floor_plan.png غير موجود")

st.divider()

# واجهة الإدخال السريع
st.subheader("تسجيل الحساسات (واقع الحال)")

if 'sensor_list' not in st.session_state:
    st.session_state.sensor_list = []

with st.form("quick_input"):
    col1, col2, col3 = st.columns(3)
    with col1:
        # إضافة اختيار اللوب لتسهيل الترقيم
        loop_no = st.selectbox("رقم اللوب", ["3", "4", "5"])
    with col2:
        s_id = st.text_input("رقم الحساس (مثلاً: 12)")
    with col3:
        s_type = st.selectbox("نوع الجهاز", ["Smoke", "Heat", "MCP", "Sounder"])
    
    submit = st.form_submit_button("إضافة إلى القائمة")
    
    if submit and s_id:
        full_address = f"{loop_no}.{s_id}"
        st.session_state.sensor_list.append({
            "العنوان (Address)": full_address,
            "النوع": s_type,
            "الحالة": "تم الجرد"
        })

# عرض الجدول وتصديره
if st.session_state.sensor_list:
    df = pd.DataFrame(st.session_state.sensor_list)
    st.table(df)
    
    if st.button("تصدير الجدول إلى Excel"):
        df.to_excel("final_audit.xlsx", index=False)
        st.success("تم توليد ملف final_audit.xlsx بنجاح")
