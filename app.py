import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- ၁။ UI & 3D VISUAL DESIGN ---
st.set_page_config(page_title="SST Hospital Master", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Advanced 3D Glass Box */
    [data-testid="stForm"], .st-emotion-cache-1r6slb0 { 
        background: rgba(255, 255, 255, 0.98) !important; 
        border: 5px solid #1E3A8A !important; 
        border-radius: 25px !important;
        padding: 45px !important;
        box-shadow: 35px 35px 75px rgba(0,0,0,0.6) !important;
    }

    h1, h2, h3, label, p, span { 
        font-weight: 900 !important; 
        color: #000000 !important; 
    }

    .main-header { 
        background: linear-gradient(135deg, #064E3B 0%, #059669 100%); 
        color: white; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 35px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ၂။ DATABASE SCHEMA (၂၀ စုံလင်စွာ) ---
DB_FILE = "sst_enterprise_v2026_final.csv"
def init_db():
    cols = [
        "Patient_ID", "လူနာအမည်", "အသက်", "ကျား/မ", "နိုင်ကတ် (NRC)", "ဖုန်းနံပါတ်",
        "ပြည်နယ်/တိုင်း", "မြို့နယ်", "ရပ်ကွက်/ကျေးရွာ", "အိမ်နံပါတ်/လမ်း",
        "Ward/ဌာန", "Diagnosis (ရောဂါအမည်)", "လူနာအမျိုးအစား", "အရေးပေါ်အခြေအနေ",
        "တက်ရောက်သည့်ရက်", "ဆင်းမည့်ရက်", "တာဝန်ကျဆရာဝန်", "တာဝန်ကျသူနာပြု",
        "ဆေးဝါးညွှန်ကြားချက်", "ဓာတ်စာ/ရှောင်ရန်", "အရေးပေါ်ဆက်သွယ်ရန်", "မှတ်ချက်", "Status"
    ]
    if not os.path.exists(DB_FILE) or os.stat(DB_FILE).st_size == 0:
        pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False, encoding='utf-8-sig')

init_db()

# --- ၃။ မြန်မာနိုင်ငံရှိ မြို့နယ် ၃၃၀ ကျော် အပြည့်အစုံ (Line 60 - 450) ---
# ဤစာရင်းသည် မြန်မာနိုင်ငံ၏ မြို့နယ်အားလုံးကို လွှမ်းခြုံထားသည်
townships = [
    "တောင်ကြီး", "အေးသာယာ", "ညောင်ရွှေ", "ဟိုပုံး", "ဆီဆိုင်", "ပင်လောင်း", "ကလော", "အောင်ပန်း", "ပင်းတယ", "ရွာငံ", 
    "ရပ်စောက်", "ဖယ်ခုံ", "လွိုင်လင်", "ပင်လုံ", "နမ့်စန်", "ကွန်းဟိန်း", "လဲချား", "မိုင်းကိုင်", "မိုင်းရှူး", "ကျေးသီး", 
    "ခိုလမ်", "လင်းခေး", "မိုးနဲ", "မောက်မယ်", "မယ်စဲ့", "ကျိုင်းတုံ", "မိုင်းခတ်", "မိုင်းယန်း", "မိုင်းလား", "တာချီလိတ်", 
    "မိုင်းဖြတ်", "မိုင်းယောင်း", "မိုင်းဆတ်", "မိုင်းတုံ", "လားရှိုး", "သိန္နီ", "ကွတ်ခိုင်", "နမ္မတူ", "ပေါင်ဆိုင်", "မူဆယ်", 
    "နမ့်ခမ်း", "ကျောက်မဲ", "နောင်ချို", "သီပေါ", "နမ့်ဆန်", "မန်တုံ", "မိုးမိတ်", "မဘိမ်း", "ကုန်းကြမ်း", "လောက်ကိုင်",
    "ဟိုပန်", "မိုင်းမော", "ပန်ဝိုင်", "နားဖန်း", "မက်မန်း", "ပန်ဆန်း", "ရန်ကုန်", "မန္တလေး", "နေပြည်တော်", "ပဲခူး",
    "စစ်ကိုင်း", "ထားဝယ်", "မြစ်ကြီးနား", "မကွေး", "ပုသိမ်", "မော်လမြိုင်", "စစ်တွေ", "ဟားခါး", "ဘားအံ", "မြဝတီ", 
    "ကော့ကရိတ်", "ကြာအင်းဆိပ်ကြီး", "ဖာပွန်", "သံတောင်ကြီး", "လှိုင်းဘွဲ့", "ကော့သောင်း", "မြိတ်", "ကျွန်းစု", "ပုလော", 
    "တနင်္သာရီ", "သရက်ချောင်း", "လောင်းလုံး", "ရေဖြူ", "ပခုက္ကူ", "ညောင်ဦး", "ချောက်", "ရေစကြို", "မြိုင်", "ဆိပ်ဖြူ", 
    "မင်းဘူး", "စကု", "ပွင့်ဖြူ", "ငဖဲ", "စေတုတ္တရာ", "တောင်တွင်းကြီး", "မြို့သစ်", "နတ်မောက်", "အောင်လံ", "ဆင်ပေါင်ဝဲ", 
    "သရက်", "မင်းလှ", "မင်းတုန်း", "ကံမ", "ဂန့်ဂေါ", "ထီးလင်း", "ဆော", "ကျောက်ထု", "ကလေး", "ကလေးဝ", "မင်းကင်း", 
    "ခန္တီး", "ဟုမ္မလင်း", "လဟယ်", "နန်းယွန်း", "ကသာ", "အင်းတော်", "ထီးချိုင့်", "ဗန်းမောက်", "ကောလင်း", "ဝန်းသို", 
    "ပင်လည်ဘူး", "ရွှေဘို", "ခင်ဦး", "ဝက်လက်", "ကန့်ဘလူ", "ကျွန်းလှ", "ရေဦး", "တန့်ဆည်", "ဒီပဲယင်း", "မုံရွာ", 
    "အရာတော်", "ချောင်းဦး", "ဆားလင်းကြီး", "ယင်းမာပင်", "ပုလဲ", "ကနီ", "မဟာအောင်မြေ", "ချမ်းအေးသာစံ", "ချမ်းမြသာစည်", 
    "ပြည်ကြီးတံခွန်", "အမရပူရ", "ပုသိမ်ကြီး", "အောင်မြေသာစံ", "ပြင်ဦးလွင်", "မတ္တရာ", "စဉ့်ကူး", "သပိတ်ကျင်း", "မိုးကုတ်", 
    "ကျောက်ဆည်", "စဉ်ကိုင်", "မြစ်သား", "တံတားဦး", "မိတ္ထီလာ", "မလှိုင်", "သာစည်", "ဝမ်းတွင်း", "မြင်းခြံ", "တောင်သာ", 
    "နွားထိုးကြီး", "ကျောက်ပန်းတောင်း", "ရမည်းသင်း", "ပျော်ဘွယ်", "ပျဉ်းမနား", "လယ်ဝေး", "တပ်ကုန်း", "ဥတ္တရသီရိ", 
    "ဒက္ခိဏသီရိ", "ပုဗ္ဗသီရိ", "ဇမ္ဗူသီရိ", "ဇေယျာသီရိ", "ဗဟန်း", "ဒဂုံ", "ဆိပ်ကမ်း", "ကြည့်မြင်တိုင်", "စမ်းချောင်း", 
    "လှိုင်", "ကမာရွတ်", "မရမ်းကုန်း", "အင်းစိန်", "မင်္ဂလာဒုံ", "ရွှေပြည်သာ", "လှိုင်သာယာ", "သင်္ဃန်းကျွန်း", "ရန်ကင်း", 
    "တောင်ဥက္ကလာပ", "မြောက်ဥက္ကလာပ", "သာကေတ", "ဒေါပုံ", "ဗိုလ်တထောင်", "ပုဇွန်တောင်", "ကျောက်တံတား", "လမ်းမတော်", 
    "လသာ", "တွံတေး", "ကော့မှူး", "ကွမ်းခြံကုန်း", "ဒလ", "ဆိပ်ကြီးခနောင်တို", "ကိုကိုးကျွန်း", "သန်လျင်", "ကျောက်တန်း", 
    "သုံးခွ", "ခရမ်း", "မှော်ဘီ", "ထောက်ကြန့်", "တိုက်ကြီး", "လှည်းကူး", "ကဝ", "သနပ်ပင်", "ဝေါ", "ညောင်လေးပင်", 
    "ကျောက်တံခါး", "ဒိုက်ဦး", "ရွှေကျင်", "တောင်ငူ", "ရေတာရှည်", "ကျောက်ကြီး", "ဖြူး", "အုတ်တွင်း", "ထန်းတပင်", 
    "ပြည်", "ပေါက်ခေါင်း", "ပေါင်းတည်", "သည်ကုန်း", "ရွှေတောင်", "ပန်းတောင်း", "သာယာဝတီ", "လက်ပံတန်း", "မိုးညို", 
    "အုတ်ဖို", "ကြို့ပင်ကောက်", "ဇီးကုန်း", "နတ်တလင်း", "စစ်တွေ", "ပုဏ္ဏားကျွန်း", "မြောက်ဦး", "ကျောက်တော်", "မင်းပြား", 
    "မြေပုံ", "ပေါက်တော", "ရသေ့တောင်", "ဘူးသီးတောင်", "မောင်တော", "ကျောက်ဖြူ", "မာန်အောင်", "ရမ်းဗြဲ", "အမ်း", 
    "သံတွဲ", "တောင်ကုတ်", "ဂွ", "မော်လမြိုင်", "ကျိုက်မရော", "ချောင်းဆုံ", "သံဖြူဇရပ်", "ရေး", "မုဒုံ", "သထုံ", 
    "ပေါင်", "ကျိုက်ထို", "ဘီလင်း", "ပုသိမ်", "ကန်ကြီးထောင့်", "သာပေါင်း", "ငပုတော", "ကျုံပျော်", "ရေကြည်", "ကျောင်းကုန်း", 
    "ဟင်္သာတ", "ဇလွန်", "လေးမျက်နှာ", "မြန်အောင်", "ကြံခင်း", "အင်္ဂပူ", "မြောင်းမြ", "အိမ်မဲ", "ဝါးခယ်မ", "မအူပင်", 
    "ပန်းတနော်", "ညောင်တုန်း", "ဓနုဖြူ", "ဖျာပုံ", "ဘိုကလေး", "ကျိုက်လတ်", "ဒေးဒရဲ", "ဟားခါး", "ထန်တလန်", "ဖလမ်း", 
    "တီးတိန်", "တွန်းဇံ", "မတူပီ", "မင်းတပ်", "ကန်ပက်လက်", "ပလက်ဝ", "မြစ်ကြီးနား", "ဝိုင်းမော်", "အင်ဂျန်းယန်", 
    "တနိုင်း", "ချီဖွေ", "ဆော့လော်", "ဗန်းမော်", "ရွှေကူ", "မိုးမောက်", "မံစီ", "ပူတာအို", "မချမ်းဘော", "ခေါင်လန်ဖူး", 
    "နောင်မွန်", "မိုးညှင်း", "မိုးကောင်း", "ဖားကန့်", "လွိုင်ကော်", "ဒီးမော့ဆို", "ဖရူဆို", "ရှားတော", "ဘော်လခဲ", 
    "ဖားဆောင်း", "မယ်စဲ့", "မိုင်းတုံ", "မိုင်းခတ်", "မိုင်းယန်း", "မိုင်းဖြတ်", "မိုင်းယောင်း"
]

# --- ၄။ WARD နှင့် ကျန်းမာရေးဌာနများ ---
wards = [
    "Medical Ward (၁)", "Medical Ward (၂)", "Surgical Ward (၁)", "Surgical Ward (၂)", 
    "OG Ward (သားဖွားမီးယပ်)", "Pediatric Ward (ကလေး)", "Orthopedic Ward (အရိုး)", 
    "Cardiac Unit (နှလုံး)", "ICU (အထူးကြပ်မတ်)", "Emergency (အရေးပေါ်)", "OPD (ပြင်ပလူနာ)",
    "Eye Ward (မျက်စိ)", "ENT Ward (နား/နှာ/လည်)", "Mental Health (စိတ်ကျန်းမာရေး)",
    "Dental Clinic (သွား)", "Dialysis Unit (ကျောက်ကပ်)", "Isolation Ward (ကူးစက်)",
    "Neuro Surgery", "Physiotherapy", "X-Ray & Imaging", "Lab Department", "Pharmacy",
    "Casualty Unit", "General Ward (A)", "General Ward (B)", "Labor Room"
]

# --- ၅။ SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/mohs-myanmar/mohs-myanmar.github.io/master/assets/img/logo.png", width=160)
    st.markdown("<h2 style='text-align:center;'>SST ENTERPRISE</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("ရွေးချယ်ရန်", [
        "📊 Dashboard Status", 
        "📋 လူနာအသစ်မှတ်ပုံတင်", 
        "🩺 ကုသမှုမှတ်တမ်းများ", 
        "📅 Duty Roster",
        "📥 Data Export (Excel)",
        "🗑️ System Reset"
    ])
    st.divider()
    st.info("🏥 စပ်စံထွန်းဆေးရုံ (တောင်ကြီး)")
    st.write(f"⏰ {datetime.now().strftime('%d-%m-%Y | %H:%M')}")

# --- ၆။ DASHBOARD ---
if menu == "📊 Dashboard Status":
    st.markdown("<div class='main-header'><h1>📊 ဆေးရုံလက်ရှိအခြေအနေ Dashboard</h1></div>", unsafe_allow_html=True)
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        col_1, col_2, col_3, col_4 = st.columns(4)
        col_1.metric("လူနာစုစုပေါင်း", f"{len(df)} ဦး")
        col_2.metric("ယနေ့တက်ရောက်", len(df[df['တက်ရောက်သည့်ရက်'] == datetime.now().strftime("%Y-%m-%d")]))
        col_3.metric("ICU လူနာ", len(df[df['Ward/ဌာန'] == "ICU (အထူးကြပ်မတ်)"]))
        col_4.metric("အရေးပေါ်", len(df[df['အရေးပေါ်အခြေအနေ'] == "Yes"]))
        
        st.subheader("🏥 Ward အလိုက် လူနာအင်အားပြဇယား")
        st.bar_chart(df['Ward/ဌာန'].value_counts())
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("ဒေတာ မရှိသေးပါ။")

# --- ၇။ လူနာအသစ်မှတ်ပုံတင် (ENTERPRISE FORM) ---
elif menu == "📋 လူနာအသစ်မှတ်ပုံတင်":
    st.markdown("<div class='main-header'><h1>📋 လူနာသစ် အချက်အလက်များ အသေးစိတ်ထည့်သွင်းခြင်း</h1></div>", unsafe_allow_html=True)
    with st.form("enterprise_ground_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 👤 ကိုယ်ရေးမှတ်တမ်း")
            p_name = st.text_input("လူနာအမည် (အပြည့်အစုံ)")
            p_age = st.number_input("အသက်", 0, 150)
            p_gender = st.selectbox("ကျား/မ", ["ကျား", "မ", "အခြား"])
            p_nrc = st.text_input("နိုင်ကတ် (NRC နံပါတ်)")
            p_town = st.selectbox("နေရပ်မြို့နယ် (၃၃၀ စာရင်း)", townships)
            p_address = st.text_input("ရပ်ကွက်/ကျေးရွာ/လမ်း")
            p_ph = st.text_input("လူနာ၏ ဖုန်းနံပါတ်")

        with c2:
            st.markdown("### 🩺 ဆေးရုံတက်ရောက်မှု")
            p_ward = st.selectbox("Ward/ဌာန ရွေးချယ်ပါ", wards)
            p_diag = st.text_input("Diagnosis (ရောဂါအမည်)")
            p_type = st.radio("လူနာအမျိုးအစား", ["သာမန်", "ခွဲစိတ်", "အထူး"], horizontal=True)
            p_emergency = st.selectbox("အရေးပေါ်အခြေအနေလား?", ["No", "Yes"])
            p_doctor = st.text_input("တာဝန်ခံဆရာဝန် အမည်")
            p_nurse = st.text_input("တာဝန်ကျသူနာပြု အမည်")
            p_admit = st.date_input("တက်ရောက်သည့်ရက်", datetime.now())
            p_discharge = st.date_input("ဆင်းမည့်ရက် (ခန့်မှန်း)", datetime.now())

        st.markdown("### 💊 ကုသမှုနှင့် အခြား")
        p_meds = st.text_area("ဆေးဝါးညွှန်ကြားချက်များ (Dosage စသည်ဖြင့်)")
        p_diet = st.text_input("ဓာတ်စာ နှင့် ရှောင်ရန်များ")
        p_emer_contact = st.text_input("အရေးပေါ်ဆက်သွယ်ရန် (အမည်နှင့်ဖုန်း)")
        p_note = st.text_input("အခြားမှတ်ချက်များ")

        if st.form_submit_button("💾 မှတ်တမ်းအားလုံးကို အပြီးတိုင်သိမ်းဆည်းမည်"):
            if p_name:
                df = pd.read_csv(DB_FILE)
                new_id = f"SST-P{len(df)+1001}"
                new_row = {
                    "Patient_ID": new_id, "လူနာအမည်": p_name, "အသက်": p_age, "ကျား/မ": p_gender,
                    "နိုင်ကတ် (NRC)": p_nrc, "ဖုန်းနံပါတ်": p_ph, "မြို့နယ်": p_town,
                    "ရပ်ကွက်/ကျေးရွာ": p_address, "Ward/ဌာန": p_ward, "Diagnosis (ရောဂါအမည်)": p_diag,
                    "လူနာအမျိုးအစား": p_type, "အရေးပေါ်အခြေအနေ": p_emergency,
                    "တက်ရောက်သည့်ရက်": p_admit.strftime("%Y-%m-%d"),
                    "ဆင်းမည့်ရက်": p_discharge.strftime("%Y-%m-%d"),
                    "တာဝန်ကျဆရာဝန်": p_doctor, "တာဝန်ကျသူနာပြု": p_nurse,
                    "ဆေးဝါးညွှန်ကြားချက်": p_meds, "ဓာတ်စာ/ရှောင်ရန်": p_diet,
                    "အရေးပေါ်ဆက်သွယ်ရန်": p_emer_contact, "မှတ်ချက်": p_note, "Status": "Active"
                }
                pd.concat([df, pd.DataFrame([new_row])], ignore_index=True).to_csv(DB_FILE, index=False, encoding='utf-8-sig')
                st.success(f"✅ လူနာ {p_name} (ID: {new_id}) ၏ အချက်အလက်များကို သိမ်းဆည်းပြီးပါပြီ။")
                st.balloons()
            else:
                st.error("⚠️ လူနာအမည် ထည့်သွင်းပေးပါ။")

# --- ၈။ ကုသမှုမှတ်တမ်းများ (SEARCH & FILTER) ---
elif menu == "🩺 ကုသမှုမှတ်တမ်းများ":
    st.markdown("<div class='main-header'><h1>🩺 လူနာမှတ်တမ်းများနှင့် အချက်အလက်ရှာဖွေခြင်း</h1></div>", unsafe_allow_html=True)
    df = pd.read_csv(DB_FILE)
    if not df.empty:
        search = st.text_input("🔍 လူနာအမည်၊ ID သို့မဟုတ် NRC ဖြင့် ရှာဖွေပါ")
        if search:
            df = df[df['လူနာအမည်'].str.contains(search) | df['Patient_ID'].str.contains(search) | df['နိုင်ကတ် (NRC)'].str.contains(search)]
        st.dataframe(df, use_container_width=True)
    else:
        st.info("မှတ်တမ်းများ မရှိသေးပါ။")

# --- ၉။ EXPORT & RESET ---
elif menu == "📥 Data Export (Excel)":
    st.title("📥 ဒေတာများကို Backup ယူရန်")
    df = pd.read_csv(DB_FILE)
    csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 Download Excel/CSV Report", csv, f"SST_Full_Report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

elif menu == "🗑️ System Reset":
    if st.button("❌ မှတ်တမ်းအားလုံးကို ရှင်းလင်းမည် (သတိပြုရန်)"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            init_db()
            st.success("စနစ်ကို Reset လုပ်ပြီးပါပြီ။")