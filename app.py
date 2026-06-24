import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# ---- Custom CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: #0d0f14;
    color: #e2e8f0;
}

/* Hide default streamlit stuff */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1100px; }

/* Hero Header */
.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #1e2433;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7c86ff 0%, #a78bfa 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: #64748b;
    font-size: 1rem;
    margin: 0;
}

/* Cards */
.card {
    background: #141820;
    border: 1px solid #1e2433;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1rem;
}

/* Score circles */
.score-wrap {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 1.5rem;
}
.score-card {
    flex: 1;
    background: #141820;
    border: 1px solid #1e2433;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}
.score-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.score-label {
    font-size: 0.78rem;
    color: #64748b;
    letter-spacing: 0.5px;
}
.score-high { color: #34d399; }
.score-mid  { color: #fbbf24; }
.score-low  { color: #f87171; }

/* Skill pills */
.pill-wrap { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
.pill {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
}
.pill-found  { background: #064e3b; color: #34d399; border: 1px solid #065f46; }
.pill-missing { background: #1f1315; color: #f87171; border: 1px solid #3b1111; }
.pill-needed  { background: #1c1a00; color: #fbbf24; border: 1px solid #3d3000; }

/* Checklist items */
.check-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid #1a1f2e;
    font-size: 0.88rem;
    color: #94a3b8;
}
.check-item:last-child { border-bottom: none; }
.check-pass { color: #34d399; font-size: 1rem; }
.check-fail { color: #f87171; font-size: 1rem; }

/* Suggestions */
.suggestion {
    background: #13182a;
    border-left: 3px solid #7c86ff;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1rem;
    margin-bottom: 0.7rem;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.6;
}

/* Status banner */
.banner {
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    font-size: 0.88rem;
    font-weight: 500;
    margin: 1rem 0;
}
.banner-good    { background: #052e16; color: #34d399; border: 1px solid #065f46; }
.banner-warning { background: #1c1400; color: #fbbf24; border: 1px solid #3d2e00; }
.banner-danger  { background: #1a0505; color: #f87171; border: 1px solid #3b0f0f; }

/* Upload area override */
[data-testid="stFileUploader"] {
    background: #141820;
    border: 1.5px dashed #2d3748;
    border-radius: 12px;
    padding: 1rem;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7c86ff;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #141820;
    border: 1px solid #2d3748;
    border-radius: 10px;
    color: #e2e8f0;
}

/* Footer */
.footer {
    text-align: center;
    color: #334155;
    font-size: 0.75rem;
    padding-top: 2rem;
    border-top: 1px solid #1e2433;
    margin-top: 2rem;
}

/* Progress bar */
.prog-bar-bg {
    background: #1e2433;
    border-radius: 999px;
    height: 6px;
    margin-top: 0.4rem;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #7c86ff, #06b6d4);
}
</style>
""", unsafe_allow_html=True)

# ---- Data ----
SKILLS = {
    "Python":          ["python"],
    "Java":            ["java"],
    "C++":             ["c++", "cpp"],
    "DSA":             ["data structures", "algorithms", "dsa", "leetcode"],
    "Machine Learning":["machine learning", "ml", "sklearn", "tensorflow"],
    "SQL":             ["sql", "mysql", "postgresql", "database"],
    "Git / GitHub":    ["git", "github"],
    "AI / LLM":        ["artificial intelligence", "llm", "openai", "gemini", "langchain"],
    "Cybersecurity":   ["penetration testing", "vapt", "owasp", "nmap", "burp suite", "wireshark"],
    "Cloud":           ["aws", "gcp", "azure", "docker"],
    "Web Dev":         ["flask", "django", "react", "fastapi", "node"],
    "Linux":           ["linux", "kali", "ubuntu", "bash", "shell"],
}

ROLE_REQUIREMENTS = {
    "SOC Analyst":       ["Cybersecurity", "Linux", "Python", "SQL"],
    "VAPT / Pentester":  ["Cybersecurity", "Linux", "Python", "Git / GitHub"],
    "ML / AI Engineer":  ["Python", "Machine Learning", "AI / LLM", "SQL"],
    "Backend Dev":       ["Python", "SQL", "Git / GitHub", "Web Dev"],
    "Full Stack Dev":    ["Python", "Web Dev", "SQL", "Git / GitHub", "Java"],
}

# ---- Helpers ----
def read_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for pg in reader.pages:
            t = pg.extract_text()
            if t:
                text += t + "\n"
        return text.lower()
    except Exception as e:
        st.error(f"Couldn't read the PDF: {e}")
        return ""

def get_skills(text):
    found, missing = [], []
    for skill, kws in SKILLS.items():
        (found if any(kw in text for kw in kws) else missing).append(skill)
    return found, missing

def check_basics(text):
    return {
        "Email address":         bool(re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)),
        "Phone number":          bool(re.search(r'\+?\d[\d\s\-]{8,}', text)),
        "GitHub link":           "github" in text,
        "LinkedIn link":         "linkedin" in text,
        "Projects section":      "project" in text,
        "Internship / experience":any(w in text for w in ["intern", "experience", "worked", "developed"]),
        "Education details":     any(w in text for w in ["b.tech", "btech", "university", "college", "cgpa", "gpa"]),
    }

def score_role(found, role):
    needed  = ROLE_REQUIREMENTS[role]
    matched = [s for s in needed if s in found]
    missing = [s for s in needed if s not in found]
    return int(len(matched) / len(needed) * 100), matched, missing

def score_color(s):
    if s >= 75: return "score-high"
    if s >= 50: return "score-mid"
    return "score-low"

def pills(items, cls):
    inner = "".join(f'<span class="pill {cls}">{i}</span>' for i in items)
    return f'<div class="pill-wrap">{inner}</div>'

# ---- Hero ----
st.markdown("""
<div class="hero">
  <h1>📄 Resume Analyzer</h1>
  <p>Built for CS &amp; Cybersecurity students targeting internships — see exactly what's missing and why.</p>
</div>
""", unsafe_allow_html=True)

# ---- Layout ----
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown('<div class="card"><div class="card-title">Upload Your Resume</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("PDF only", type=["pdf"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Target Role</div>', unsafe_allow_html=True)
    target_role = st.selectbox(
        "Role",
        list(ROLE_REQUIREMENTS.keys()),
        label_visibility="collapsed",
        help="Pick the internship role you're applying for"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if not uploaded:
        st.markdown("""
        <div class="card" style="color:#475569;font-size:0.85rem;line-height:1.7;">
          <div class="card-title">How it works</div>
          1. Upload your resume PDF<br>
          2. Choose your target role<br>
          3. See skill gaps & checklist<br>
          4. Fix the red items & reapply
        </div>
        """, unsafe_allow_html=True)

with right:
    if not uploaded:
        st.markdown("""
        <div style="height:300px;display:flex;align-items:center;justify-content:center;color:#334155;font-size:0.9rem;">
          ← Upload your resume to see the analysis
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    resume_text = read_pdf(uploaded)
    if not resume_text:
        st.stop()

    found_skills, missing_skills = get_skills(resume_text)
    basics      = check_basics(resume_text)
    role_score, role_matched, role_missing = score_role(found_skills, target_role)
    overall     = int(len(found_skills) / len(SKILLS) * 100)

    # Scores
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="score-card">
          <div class="score-num {score_color(overall)}">{overall}%</div>
          <div class="score-label">Overall Skill Coverage</div>
          <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{overall}%"></div></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="score-card">
          <div class="score-num {score_color(role_score)}">{role_score}%</div>
          <div class="score-label">Match for {target_role}</div>
          <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{role_score}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

    # Banner
    if role_score >= 75:
        banner_cls, banner_msg = "banner-good", "✅ Strong match! You're well-positioned for this role."
    elif role_score >= 50:
        banner_cls, banner_msg = "banner-warning", "⚠️ Decent match — add the missing skills below to stand out."
    else:
        banner_cls, banner_msg = "banner-danger", "❌ Low match — focus on the missing role skills before applying."

    st.markdown(f'<div class="banner {banner_cls}">{banner_msg}</div>', unsafe_allow_html=True)

    # Skills section
    sa, sb, sc = st.columns(3)
    with sa:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">✅ Skills Detected</div>
          {pills(found_skills, "pill-found") if found_skills else '<span style="color:#475569;font-size:0.85rem;">None found</span>'}
        </div>
        """, unsafe_allow_html=True)
    with sb:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">❌ Skills Missing</div>
          {pills(missing_skills, "pill-missing") if missing_skills else '<span style="color:#34d399;font-size:0.85rem;">All covered!</span>'}
        </div>
        """, unsafe_allow_html=True)
    with sc:
        have_html = pills(role_matched, "pill-found") if role_matched else ""
        need_html = pills(role_missing, "pill-needed") if role_missing else '<span style="color:#34d399;font-size:0.85rem;">All covered!</span>'
        st.markdown(f"""
        <div class="card">
          <div class="card-title">🎯 For {target_role}</div>
          {"<div style='font-size:0.72rem;color:#475569;margin-bottom:0.3rem;'>HAVE</div>" + have_html if role_matched else ""}
          <div style='font-size:0.72rem;color:#475569;margin:0.6rem 0 0.3rem 0;'>NEED</div>
          {need_html}
        </div>
        """, unsafe_allow_html=True)

# ---- Checklist ----
st.markdown('<div class="card" style="margin-top:1.2rem;"><div class="card-title">📋 Resume Checklist</div>', unsafe_allow_html=True)
items_html = ""
for label, passed in basics.items():
    icon_cls = "check-pass" if passed else "check-fail"
    icon     = "✓" if passed else "✗"
    items_html += f'<div class="check-item"><span class="{icon_cls}">{icon}</span>{label}</div>'
st.markdown(items_html + "</div>", unsafe_allow_html=True)

# ---- Suggestions ----
suggestions = []
if "DSA" in missing_skills:
    suggestions.append("👉 <b>Add DSA</b> — Even cybersecurity roles sometimes ask DSA rounds. 50 easy LeetCode problems + mention it on resume.")
if "Git / GitHub" in missing_skills:
    suggestions.append("👉 <b>Link GitHub</b> — Recruiters click this first. If you have projects, push them today.")
if "Cloud" in missing_skills:
    suggestions.append("👉 <b>Add cloud exposure</b> — Even AWS free tier + one deployed project is enough to mention.")
if role_score < 60:
    suggestions.append(f"👉 <b>Upskill for {target_role}</b> — Prioritize: {', '.join(role_missing)}.")
if overall >= 70:
    suggestions.append("✅ Good overall coverage. Focus on depth in 2–3 areas rather than spreading thin.")
if not basics["Projects section"]:
    suggestions.append("👉 <b>Add a Projects section</b> — For freshers, projects are your experience. Don't skip this.")

if suggestions:
    st.markdown('<div class="card"><div class="card-title">💡 Suggestions</div>', unsafe_allow_html=True)
    for s in suggestions:
        st.markdown(f'<div class="suggestion">{s}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Footer ----
st.markdown("""
<div class="footer">
  Keyword-based matching — use as a quick self-check, not a final verdict.<br>
  Built by <b>Jhanvi Jyant</b> · <a href="https://github.com/jhanvijyant" style="color:#7c86ff;">GitHub</a> · <a href="https://linkedin.com/in/jhanvi-jyant" style="color:#7c86ff;">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
