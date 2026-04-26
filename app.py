import streamlit as st
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.set_page_config(page_title="مكتب الحسنين - جرد تفاعلي", layout="wide")

st.title("نظام جرد الحساسات - الطابق الأول")

# دالة لتحميل الصورة بصيغة متوافقة جداً
def load_and_fix_image(path):
    try:
        img = Image.open(path)
        # تحويل الصورة إلى RGB للتخلص من أي قنوات زائدة (مثل الشفافية في PNG)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return img
    except:
        return None

# حاول تحميل الصورة بالامتداد الجديد
bg_image = load_and_fix_image("floor_plan.jpg")

if bg_image:
    st.write("انقر على المخطط لتحديد موقع الحساس:")
    
    # استخدام اللوحة التفاعلية
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.4)",
        stroke_width=2,
        background_image=bg_image, # هنا السطر الحساس، قمنا بتنظيف الصورة قبله
        update_streamlit=True,
        height=bg_image.height,
        width=bg_image.width,
        drawing_mode="point",
        point_display_radius=5,
        key="fire_alarm_final_fix",
    )

    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        if not objects.empty:
            st.subheader("تسجيل الحساسات (واقع الحال)")
            
            if 'results' not in st.session_state:
                st.session_state.results = {}

            export_list = []
            for i, row in objects.iterrows():
                key = f"pt_{int(row['left'])}_{int(row['top'])}"
                val = st.text_input(f"رقم الحساس في الموقع ({int(row['left'])}, {int(row['top'])}):", 
                                   key=key, value=st.session_state.results.get(key, ""))
                st.session_state.results[key] = val
                
                export_list.append({"رقم الحساس": val, "X": row['left'], "Y": row['top']})
            
            df = pd.DataFrame(export_list)
            st.dataframe(df)

            if st.button("حفظ الجدول النهائي"):
                df.to_excel("audit_report.xlsx", index=False)
                st.success("تم الحفظ!")
else:
    st.error("تنبيه: لم يتم العثور على floor_plan.jpg. يرجى التأكد من تغيير الامتداد ورفع الملف.")
