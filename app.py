# app.py
import streamlit as st
import pandas as pd
from datetime import date, datetime

# page config
st.set_page_config(page_title="Resume Builder (Friendly UI)", layout="wide")

# ============================
# CONFIG (limits)
# ============================
MAX_PROJECTS = 5
MAX_EDUCATION = 3
MAX_WORK_EXP = 5
MAX_CERTS = 5
MAX_VOLUNTEER = 2

# ============================
# CSV HEADER (full final schema)
# ============================
CSV_HEADER = [
    "pd_FN","pd_MN","pd_LN","pd_Phone","pd_Email","pd_link_LinkedIn","pd_link_GitHub","pd_link_Portfolio",
    "pd_link_Kaggle","pd_link_HuggingFace","pd_link_GoogleScholar","pd_link_StackOverflow","pd_link_LeetCode",
    "pd_link_Codeforces","pd_link_CodeChef","pd_Location","pd_City","pd_State","pd_Country","pd_Pin",
    "pd_DOB","pd_Gender","pd_Nationality","pd_Languages","pd_MaritalStatus",
    "sum_ProfileSummary","sum_Objective","sum_ExpYears","sum_CurrentTitle","sum_CurrentCompany","sum_CurrentCTC",
    "sum_ExpectedCTC","sum_NoticePeriod","sum_Relocation",
    "sk_TechSkills","sk_SoftSkills","sk_Tools","sk_ProgLang","sk_PyLibs","sk_FWLibs","sk_DB","sk_CP","sk_OS",
    "edu1_Degree","edu1_Institute","edu1_Location","edu1_StartDate","edu1_EndDate","edu1_Score",
    "edu2_Degree","edu2_Institute","edu2_Location","edu2_StartDate","edu2_EndDate","edu2_Score",
    "edu3_Degree","edu3_Institute","edu3_Location","edu3_StartDate","edu3_EndDate","edu3_Score",
    "we1_Title","we1_Company","we1_Location","we1_StartDate","we1_EndDate","we1_Responsibilities",
    "we2_Title","we2_Company","we2_Location","we2_StartDate","we2_EndDate","we2_Responsibilities",
    "we3_Title","we3_Company","we3_Location","we3_StartDate","we3_EndDate","we3_Responsibilities",
    "we4_Title","we4_Company","we4_Location","we4_StartDate","we4_EndDate","we4_Responsibilities",
    "we5_Title","we5_Company","we5_Location","we5_StartDate","we5_EndDate","we5_Responsibilities",
    "prj1_Title","prj1_Description","prj1_Tech","prj1_Role","prj1_StartDate","prj1_EndDate","prj1_Link_GitHub","prj1_Link_Demo",
    "prj2_Title","prj2_Description","prj2_Tech","prj2_Role","prj2_StartDate","prj2_EndDate","prj2_Link_GitHub","prj2_Link_Demo",
    "prj3_Title","prj3_Description","prj3_Tech","prj3_Role","prj3_StartDate","prj3_EndDate","prj3_Link_GitHub","prj3_Link_Demo",
    "prj4_Title","prj4_Description","prj4_Tech","prj4_Role","prj4_StartDate","prj4_EndDate","prj4_Link_GitHub","prj4_Link_Demo",
    "prj5_Title","prj5_Description","prj5_Tech","prj5_Role","prj5_StartDate","prj5_EndDate","prj5_Link_GitHub","prj5_Link_Demo",
    "cert1_Name","cert1_Issuer","cert1_Date","cert1_Expiry","cert1_ID","cert1_Link",
    "cert2_Name","cert2_Issuer","cert2_Date","cert2_Expiry","cert2_ID","cert2_Link",
    "cert3_Name","cert3_Issuer","cert3_Date","cert3_Expiry","cert3_ID","cert3_Link",
    "cert4_Name","cert4_Issuer","cert4_Date","cert4_Expiry","cert4_ID","cert4_Link",
    "cert5_Name","cert5_Issuer","cert5_Date","cert5_Expiry","cert5_ID","cert5_Link",
    "pub1_Title","pub1_Publisher","pub1_Date","pub1_Link",
    "pub2_Title","pub2_Publisher","pub2_Date","pub2_Link",
    "vol1_Role","vol1_Organization","vol1_StartDate","vol1_EndDate",
    "vol2_Role","vol2_Organization","vol2_StartDate","vol2_EndDate",
    "ex_Awards","ex_Hobbies","ex_References","ref1_Name","ref1_Designation","ref1_Company","ref1_Contact","ex_Notes",
    "howmuch_filled"
]

# ============================
# FIELD SCHEMA (friendly labels + widget choices)
# widget types: "text","textarea","date","small","radio","select","multiselect","number"
# ============================
FIELD_SCHEMA = {
    # Personal
    "pd_FN": ("First name", "small"),
    "pd_MN": ("Middle name (optional)", "small"),
    "pd_LN": ("Last name", "small"),
    "pd_Phone": ("Phone number (include country code if applicable)", "small"),
    "pd_Email": ("Email address", "small"),
    "pd_link_LinkedIn": ("LinkedIn URL", "small"),
    "pd_link_GitHub": ("GitHub URL", "small"),
    "pd_link_Portfolio": ("Portfolio / Website URL", "small"),
    "pd_link_Kaggle": ("Kaggle profile URL", "small"),
    "pd_link_HuggingFace": ("Hugging Face profile URL", "small"),
    "pd_link_GoogleScholar": ("Google Scholar URL", "small"),
    "pd_link_StackOverflow": ("Stack Overflow URL", "small"),
    "pd_link_LeetCode": ("LeetCode URL", "small"),
    "pd_link_Codeforces": ("Codeforces URL", "small"),
    "pd_link_CodeChef": ("CodeChef URL", "small"),
    "pd_Location": ("Current location (city, state, country)", "text"),
    "pd_City": ("City", "small"),
    "pd_State": ("State", "small"),
    "pd_Country": ("Country", "small"),
    "pd_Pin": ("Postal code / PIN", "small"),
    "pd_DOB": ("Date of birth", "date"),
    "pd_Gender": ("Gender", "radio"),
    "pd_Nationality": ("Nationality", "small"),
    "pd_Languages": ("Languages (select common then add others below)", "multiselect"),
    "pd_MaritalStatus": ("Marital status", "select"),

    # Summary
    "sum_ProfileSummary": ("Profile summary (short paragraph)", "textarea"),
    "sum_Objective": ("Objective (optional)", "textarea"),
    "sum_ExpYears": ("Total experience (select or 'Fresher')", "select"),
    "sum_CurrentTitle": ("Current job title", "small"),
    "sum_CurrentCompany": ("Current company", "small"),
    "sum_CurrentCTC": ("Current salary (CTC) — optional", "small"),
    "sum_ExpectedCTC": ("Expected salary (CTC) — optional", "small"),
    "sum_NoticePeriod": ("Notice period (e.g., 2 months)", "small"),
    "sum_Relocation": ("Open to relocation?", "radio"),

    # Skills
    "sk_TechSkills": ("Top technical skills (quick select + add others)", "multiselect"),
    "sk_SoftSkills": ("Soft skills (select + add)", "multiselect"),
    "sk_Tools": ("Tools & technologies (comma-separated)", "text"),
    "sk_ProgLang": ("Programming languages (select + add)", "multiselect"),
    "sk_PyLibs": ("Python libraries (common + add)", "multiselect"),
    "sk_FWLibs": ("Frameworks & libraries (select + add)", "multiselect"),
    "sk_DB": ("Databases (select)", "multiselect"),
    "sk_CP": ("Cloud platforms (select)", "multiselect"),
    "sk_OS": ("Operating systems (select)", "multiselect"),
}

# add dynamic repeated fields (education, work, projects, certs, pubs, vols, extras)
for i in range(1, MAX_EDUCATION + 1):
    FIELD_SCHEMA[f"edu{i}_Degree"] = (f"Education {i} — Degree (e.g., B.Tech in CSE)", "small")
    FIELD_SCHEMA[f"edu{i}_Institute"] = (f"Education {i} — Institute", "small")
    FIELD_SCHEMA[f"edu{i}_Location"] = (f"Education {i} — Location", "small")
    FIELD_SCHEMA[f"edu{i}_StartDate"] = (f"Education {i} — Start date", "date")
    FIELD_SCHEMA[f"edu{i}_EndDate"] = (f"Education {i} — End date", "date")
    FIELD_SCHEMA[f"edu{i}_Score"] = (f"Education {i} — Score / CGPA", "small")

for i in range(1, MAX_WORK_EXP + 1):
    FIELD_SCHEMA[f"we{i}_Title"] = (f"Experience {i} — Job title", "small")
    FIELD_SCHEMA[f"we{i}_Company"] = (f"Experience {i} — Company", "small")
    FIELD_SCHEMA[f"we{i}_Location"] = (f"Experience {i} — Location", "small")
    FIELD_SCHEMA[f"we{i}_StartDate"] = (f"Experience {i} — Start date", "date")
    FIELD_SCHEMA[f"we{i}_EndDate"] = (f"Experience {i} — End date", "date")
    FIELD_SCHEMA[f"we{i}_Responsibilities"] = (f"Experience {i} — Responsibilities / achievements", "textarea")

for i in range(1, MAX_PROJECTS + 1):
    FIELD_SCHEMA[f"prj{i}_Title"] = (f"Project {i} — Title", "small")
    FIELD_SCHEMA[f"prj{i}_Description"] = (f"Project {i} — Short description", "textarea")
    FIELD_SCHEMA[f"prj{i}_Tech"] = (f"Project {i} — Technologies used", "multiselect")
    FIELD_SCHEMA[f"prj{i}_Role"] = (f"Project {i} — Your role", "small")
    FIELD_SCHEMA[f"prj{i}_StartDate"] = (f"Project {i} — Start date", "date")
    FIELD_SCHEMA[f"prj{i}_EndDate"] = (f"Project {i} — End date", "date")
    FIELD_SCHEMA[f"prj{i}_Link_GitHub"] = (f"Project {i} — GitHub link", "small")
    FIELD_SCHEMA[f"prj{i}_Link_Demo"] = (f"Project {i} — Demo / live link", "small")

for i in range(1, MAX_CERTS + 1):
    FIELD_SCHEMA[f"cert{i}_Name"] = (f"Certification {i} — Name", "small")
    FIELD_SCHEMA[f"cert{i}_Issuer"] = (f"Certification {i} — Issuer", "small")
    FIELD_SCHEMA[f"cert{i}_Date"] = (f"Certification {i} — Issue date", "date")
    FIELD_SCHEMA[f"cert{i}_Expiry"] = (f"Certification {i} — Expiry date (optional)", "date")
    FIELD_SCHEMA[f"cert{i}_ID"] = (f"Certification {i} — Credential ID", "small")
    FIELD_SCHEMA[f"cert{i}_Link"] = (f"Certification {i} — Credential URL", "small")

for i in range(1, 3):
    FIELD_SCHEMA[f"pub{i}_Title"] = (f"Publication {i} — Title", "small")
    FIELD_SCHEMA[f"pub{i}_Publisher"] = (f"Publication {i} — Publisher / Venue", "small")
    FIELD_SCHEMA[f"pub{i}_Date"] = (f"Publication {i} — Date", "date")
    FIELD_SCHEMA[f"pub{i}_Link"] = (f"Publication {i} — Link", "small")

for i in range(1, MAX_VOLUNTEER + 1):
    FIELD_SCHEMA[f"vol{i}_Role"] = (f"Volunteer {i} — Role", "small")
    FIELD_SCHEMA[f"vol{i}_Organization"] = (f"Volunteer {i} — Organization", "small")
    FIELD_SCHEMA[f"vol{i}_StartDate"] = (f"Volunteer {i} — Start date", "date")
    FIELD_SCHEMA[f"vol{i}_EndDate"] = (f"Volunteer {i} — End date", "date")

# extras
FIELD_SCHEMA["ex_Awards"] = ("Awards & achievements (comma-separated)", "text")
FIELD_SCHEMA["ex_Hobbies"] = ("Hobbies & interests (comma-separated)", "text")
FIELD_SCHEMA["ex_References"] = ("References short list / notes", "text")
FIELD_SCHEMA["ref1_Name"] = ("Primary reference — Name", "small")
FIELD_SCHEMA["ref1_Designation"] = ("Primary reference — Designation", "small")
FIELD_SCHEMA["ref1_Company"] = ("Primary reference — Company", "small")
FIELD_SCHEMA["ref1_Contact"] = ("Primary reference — Contact (phone/email)", "small")
FIELD_SCHEMA["ex_Notes"] = ("Additional private notes", "textarea")

# ============================
# SESSION INIT
# ============================
def init_session():
    if "form_data" not in st.session_state:
        st.session_state.form_data = {k: "" for k in CSV_HEADER}
    # ensure keys
    for k in CSV_HEADER:
        if k not in st.session_state.form_data:
            st.session_state.form_data[k] = ""
    # counters for dynamic blocks
    if "projects_count" not in st.session_state:
        st.session_state.projects_count = 1
    if "education_count" not in st.session_state:
        st.session_state.education_count = 1
    if "work_count" not in st.session_state:
        st.session_state.work_count = 1
    if "cert_count" not in st.session_state:
        st.session_state.cert_count = 1
    if "vol_count" not in st.session_state:
        st.session_state.vol_count = 1

init_session()

# ============================
# Small CSS for cards
# ============================
CARD_CSS = """
<style>
.card {
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 12px;
  background: white;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.section-title {
  font-weight:600;
  margin-bottom: 6px;
}
.note { color: #6c6c6c; font-size:12px; }
</style>
"""
st.markdown(CARD_CSS, unsafe_allow_html=True)

# ============================
# Common option lists for multiselects and selects
# ============================
COMMON_LANGUAGES = ["English","Hindi","Telugu","Tamil","Kannada","Malayalam","Bengali","Marathi","Urdu","Punjabi","Other"]
COMMON_PROGLANGS = ["Python","Java","C++","JavaScript","TypeScript","Go","Rust","R","SQL","MATLAB"]
COMMON_PYLIBS = ["numpy","pandas","scikit-learn","tensorflow","pytorch","matplotlib","seaborn","xgboost","lightgbm"]
COMMON_FRAMEWORKS = ["Django","Flask","FastAPI","React","Angular","Vue","Node.js","Spring"]
COMMON_DB = ["MySQL","PostgreSQL","MongoDB","Redis","SQLite","BigQuery"]
COMMON_CLOUD = ["AWS","GCP","Azure","DigitalOcean"]
COMMON_OS = ["Linux","Windows","macOS"]
COMMON_TECH = sorted(set(COMMON_PROGLANGS + COMMON_PYLIBS + COMMON_FRAMEWORKS + COMMON_DB))

# ============================
# Helper widgets that map to CSV keys
# ============================
def save_text(key, label=None, placeholder=None):
    label = label if label else FIELD_SCHEMA.get(key, (key,"text"))[0]
    val = st.text_input(label, value=st.session_state.form_data.get(key,""), placeholder=placeholder, key=f"ui_{key}")
    st.session_state.form_data[key] = val.strip() if isinstance(val,str) else val
    return val

def save_textarea(key, label=None, placeholder=None, height=140):
    label = label if label else FIELD_SCHEMA.get(key, (key,"textarea"))[0]
    val = st.text_area(label, value=st.session_state.form_data.get(key,""), placeholder=placeholder, height=height, key=f"ui_{key}")
    st.session_state.form_data[key] = val.strip() if isinstance(val,str) else val
    return val

def save_date(key, label=None):
    label = label if label else FIELD_SCHEMA.get(key, (key,"date"))[0]
    cur = st.session_state.form_data.get(key,"")
    default = None
    if cur:
        try:
            default = datetime.fromisoformat(cur).date()
        except Exception:
            default = None
    if default:
        d = st.date_input(label, value=default, key=f"ui_{key}")
    else:
        # neutral default: Jan 1 of current year - lighter choice
        d = st.date_input(label, key=f"ui_{key}")
    if isinstance(d, date):
        iso = d.isoformat()
        st.session_state.form_data[key] = iso
        return iso
    st.session_state.form_data[key] = ""
    return ""

def save_radio(key, options, label=None):
    label = label if label else FIELD_SCHEMA.get(key, (key,"radio"))[0]
    cur = st.session_state.form_data.get(key,"")
    if cur in options:
        default = options.index(cur)
    else:
        default = 0
    val = st.radio(label, options, index=default, key=f"ui_{key}")
    st.session_state.form_data[key] = val
    return val

def save_select(key, options, label=None):
    label = label if label else FIELD_SCHEMA.get(key, (key,"select"))[0]
    cur = st.session_state.form_data.get(key,"")
    # if stored value matches one option, set it otherwise default 0
    if cur in options:
        idx = options.index(cur)
    else:
        idx = 0
    val = st.selectbox(label, options, index=idx, key=f"ui_{key}")
    st.session_state.form_data[key] = val
    return val

def save_multiselect(key, options, label=None, allow_other=False):
    label = label if label else FIELD_SCHEMA.get(key, (key,"multiselect"))[0]
    stored = st.session_state.form_data.get(key,"")
    stored_list = []
    if stored:
        # stored may be comma separated
        stored_list = [x.strip() for x in stored.split(",") if x.strip()]
    # pre-select intersection
    pre_selected = [o for o in options if o in stored_list]
    selected = st.multiselect(label, options, default=pre_selected, key=f"ui_{key}")
    # additional other
    other_txt = ""
    if allow_other:
        other_txt = st.text_input("Add other (comma-separated)", key=f"ui_{key}_other", value=",".join([x for x in stored_list if x not in options]))
    # combine
    final_list = selected.copy()
    if allow_other and other_txt:
        extras = [x.strip() for x in other_txt.split(",") if x.strip()]
        final_list.extend(extras)
    # store as comma-separated
    st.session_state.form_data[key] = ",".join(final_list)
    return final_list

def save_number_or_fresher(key, label=None):
    label = label if label else FIELD_SCHEMA.get(key, (key,"number"))[0]
    # fetch existing
    cur = st.session_state.form_data.get(key,"")
    # If cur is 'Fresher' treat separately
    if cur == "Fresher":
        default = "Fresher"
    else:
        default = cur
    col1, col2 = st.columns([2,1])
    with col1:
        val = st.text_input(label, value=default, key=f"ui_{key}")
    with col2:
        if st.button("Mark as Fresher", key=f"fresher_{key}"):
            val = "Fresher"
            st.session_state.form_data[key] = val
    st.session_state.form_data[key] = val.strip() if isinstance(val,str) else val
    return val

# ============================
# Sidebar and navigation
# ============================
st.sidebar.title("Resume Builder")
st.sidebar.write("Fill stages — data stored in this session until you close the tab.")
sections = [
    "Personal", "Summary", "Skills", "Education", "Work Experience",
    "Projects", "Certifications", "Publications", "Volunteering", "Extras", "Finish"
]
choice = st.sidebar.radio("Go to stage:", sections)

if st.sidebar.button("Reset all data"):
    for k in st.session_state.form_data.keys():
        st.session_state.form_data[k] = ""
    st.session_state.projects_count = 1
    st.session_state.education_count = 1
    st.session_state.work_count = 1
    st.session_state.cert_count = 1
    st.session_state.vol_count = 1
    st.sidebar.success("Cleared session data.")

st.title("Resume Builder — Friendly UI (fast inputs)")

# ============================
# PERSONAL
# ============================
if choice == "Personal":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Personal details</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        save_text("pd_FN")
        save_text("pd_MN")
        save_text("pd_LN")
    with c2:
        save_text("pd_Phone")
        save_text("pd_Email")
        save_text("pd_link_LinkedIn")
    with c3:
        save_text("pd_link_GitHub")
        save_text("pd_link_Portfolio")
        save_text("pd_link_Kaggle")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">More personal info</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        save_text("pd_Location")
        save_text("pd_City")
        save_text("pd_State")
    with c2:
        save_text("pd_Country")
        save_text("pd_Pin")
        save_date("pd_DOB")
    # gender radio
    save_radio("pd_Gender", ["Male","Female","Other","Prefer not to say"])
    # languages multiselect
    save_multiselect("pd_Languages", COMMON_LANGUAGES, allow_other=True)
    save_select("pd_MaritalStatus", ["", "Single","Married","Other"])
    save_text("pd_Nationality")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# SUMMARY
# ============================
elif choice == "Summary":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Profile summary & career info</div>', unsafe_allow_html=True)
    save_textarea("sum_ProfileSummary")
    save_textarea("sum_Objective")
    # experience select (Fresher + 0..40)
    exp_options = ["Fresher"] + [str(i) for i in range(0, 41)]
    save_select("sum_ExpYears", exp_options)
    save_text("sum_CurrentTitle")
    save_text("sum_CurrentCompany")
    save_text("sum_CurrentCTC")
    save_text("sum_ExpectedCTC")
    save_text("sum_NoticePeriod")
    save_radio("sum_Relocation", ["Yes","No"])
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# SKILLS
# ============================
elif choice == "Skills":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Skills — quick picks</div>', unsafe_allow_html=True)
    save_multiselect("sk_ProgLang", COMMON_PROGLANGS, allow_other=True)
    save_multiselect("sk_PyLibs", COMMON_PYLIBS, allow_other=True)
    save_multiselect("sk_FWLibs", COMMON_FRAMEWORKS, allow_other=True)
    save_multiselect("sk_DB", COMMON_DB, allow_other=True)
    save_multiselect("sk_CP", COMMON_CLOUD, allow_other=True)
    save_multiselect("sk_OS", COMMON_OS, allow_other=True)
    # additional text fields
    save_text("sk_Tools", placeholder="e.g., Docker, Git, Airflow (comma sep)")
    save_multiselect("sk_SoftSkills", ["Communication","Teamwork","Leadership","Problem solving","Time management"], allow_other=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# EDUCATION (dynamic up to MAX_EDUCATION)
# ============================
elif choice == "Education":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Education (add up to {})</div>'.format(MAX_EDUCATION), unsafe_allow_html=True)

    col_add = st.columns([1,4])
    with col_add[0]:
        if st.button("➕ Add Education", key="add_edu"):
            if st.session_state.education_count < MAX_EDUCATION:
                st.session_state.education_count += 1
    with col_add[1]:
        st.write("")

    for i in range(1, st.session_state.education_count + 1):
        st.markdown(f'<div style="padding:10px;margin-bottom:8px;border-radius:6px;background:#fbfbfb"> <b>Education {i}</b></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            save_text(f"edu{i}_Degree")
            save_text(f"edu{i}_Institute")
            save_text(f"edu{i}_Location")
        with c2:
            # date pickers
            save_date(f"edu{i}_StartDate")
            save_date(f"edu{i}_EndDate")
            save_text(f"edu{i}_Score")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# WORK EXPERIENCE (dynamic up to MAX_WORK_EXP)
# ============================
elif choice == "Work Experience":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Work Experience (add up to {})</div>'.format(MAX_WORK_EXP), unsafe_allow_html=True)

    col_add = st.columns([1,4])
    with col_add[0]:
        if st.button("➕ Add Work Experience", key="add_work"):
            if st.session_state.work_count < MAX_WORK_EXP:
                st.session_state.work_count += 1
    with col_add[1]:
        st.write("")

    for i in range(1, st.session_state.work_count + 1):
        st.markdown(f'<div style="padding:10px;margin-bottom:8px;border-radius:6px;background:#fbfbfb"> <b>Experience {i}</b></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([2,2])
        with c1:
            save_text(f"we{i}_Title")
            save_text(f"we{i}_Company")
            save_text(f"we{i}_Location")
        with c2:
            save_date(f"we{i}_StartDate")
            save_date(f"we{i}_EndDate")
        save_textarea(f"we{i}_Responsibilities")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# PROJECTS (dynamic up to MAX_PROJECTS)
# ============================
elif choice == "Projects":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Projects (add up to {})</div>'.format(MAX_PROJECTS), unsafe_allow_html=True)

    col_add = st.columns([1,4])
    with col_add[0]:
        if st.button("➕ Add Project", key="add_project"):
            if st.session_state.projects_count < MAX_PROJECTS:
                st.session_state.projects_count += 1
    with col_add[1]:
        st.write("")

    for i in range(1, st.session_state.projects_count + 1):
        st.markdown(f'<div style="padding:10px;margin-bottom:8px;border-radius:6px;background:#fbfbfb"> <b>Project {i}</b></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([2,1])
        with c1:
            save_text(f"prj{i}_Title")
            save_textarea(f"prj{i}_Description")
            # tech multiselect uses COMMON_TECH
            save_multiselect(f"prj{i}_Tech", COMMON_TECH, allow_other=True)
        with c2:
            save_text(f"prj{i}_Role")
            save_date(f"prj{i}_StartDate")
            save_date(f"prj{i}_EndDate")
            save_text(f"prj{i}_Link_GitHub")
            save_text(f"prj{i}_Link_Demo")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# CERTIFICATIONS (dynamic up to MAX_CERTS)
# ============================
elif choice == "Certifications":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Certifications (add up to {})</div>'.format(MAX_CERTS), unsafe_allow_html=True)

    col_add = st.columns([1,4])
    with col_add[0]:
        if st.button("➕ Add Certification", key="add_cert"):
            if st.session_state.cert_count < MAX_CERTS:
                st.session_state.cert_count += 1
    with col_add[1]:
        st.write("")

    for i in range(1, st.session_state.cert_count + 1):
        st.markdown(f'<div style="padding:10px;margin-bottom:8px;border-radius:6px;background:#fbfbfb"> <b>Certification {i}</b></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            save_text(f"cert{i}_Name")
            save_text(f"cert{i}_Issuer")
        with c2:
            save_date(f"cert{i}_Date")
            save_date(f"cert{i}_Expiry")
        save_text(f"cert{i}_ID")
        save_text(f"cert{i}_Link")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# PUBLICATIONS (up to 2)
# ============================
elif choice == "Publications":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Publications (up to 2)</div>', unsafe_allow_html=True)
    for i in range(1, 3):
        st.markdown(f'<div style="padding:10px;margin-bottom:8px;border-radius:6px;background:#fbfbfb"> <b>Publication {i}</b></div>', unsafe_allow_html=True)
        save_text(f"pub{i}_Title")
        save_text(f"pub{i}_Publisher")
        save_date(f"pub{i}_Date")
        save_text(f"pub{i}_Link")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# VOLUNTEERING (dynamic up to MAX_VOLUNTEER)
# ============================
elif choice == "Volunteering":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Volunteering (add up to {})</div>'.format(MAX_VOLUNTEER), unsafe_allow_html=True)

    col_add = st.columns([1,4])
    with col_add[0]:
        if st.button("➕ Add Volunteering", key="add_vol"):
            if st.session_state.vol_count < MAX_VOLUNTEER:
                st.session_state.vol_count += 1
    with col_add[1]:
        st.write("")

    for i in range(1, st.session_state.vol_count + 1):
        st.markdown(f'<div style="padding:10px;margin-bottom:8px;border-radius:6px;background:#fbfbfb"> <b>Volunteer {i}</b></div>', unsafe_allow_html=True)
        save_text(f"vol{i}_Role")
        save_text(f"vol{i}_Organization")
        save_date(f"vol{i}_StartDate")
        save_date(f"vol{i}_EndDate")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# EXTRAS & REFERENCES
# ============================
elif choice == "Extras":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Extras & references</div>', unsafe_allow_html=True)
    save_text("ex_Awards",)
    save_text("ex_Hobbies")
    save_text("ex_References")
    st.subheader("Primary reference (optional)")
    c1, c2 = st.columns(2)
    with c1:
        save_text("ref1_Name")
        save_text("ref1_Designation")
    with c2:
        save_text("ref1_Company")
        save_text("ref1_Contact")
    save_textarea("ex_Notes")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# FINISH: compose CSV, show preview, download
# ============================
elif choice == "Finish":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Review & export</div>', unsafe_allow_html=True)

    # compute howmuch_filled
    filled = sum(1 for v in st.session_state.form_data.values() if str(v).strip() != "")
    st.session_state.form_data["howmuch_filled"] = str(filled)

    # Build ordered row to match CSV_HEADER
    row = {k: st.session_state.form_data.get(k,"") for k in CSV_HEADER}
    df = pd.DataFrame([row], columns=CSV_HEADER)

    left, right = st.columns([1, 2])
    with left:
        st.metric("Fields filled", filled)
        st.write("Non-empty fields (sample):")
        nonempty = [k for k, v in row.items() if str(v).strip() != ""]
        st.write(nonempty[:200])
        if st.button("Upload to Supabase (placeholder)"):
            st.info("Supabase upload not implemented. Add supabase code here with your keys.")
    with right:
        st.write("Preview (vertical):")
        st.dataframe(df.T, height=600)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv_bytes, "resume_row.csv", "text/csv")

    st.markdown("</div>", unsafe_allow_html=True)

# footer
st.markdown("---")
st.caption("Tips: • Use Add buttons to reveal more blocks. • Dates stored as YYYY-MM-DD. • Data is kept in session_state while this tab is open.")
