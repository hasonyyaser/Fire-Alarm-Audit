import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="مكتب الحسنين - جرد تفاعلي", layout="wide")

st.title("نظام جرد الحساسات التفاعلي - الطابق الأول")
st.write("انقر على موقع الحساس في المخطط لتسجيل رقمه")

# 1. تحميل صورة المخطط (تأكد من وجود الملف floor_plan.jpg أو png)
image_path = "floor_plan.jpg" 
try:
    img = Image.open(image_path)
except:
    image_path = "floor_plan.png"
    try:
        img = Image.open(image_path)
    except:
        st.error("لم يتم العثور على صورة المخطط. تأكد من رفعها باسم floor_plan.jpg أو floor_plan.png")
        st.stop()

# 2. عرض المخطط واستقبال إحداثيات النقر مباشرة
# هذه الخاصية (label_visibility) تجعل الصورة قابلة للنقر وتخزن الإحداثيات في 'value'
clicked_coords = st.image(img, use_container_width=True)

# 3. إعداد مخزن البيانات
if 'sensor_records' not in st.session_state:
    st.session_state.sensor_list = []

# 4. واجهة إدخال البيانات في القائمة الجانبية
with st.sidebar:
    st.header("إضافة حساس جديد")
    st.info("سجل الرقم والملاحظات بناءً على ما جردته في الموقع")
    
    new_id = st.text_input("رقم الحساس (مثلاً: 4.15)")
    new_note = st.text_area("ملاحظات الموقع")
    
    if st.button("حفظ الحساس في القائمة"):
        if new_id:
            st.session_state.sensor_list.append({
                "العنوان (Address)": new_id,
                "الملاحظات": new_note
            })
            st.success(f"تم إضافة الحساس {new_id}")

# 5. عرض النتائج وتصديرها
if st.session_state.sensor_list:
    df = pd.DataFrame(st.session_state.sensor_list)
    st.subheader("جدول الجرد الحالي")
    st.dataframe(df, use_container_width=True)
    
    if st.button("تصدير إلى Excel"):
        df.to_excel("sensor_audit.xlsx", index=False)
        with open("sensor_audit.xlsx", "rb") as f:
            st.download_button("تحميل ملف الإكسل", f, file_name="sensor_audit.xlsx")

if st.button("مسح الجدول والبدء من جديد"):
    st.session_state.sensor_list = []
    st.rerun()
