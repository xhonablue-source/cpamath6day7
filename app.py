"""
CPA Math 6 — Day 7: Area of Compound Rectangles
Built to match the visual/interactive structure of the Day 5 ("Area Is
Multiplication") and Day 6 ("Area Unlocks the Missing Side") apps by
Xavier Honablue, M.Ed — Chandler Park Academy.

Lesson mode follows the i-Ready Classroom Mathematics session flow used for
its "Area of a Parallelogram" lesson (Explore -> Model It, two ways -> Try It
-> Discuss It & Connect It -> Practice -> Apply It) — applied here to
composite/compound figures built entirely out of rectangles, continuing
directly from Day 6's L-shaped floor.

Run locally with:  streamlit run app.py
Deploy the same way Day 5/6 were deployed: push this folder to a new GitHub
repo (e.g. cpamath6day7) and connect it on Streamlit Community Cloud as
cpamath6day7.streamlit.app, then add the card to the launcher app.
"""

import random
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import streamlit as st

# ----------------------------------------------------------------------
# Page config & theme
# ----------------------------------------------------------------------
st.set_page_config(page_title="Day 7 — Area of Compound Rectangles", page_icon="📐", layout="wide")

NAVY = "#1b3a5c"
NAVY_LIGHT = "#eef4fa"
NAVY_BORDER = "#2c4a6e"
GREEN = "#3f7d55"
GREEN_LIGHT = "#eef7f0"
GOLD = "#8a5a20"
GOLD_LIGHT = "#f6ecd9"
RED = "#b03a2e"
RED_LIGHT = "#fdf1ef"
PURPLE = "#5b3a7d"
PURPLE_LIGHT = "#f2eef7"

FILL_A = "#dbe8f6"   # piece A / kept region
FILL_B = "#f6e3c6"   # piece B
FILL_CUT = "#f6d0c9"  # subtracted / cut-out region

CUSTOM_CSS = f"""
<style>
.box {{
    border: 2px solid {NAVY};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    background: white;
}}
.pill {{
    display: inline-block;
    color: white;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    padding: 4px 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}}
.box-readaloud {{ border-color: {NAVY}; }}
.box-readaloud .pill {{ background: {NAVY}; }}
.box-readaloud p {{ font-style: italic; margin: 4px 0 0 0; }}

.box-literacy {{ border-color: {NAVY_BORDER}; background: {NAVY_LIGHT}; }}
.box-literacy .pill {{ background: {NAVY_BORDER}; }}

.box-existing {{ border-color: {GREEN}; background: {GREEN_LIGHT}; }}
.box-existing .pill {{ background: {GREEN}; }}

.box-tools {{ border-color: {GOLD}; background: {GOLD_LIGHT}; }}
.box-tools .pill {{ background: {GOLD}; }}

.box-observer {{ border: 2px dashed {RED}; background: {RED_LIGHT}; }}
.box-observer .pill {{ background: {RED}; }}

.box-method {{ border-color: {PURPLE}; background: {PURPLE_LIGHT}; }}
.box-method .pill {{ background: {PURPLE}; }}

.ask {{ color: {RED}; font-weight: 700; margin-top: 8px; }}

.roadmap-title {{ color: {NAVY}; font-weight: 700; font-size: 15px; margin-bottom: 0; }}
.roadmap-sub {{ color: #5a6672; font-size: 11.5px; margin-top: -4px; }}

.credit {{ text-align: center; color: #8a939c; font-size: 11px; margin-top: 18px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def box(kind, pill, body_html):
    st.markdown(
        f'<div class="box box-{kind}"><span class="pill">{pill}</span>{body_html}</div>',
        unsafe_allow_html=True,
    )


def read_aloud(text):
    box("readaloud", "🔊 READ ALOUD", f"<p>&ldquo;{text}&rdquo;</p>")


def ask_the_class(text):
    st.markdown(f'<p class="ask">❓ Ask the class: {text}</p>', unsafe_allow_html=True)


def attempt(key):
    k = f"attempts_{key}"
    st.session_state[k] = st.session_state.get(k, 0) + 1
    return st.session_state[k]


def explain(title, lines):
    body = "<br>".join(lines)
    st.markdown(
        f'<div class="box box-tools"><span class="pill">💡 {title}</span>{body}</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Drawing helpers (matplotlib, styled to match the Day 5/6 diagrams)
# ----------------------------------------------------------------------
def draw_grid(base, height, area_label=None, fill=FILL_A, edge=NAVY, figsize=(4.2, 3.2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.add_patch(patches.Rectangle((0, 0), base, height, facecolor=fill, edgecolor=edge, linewidth=2.2))
    for c in range(base + 1):
        ax.plot([c, c], [0, height], color="#9db6cc", linewidth=0.6)
    for r in range(height + 1):
        ax.plot([0, base], [r, r], color="#9db6cc", linewidth=0.6)
    if area_label:
        ax.text(base / 2, height / 2, area_label, ha="center", va="center",
                 fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xlim(-0.6, base + 0.6)
    ax.set_ylim(-0.6, height + 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_L_add(a_base, a_height, top_width, b_height):
    """L shape by ADDITION: bottom piece (a_base x a_height) + top piece
    (top_width x b_height), sitting flush against the left edge."""
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ax.add_patch(Rectangle((0, 0), a_base, a_height, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))
    ax.add_patch(Rectangle((0, a_height), top_width, b_height, facecolor=FILL_B, edgecolor=NAVY, linewidth=2.2))
    ax.plot([0, top_width], [a_height, a_height], linestyle="--", color=GOLD, linewidth=1.6)
    ax.text(top_width / 2, a_height + b_height / 2, f"A\n{top_width}×{b_height}={top_width*b_height}",
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.text(a_base / 2, a_height / 2, f"B\n{a_base}×{a_height}={a_base*a_height}",
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.2, a_base + 1.2)
    ax.set_ylim(-1.2, a_height + b_height + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_L_subtract(a_base, a_height, top_width, b_height):
    """The SAME L shape, found by enclosing it in one big rectangle and
    subtracting the notch that isn't actually part of the floor."""
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    big_h = a_height + b_height
    notch_w = a_base - top_width
    # big bounding rectangle, lightly filled
    ax.add_patch(Rectangle((0, 0), a_base, big_h, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))
    if notch_w > 0:
        ax.add_patch(Rectangle((top_width, a_height), notch_w, b_height,
                                facecolor=FILL_CUT, edgecolor=RED, linewidth=1.8, hatch="///"))
        ax.text(top_width + notch_w / 2, a_height + b_height / 2,
                f"cut out\n{notch_w}×{b_height}={notch_w*b_height}",
                ha="center", va="center", fontsize=9.5, fontweight="bold", color=RED)
    ax.text(a_base / 2, big_h + 0.7, f"big rectangle: {a_base}×{big_h}={a_base*big_h}",
            ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.2, a_base + 1.2)
    ax.set_ylim(-1.2, big_h + 2.0)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def draw_T_shape(top_w, top_h, stem_w, stem_h):
    """T shape: a top bar (top_w x top_h) centered above a narrower stem
    (stem_w x stem_h)."""
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    stem_x = (top_w - stem_w) / 2
    ax.add_patch(Rectangle((0, stem_h), top_w, top_h, facecolor=FILL_A, edgecolor=NAVY, linewidth=2.2))
    ax.add_patch(Rectangle((stem_x, 0), stem_w, stem_h, facecolor=FILL_B, edgecolor=NAVY, linewidth=2.2))
    ax.plot([0, top_w], [stem_h, stem_h], linestyle="--", color=GOLD, linewidth=1.4)
    ax.plot([stem_x, stem_x], [0, stem_h], linestyle="--", color=GOLD, linewidth=1.0)
    ax.plot([stem_x + stem_w, stem_x + stem_w], [0, stem_h], linestyle="--", color=GOLD, linewidth=1.0)
    ax.text(top_w / 2, stem_h + top_h / 2, f"A\n{top_w}×{top_h}={top_w*top_h}",
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.text(stem_x + stem_w / 2, stem_h / 2, f"B\n{stem_w}×{stem_h}={stem_w*stem_h}",
            ha="center", va="center", fontsize=11, fontweight="bold", color=NAVY)
    ax.set_xlim(-1.2, top_w + 1.2)
    ax.set_ylim(-1.2, stem_h + top_h + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def random_L():
    a_base = random.randint(8, 14)
    a_height = random.randint(3, 6)
    top_width = random.randint(3, a_base - 2)
    b_height = random.randint(2, 5)
    return a_base, a_height, top_width, b_height


def random_T():
    top_w = random.randint(8, 14)
    top_h = random.randint(2, 4)
    stem_w = random.randint(3, top_w - 3)
    stem_h = random.randint(3, 6)
    return top_w, top_h, stem_w, stem_h


# ----------------------------------------------------------------------
# Sidebar — Sign In + Roadmap (mirrors Day 5 / Day 6)
# ----------------------------------------------------------------------
with st.sidebar:
    st.subheader("Sign In")
    st.text_input("Your name:", key="student_name")
    st.selectbox("Choose your shape avatar:", ["Rectangle", "Square", "L-Shape", "T-Shape", "Hexagon"], key="avatar")
    st.selectbox(
        "Pick your learning mode:",
        ["Focus Champ", "Growth Mode", "Problem Solver", "Data Boss", "Brain Builder"],
        key="learning_mode",
    )
    st.markdown("---")
    st.markdown('<p class="roadmap-title">Day 7 Roadmap</p>', unsafe_allow_html=True)
    st.markdown('<p class="roadmap-sub">55-minute period — Area of Compound Rectangles</p>', unsafe_allow_html=True)

    steps = [
        "1. Welcome Back",
        "2. Warm-Up Recitation",
        "3. Try It: The New Floor Plan",
        "4. Model It: Add or Subtract",
        "5. Discuss It & Connect It",
        "6. Practice: Mixed Shapes",
        "7. Engage / Explore / Enrich",
        "8. Apply It: Exit Ticket",
        "9. Journal & What You Just Did",
    ]
    if "step" not in st.session_state:
        st.session_state.step = 0
    for i, label in enumerate(steps):
        marker = "▶ " if i == st.session_state.step else ""
        if st.button(marker + label, key=f"nav_{i}", use_container_width=True):
            st.session_state.step = i
            st.rerun()
    st.markdown("---")
    st.caption("Lesson mode: i-Ready Classroom Mathematics session flow — Explore, Model It (two ways), Try It, Discuss It & Connect It, Apply It — applied to compound rectangles.")
    st.caption("Standards: 6.G.A.1 (grade-level) · 3.MD.C.7d (repair/foundation) · MP.1 · MP.7")

# ----------------------------------------------------------------------
# Roadmap step content
# ----------------------------------------------------------------------
step = st.session_state.step
name = st.session_state.get("student_name", "") or "class"

st.markdown(f"## {steps[step]}")
st.progress((step + 1) / len(steps))

if step == 0:
    box(
        "observer",
        "🔎 OBSERVER NOTE — carried from Day 6",
        "<p style='margin:0'>Most students could split a simple L-shaped floor into two rectangles "
        "when the split was already drawn for them, but several froze when asked to decide WHERE to "
        "draw the split themselves, and almost no one thought to try surrounding the shape in one big "
        "rectangle and subtracting instead. Day 7 opens by naming both moves on purpose and giving "
        "students a real choice between them.</p>",
    )
    read_aloud(
        "Yesterday you split an L-shaped floor into two rectangles and added the pieces. That's one way "
        "to handle a shape that isn't a single rectangle — we call any shape built out of rectangles a "
        "compound figure, or a composite figure. Today you get a second tool for the same job, you get "
        "to choose which tool fits a shape best, and you'll use both tools on shapes trickier than "
        "yesterday's — including one shaped like a T."
    )
    box(
        "literacy",
        "📖 MATH LITERACY: UNLOCK THE WORDS",
        "A <b>compound</b> (or <b>composite</b>) figure is a shape made of two or more simpler shapes "
        "put together. <b>Decompose</b> means to break a shape into smaller pieces you already know how "
        "to find the area of. Today every piece will be a rectangle, so &ldquo;decompose&rdquo; will "
        "always mean &ldquo;cut into rectangles.&rdquo;",
    )
    box(
        "existing",
        "🧠 EXISTING KNOWLEDGE",
        "Think about a real room shaped like an L — maybe a kitchen that opens into a dining nook. If "
        "someone asked you &ldquo;how much flooring do we need,&rdquo; you would never see a single "
        "clean rectangle. You'd have to see the room as pieces, or see it as a big rectangle with a "
        "corner missing. Both are correct — they're just two different ways of looking at the exact "
        "same floor."
        "<div class='class-question'></div>",
    )
    ask_the_class(
        "Picture a room shaped like a plus sign (+). Could you find its area by adding pieces together? "
        "Could you find it by starting with one big square and subtracting corners? Which sounds easier?"
    )
    box("tools", "Today's tools",
        "Graph paper and colored pencils &middot; floor tiles or a taped grid on the classroom floor "
        "&middot; journal &middot; exit ticket &middot; today's classwork worksheet.")

elif step == 1:
    st.write("**Purpose:** A fast recitation that rehearses BOTH moves — add the pieces, or subtract the "
             "missing piece — before any drawing begins.")
    box("tools", "How to run it",
        "Read one prompt card at a time. Students chorally finish the sentence with the operation and "
        "the answer. Alternate an &ldquo;add the pieces&rdquo; card with a &ldquo;subtract the missing "
        "piece&rdquo; card.")

    cards = [
        ("Add the pieces: a floor is two rectangles, 8×3 and 4×2",
         "8×3 = 24 and 4×2 = 8. 24 + 8 = 32 square units."),
        ("Subtract the missing piece: a 10×6 rectangle is missing a 3×2 corner",
         "10×6 = 60 and 3×2 = 6. 60 − 6 = 54 square units."),
        ("Add the pieces: a T-shape is 9×2 on top and 3×5 for the stem",
         "9×2 = 18 and 3×5 = 15. 18 + 15 = 33 square units."),
        ("Subtract the missing piece: a 12×7 rectangle is missing a 5×3 corner",
         "12×7 = 84 and 5×3 = 15. 84 − 15 = 69 square units."),
        ("(reverse!) Two pieces add to 50 square units; one piece is 30",
         "50 − 30 = 20 square units for the other piece."),
        ("(reverse!) A big rectangle is 45 and the cut-out is 45 minus the shape's 33",
         "45 − 33 = 12 square units were cut out."),
    ]
    if "recite_idx" not in st.session_state:
        st.session_state.recite_idx = 0
    idx = st.session_state.recite_idx
    prompt, answer = cards[idx]
    st.markdown(f"#### Card {idx + 1} of {len(cards)}")
    st.info(f"**Teacher reads:** {prompt}")
    if st.button("🔊 Reveal the class recitation"):
        st.success(answer)
    c1, c2 = st.columns(2)
    if c1.button("⬅ Previous card") and idx > 0:
        st.session_state.recite_idx -= 1
        st.rerun()
    if c2.button("Next card ➡") and idx < len(cards) - 1:
        st.session_state.recite_idx += 1
        st.rerun()
    ask_the_class("In cards 1 and 3, which operation did we use? In cards 2 and 4? What word in the "
                  "sentence told you which one to pick?")

elif step == 2:
    read_aloud(
        "Here's today's floor. It's the same L-shape idea as yesterday, but you get to pick where the "
        "split goes, and this time we'll also check it by surrounding it and subtracting."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        a_base = st.slider("Bottom piece width (ft)", 6, 14, 10, key="t_abase")
        a_height = st.slider("Bottom piece height (ft)", 2, 8, 4, key="t_aheight")
    with col2:
        top_width = st.slider("Top piece width (ft)", 2, a_base - 1, min(6, a_base - 1), key="t_topw")
        b_height = st.slider("Top piece height (ft)", 1, 6, 3, key="t_bheight")
    with col3:
        fig = draw_L_add(a_base, a_height, top_width, b_height)
        st.pyplot(fig, use_container_width=False)

    area_a = top_width * b_height
    area_b = a_base * a_height
    total = area_a + area_b
    st.write("Fill in each piece, then the total:")
    g1, g2, g3 = st.columns(3)
    ga = g1.number_input("Area A (sq ft)", min_value=0, step=1, key="try_ga")
    gb = g2.number_input("Area B (sq ft)", min_value=0, step=1, key="try_gb")
    gt = g3.number_input("Total area (sq ft)", min_value=0, step=1, key="try_gt")
    if st.button("Check", key="check_tryit"):
        n = attempt("tryit7")
        if ga == area_a and gb == area_b and gt == total:
            st.balloons()
            st.success(f"Correct! {top_width}×{b_height} + {a_base}×{a_height} = {area_a} + {area_b} = {total} sq ft.")
        else:
            st.error("Not quite yet — check each piece against the picture, then re-add.")
            if n >= 2:
                explain("Redo help", [
                    f"Piece A: {top_width} × {b_height} = <b>{area_a}</b> sq ft.",
                    f"Piece B: {a_base} × {a_height} = <b>{area_b}</b> sq ft.",
                    f"Total: {area_a} + {area_b} = <b>{total}</b> sq ft.",
                ])
    ask_the_class("Where exactly did you draw the split line? Could a different student have split this "
                  "same shape in a different place and still gotten the same total?")

elif step == 3:
    read_aloud(
        "Same floor, second tool. Instead of splitting it into two pieces and adding, picture ONE big "
        "rectangle that completely surrounds the shape, then subtract the corner that isn't really "
        "there. This works because the L-shape is just a rectangle with a bite taken out of it."
    )
    box("method", "MODEL IT — Method 1: Decompose and ADD",
        "Cut the compound figure into rectangles you already know. Find each piece's area. "
        "<b>Add</b> the pieces together.")
    box("method", "MODEL IT — Method 2: Enclose and SUBTRACT",
        "Draw the smallest rectangle that completely encloses the shape. Find its area. Find the area "
        "of the extra piece that got included but isn't part of the shape. <b>Subtract</b> it.")

    col1, col2 = st.columns(2)
    with col1:
        m_abase = st.slider("Bottom width (ft)", 6, 14, 10, key="m_abase")
        m_aheight = st.slider("Bottom height (ft)", 2, 8, 4, key="m_aheight")
    with col2:
        m_topw = st.slider("Top width (ft)", 2, m_abase - 1, min(6, m_abase - 1), key="m_topw")
        m_bheight = st.slider("Top height (ft)", 1, 6, 3, key="m_bheight")

    left, right = st.columns(2)
    with left:
        st.markdown("**Method 1 — Add**")
        st.pyplot(draw_L_add(m_abase, m_aheight, m_topw, m_bheight), use_container_width=False)
        add_total = m_topw * m_bheight + m_abase * m_aheight
        st.markdown(f"{m_topw}×{m_bheight} + {m_abase}×{m_aheight} = **{add_total} sq ft**")
    with right:
        st.markdown("**Method 2 — Subtract**")
        st.pyplot(draw_L_subtract(m_abase, m_aheight, m_topw, m_bheight), use_container_width=False)
        big = m_abase * (m_aheight + m_bheight)
        cut = (m_abase - m_topw) * m_bheight
        sub_total = big - cut
        st.markdown(f"{m_abase}×{m_aheight + m_bheight} − {m_abase - m_topw}×{m_bheight} = {big} − {cut} = **{sub_total} sq ft**")

    if add_total == sub_total:
        st.success(f"Both methods agree: **{add_total} square feet** — same shape, same answer, two honest paths there.")
    ask_the_class("Both pictures show the exact same floor. Why does it make sense that they give the "
                  "same total? Which method would you reach for first, and why?")

elif step == 4:
    read_aloud(
        "Now a shape where the choice is less obvious: a T. Look at it for a moment before touching any "
        "slider. Which method feels faster for THIS shape — add or subtract?"
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        top_w = st.slider("Top bar width (ft)", 8, 14, 10, key="tshape_topw")
        top_h = st.slider("Top bar height (ft)", 2, 4, 2, key="tshape_toph")
    with col2:
        max_stem = top_w - 3
        stem_w = st.slider("Stem width (ft)", 3, max_stem, min(4, max_stem), key="tshape_stemw")
        stem_h = st.slider("Stem height (ft)", 3, 6, 4, key="tshape_stemh")
    with col3:
        st.pyplot(draw_T_shape(top_w, top_h, stem_w, stem_h), use_container_width=False)

    area_a = top_w * top_h
    area_b = stem_w * stem_h
    total = area_a + area_b
    st.markdown(f"**Area A** (top bar) = {top_w} × {top_h} = {area_a} sq ft")
    st.markdown(f"**Area B** (stem) = {stem_w} × {stem_h} = {area_b} sq ft")
    st.markdown(f"### Total area = {area_a} + {area_b} = **{total} sq ft**")
    st.info(
        "Notice: a T-shape has TWO notches (one on each side of the stem), not one. Enclosing it in a "
        "big rectangle would mean subtracting two corners instead of one — for this shape, most people "
        "find **adding the two pieces** faster than subtracting two corners."
    )
    ask_the_class("Was your first instinct add or subtract for the T-shape? Now think of a shape where "
                  "subtract would clearly win — what would it look like?")

elif step == 5:
    st.write("**Practice — Mixed Shapes.** Some problems are L-shapes, some are T-shapes. Pick your "
             "method, solve, then check.")
    if "practice_problem" not in st.session_state:
        st.session_state.practice_problem = None
    if "practice_kind" not in st.session_state:
        st.session_state.practice_kind = None

    def new_practice():
        kind = random.choice(["L", "T"])
        st.session_state.practice_kind = kind
        if kind == "L":
            st.session_state.practice_problem = random_L()
        else:
            st.session_state.practice_problem = random_T()

    if st.session_state.practice_problem is None:
        new_practice()

    kind = st.session_state.practice_kind
    p = st.session_state.practice_problem
    if kind == "L":
        a_base, a_height, top_width, b_height = p
        st.pyplot(draw_L_add(a_base, a_height, top_width, b_height), use_container_width=False)
        answer = a_base * a_height + top_width * b_height
        st.caption("This is an L-shape — the dashed line shows one valid split, but you may solve it "
                   "any correct way.")
    else:
        top_w, top_h, stem_w, stem_h = p
        st.pyplot(draw_T_shape(top_w, top_h, stem_w, stem_h), use_container_width=False)
        answer = top_w * top_h + stem_w * stem_h
        st.caption("This is a T-shape.")

    guess = st.number_input("Total area (square units):", min_value=0, step=1, key=f"practice_guess_{id(p)}")
    c1, c2 = st.columns(2)
    if c1.button("Check answer", key="practice_check"):
        n = attempt("practice7")
        if guess == answer:
            st.balloons()
            st.success(f"Correct! Total area = {answer} square units.")
        else:
            st.error(f"Not yet. Total area = {answer} square units. Try decomposing it again.")
            if n >= 2:
                if kind == "L":
                    explain("Redo help", [
                        f"Piece A (top): {top_width} × {b_height} = <b>{top_width*b_height}</b>.",
                        f"Piece B (bottom): {a_base} × {a_height} = <b>{a_base*a_height}</b>.",
                        f"Add: {top_width*b_height} + {a_base*a_height} = <b>{answer}</b>.",
                    ])
                else:
                    explain("Redo help", [
                        f"Piece A (top bar): {top_w} × {top_h} = <b>{top_w*top_h}</b>.",
                        f"Piece B (stem): {stem_w} × {stem_h} = <b>{stem_w*stem_h}</b>.",
                        f"Add: {top_w*top_h} + {stem_w*stem_h} = <b>{answer}</b>.",
                    ])
    if c2.button("New problem", key="practice_new"):
        new_practice()
        st.rerun()

elif step == 6:
    st.markdown("#### Engage / Explore / Enrich stations")
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown(
            """
            <div class="box box-tools">
            <span class="pill">Engage · with teacher</span>
            <i>Still unsure where to draw the split line.</i><br><br>
            1. Physically cut a paper L-shape into two rectangles. Trace and label each piece.<br>
            2. Rebuild the same L-shape from two pre-cut rectangles instead — same total, both ways.<br>
            3. Today's worksheet, Part 1 only (add-the-pieces problems).
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e2:
        st.markdown(
            """
            <div class="box box-existing">
            <span class="pill">Explore · independent</span>
            <i>Comfortable adding pieces; ready to try subtracting.</i><br><br>
            1. Today's worksheet, Parts 1 and 2 (add AND subtract problems).<br>
            2. Solve one L-shape problem BOTH ways and confirm the totals match.<br>
            3. <a href="https://www.ixl.com/math/grade-6/area-of-compound-figures" target="_blank" rel="noopener noreferrer">📝 HMWK — IXL <b>GG.11</b>: Area of compound figures</a>.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with e3:
        st.markdown(
            """
            <div class="box box-method">
            <span class="pill">Enrich · previews parallelograms</span>
            <i>Fluent with both methods, finished early.</i><br><br>
            1. A room is a 12 ft × 9 ft rectangle with a 4 ft × 3 ft triangular corner cut off (not a "
            rectangle cut-out — a diagonal cut). Can you still use subtract? What's different about "
            finding the cut piece's area now?<br>
            2. Design your own 3-piece compound figure (an L plus a notch, or a plus-sign) and swap with "
            a partner to solve.<br>
            3. IXL <b>GG.12</b> Area of compound figures with triangles.
            </div>
            """,
            unsafe_allow_html=True,
        )
    box("existing", "✏️ Homework reminder",
        "Show ALL work by hand — pencil and paper (graph paper is best), written out in your math "
        "notebook, including which method (add or subtract) you used for each problem.")
    st.markdown("**Board self-check** — which board are you on?")
    board = st.radio("", ["Engage", "Explore", "Enrich"], horizontal=True, key="board_pick", label_visibility="collapsed")
    st.info(f"{name or 'You'} → **{board}** board. Grab your worksheet and go.")

elif step == 7:
    read_aloud("Exit ticket. Silent. Show your method — add or subtract — for every problem.")
    st.markdown("**1.** A floor is two rectangles: 9 ft × 3 ft and 5 ft × 4 ft. Total area?")
    q1 = st.number_input("Answer 1 (sq ft)", 0, 500, step=1, key="et7_1")
    st.markdown("**2.** A 11 ft × 8 ft rectangle is missing a 4 ft × 3 ft corner. Total area?")
    q2 = st.number_input("Answer 2 (sq ft)", 0, 500, step=1, key="et7_2")
    st.markdown("**3.** A T-shape has a top bar 10 ft × 2 ft and a stem 4 ft × 5 ft. Total area?")
    q3 = st.number_input("Answer 3 (sq ft)", 0, 500, step=1, key="et7_3")
    enrich = st.checkbox("I'm on the Enrich board — show problem 4", key="et7_enrich")
    q4 = None
    if enrich:
        st.markdown("**4.** A 14 ft × 10 ft rectangle is missing a 6 ft × 3 ft corner AND a separate "
                     "2 ft × 2 ft corner. Total area?")
        q4 = st.number_input("Answer 4 (sq ft)", 0, 500, step=1, key="et7_4")
    if st.button("Submit exit ticket", key="et7_submit", use_container_width=True):
        n = attempt("exit7")
        results = [
            (q1 == 47, "47", ["9×3 = 27 and 5×4 = 20.", "27 + 20 = <b>47</b>."]),
            (q2 == 76, "76", ["11×8 = 88 and 4×3 = 12.", "88 − 12 = <b>76</b>."]),
            (q3 == 40, "40", ["10×2 = 20 and 4×5 = 20.", "20 + 20 = <b>40</b>."]),
        ]
        if enrich:
            results.append((q4 == 118, "118", ["14×10 = 140.", "Subtract the first corner: 140 − 6×3 = 140 − 18 = 122.", "Subtract the second corner: 122 − 2×2 = 122 − 4 = <b>118</b>."]))
        score = sum(1 for ok, _, _ in results if ok)
        for i, (ok, ans, why) in enumerate(results, start=1):
            if ok:
                st.success(f"Problem {i}: ✔ {ans}")
            else:
                st.error(f"Problem {i}: ✘")
                if n >= 2:
                    explain(f"Problem {i} — how to get it", why)
        if score == len(results):
            st.balloons()
        elif n == 1:
            st.info("Fix any ✘ and submit again — the second submit shows how each one works.")
        st.markdown(f"**{name or 'Student'}: {score} / {len(results)}**")

elif step == 8:
    read_aloud(
        "Journal: draw your own compound figure made of exactly three rectangles, worth at least 50 "
        "square units. Solve it your own way, then challenge a partner to solve it a DIFFERENT way and "
        "check that your totals match."
    )
    j = st.text_area("Journal (optional — write it on paper too):", height=110, key="journal7")
    if j.strip():
        st.success("Journaled. Hand-drawn version goes in your notebook.")

    st.markdown("---")
    icans = [
        ("DECOMPOSE", "I can decompose a compound figure into rectangles and add their areas. (6.G.A.1)"),
        ("ENCLOSE", "I can enclose a compound figure in a rectangle and subtract the extra piece. (6.G.A.1)"),
        ("CHOOSE", "I can choose whichever method — add or subtract — is more efficient for a shape. (MP.1)"),
        ("STRUCTURE", "I can see the same shape two different correct ways and get the same area. (MP.7)"),
        ("REPAIR", "I can decompose a simple rectilinear shape into non-overlapping rectangles. (3.MD.C.7d)"),
    ]
    for tag, text in icans:
        st.markdown(f'<div class="box box-existing" style="border-left:6px solid {GOLD};padding:0.7rem 1rem;">'
                    f'<span class="pill" style="background:{NAVY};">{tag}</span>{text}</div>', unsafe_allow_html=True)
    st.caption(
        "Standards in play: 6.G.A.1 (grade-level composite area) · 3.MD.C.7d (repair — decompose "
        "rectilinear shapes into rectangles) · MP.1 (make sense of problems, choose a strategy) · "
        "MP.7 (use structure)."
    )
    st.markdown(
        f"""
        <div class="box box-tools">
        You walked in with ONE way to handle an L-shaped floor. You walked out with TWO — and the "
        judgment to pick between them.
        <br><br><b>{name or 'Mathematician'}, that choice is what makes you faster tomorrow, not just "
        today.</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
c_back, c_next = st.columns([1, 1])
if c_back.button("⬅ Back", disabled=(step == 0)):
    st.session_state.step = max(0, step - 1)
    st.rerun()
if c_next.button("Next ➡", disabled=(step == len(steps) - 1)):
    st.session_state.step = min(len(steps) - 1, step + 1)
    st.rerun()

st.caption("Standards in play: 6.G.A.1 (composite area) · 3.MD.C.7d (decompose rectilinear shapes — "
           "repair) · MP.1 · MP.7.")
st.markdown(
    "<div class='credit'>www.cognitivecloud.ai &middot; Developed by Xavier Honablue, M.Ed &middot; "
    "Chandler Park Academy</div>",
    unsafe_allow_html=True,
)
