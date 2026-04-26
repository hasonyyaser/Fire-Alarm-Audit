import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد الحساسات", layout="wide")

st.title("نظام جرد الحساسات - الطابق الأول")
st.info("قم بمعاينة المخطط أدناه، ثم سجل أرقام الحساسات حسب واقع الحال")

# 1. عرض المخطط للمعاينة فقط
try:
    img = Image.open("floor_plan.png")
    st.image(img, caption="مخطط الطابق الأول - مكتب الحسنين", use_container_width=True)
except:
    st.error("تنبيه: لم يتم العثور على صورة floor_plan.png")

st.divider()

# 2. واجهة إدخال البيانات (واقع الحال)
st.subheader("تسجيل الحساسات المربوطة فعلياً")

# استخدام session_state لحفظ القائمة
if 'sensor_list' not in st.session_state:
    st.session_state.sensor_list = []

# نموذج إضافة حساس جديد
with st.form("sensor_form"):
    col1, col2 = st.columns(2)
    with col1:
        s_id = st.text_input("رقم الحساس (مثال: 4.12)")
    with col2:
        s_note = st.text_input("ملاحظات (مثال: الغرفة رقم 5)")
    
    submit = st.form_submit_button("إضافة الحساس للقائمة")
    if submit and s_id:
        st.session_state.sensor_list.append({"رقم الحساس": s_id, "الملاحظات": s_note})

# 3. عرض الجدول الحالي
if st.session_state.sensor_list:
    df = pd.DataFrame(st.session_state.sensor_list)
    st.table(df)
    
    # 4. تصدير البيانات إلى إكسل
    if st.button("تصدير الجدول إلى Excel"):
        df.to_excel("sensor_audit_final.xlsx", index=False)
        st.success("تم حفظ الملف بنجاح")

if st.button("مسح القائمة والبدء من جديد"):
    st.session_state.sensor_list = []
    st.rerun()
