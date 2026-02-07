# import os
# import datetime
# from collections import defaultdict

# import streamlit as st

# from challenge_config import get_random_fallback
# from ai_client import generate_challenge
# from progress_store import load_progress, save_progress, IMAGE_DIR


# # -------------------------------------------------
# # Page setup
# # -------------------------------------------------
# st.set_page_config(
#     page_title="TinyImpact: Daily Eco Challenge",
#     page_icon="🌱",
#     layout="centered",
# )

# st.title("🌱 TinyImpact: Daily Eco Challenge")
# st.write("Get one small, realistic eco-friendly action you can take **today**.")


# # -------------------------------------------------
# # Session State
# # -------------------------------------------------
# if "last_challenge" not in st.session_state:
#     st.session_state.last_challenge = None

# # Load all-time progress first
# if "progress_log" not in st.session_state:
#     st.session_state.progress_log = load_progress()

# # Now base the counter on the length of the log
# if "completed_count" not in st.session_state:
#     st.session_state.completed_count = len(st.session_state.progress_log)


# # -------------------------------------------------
# # Tiny stats bar
# # -------------------------------------------------
# st.markdown(
#     f"""
# <div style="padding:0.6rem 1rem; border-radius:0.75rem; background:#f0f9f4;
#             border:1px solid #c7ebd6; margin-bottom:1rem;">
#   <strong>✨ TinyImpact score:</strong>
#   You’ve completed <strong>{st.session_state.completed_count}</strong>
#   challenge(s) this session.
# </div>
# """,
#     unsafe_allow_html=True,
# )

# # -------------------------------------------------
# # Tabs
# # -------------------------------------------------
# tab_today, tab_progress = st.tabs(["🌍 Today's Challenge", "📅 My Progress"])


# # =================================================
# # TAB 1 — TODAY'S CHALLENGE (WITH ENTER SUPPORT)
# # =================================================
# with tab_today:
#     with st.form("challenge_form"):
#         st.markdown("### Tell us a bit about your day:")

#         living_choice = st.selectbox(
#             "Where do you live?",
#             ["Dorm", "Apartment", "House", "Shared housing", "Other"],
#         )

#         if living_choice == "Other":
#             custom_living = st.text_input(
#                 "Please specify where you live:",
#                 placeholder="e.g., Studio, Townhouse, Family home",
#             )
#             resolved_living = custom_living.strip()
#         else:
#             resolved_living = living_choice

#         time_minutes = st.slider(
#             "How much time do you have today?",
#             5, 60, 10, 5
#         )

#         focus_areas = st.multiselect(
#             "What do you want to focus on?",
#             ["Waste", "Energy", "Food", "Transport", "Water", "Digital"],
#             default=["Waste"],
#         )

#         difficulty = st.radio(
#             "How hard should it be?",
#             ["Easy", "Medium", "Ambitious"],
#         )

#         st.markdown("---")

#         col1, col2 = st.columns([2, 1])
#         with col1:
#             generate_submit = st.form_submit_button(
#                 "✨ Generate Today's Challenge", type="primary"
#             )
#         with col2:
#             regen_submit = st.form_submit_button("🔁 New one")

#     # -------- Form submission logic --------
#     if generate_submit or regen_submit:
#         if living_choice == "Other" and not resolved_living:
#             st.warning("Please specify where you live before generating a challenge.")
#         else:
#             with st.spinner("Thinking of a tiny impact you can make today..."):
#                 data = generate_challenge(
#                     living_situation=resolved_living,
#                     time_minutes=time_minutes,
#                     focus_areas=focus_areas,
#                     difficulty=difficulty,
#                 )

#                 if not data:
#                     data = get_random_fallback(focus_areas)

#                 st.session_state.last_challenge = data

#     st.markdown("---")

#     # -------- Display challenge --------
#     challenge = st.session_state.last_challenge

#     if challenge:
#         st.subheader("🌍 Today's Challenge")
#         st.markdown(f"**Challenge:** {challenge['challenge']}")
#         st.markdown(f"**Why it matters:** {challenge['why_it_matters']}")
#         st.markdown(f"**Impact estimate:** {challenge['impact_estimate']}")
#         st.caption(f"Category: {challenge['category']}")

#         st.markdown("### ✅ Mark as Done")

#         uploaded_image = st.file_uploader(
#             "Optional: upload a photo of what you did",
#             type=["jpg", "jpeg", "png"],
#         )

#         save_btn = st.button("✅ I did this & save today's progress")

#         if save_btn:
#             st.session_state.completed_count += 1
#             os.makedirs(IMAGE_DIR, exist_ok=True)

#             image_filename = None
#             if uploaded_image:
#                 today = datetime.date.today().isoformat()
#                 image_filename = f"{today}_{len(st.session_state.progress_log)+1}.jpg"
#                 with open(os.path.join(IMAGE_DIR, image_filename), "wb") as f:
#                     f.write(uploaded_image.getbuffer())

#             entry = {
#                 "date": datetime.date.today().isoformat(),
#                 "challenge": challenge["challenge"],
#                 "why_it_matters": challenge["why_it_matters"],
#                 "impact_estimate": challenge["impact_estimate"],
#                 "category": challenge["category"],
#                 "image_filename": image_filename,
#             }

#             st.session_state.progress_log.append(entry)
#             save_progress(st.session_state.progress_log)

#             st.success("Saved! Tiny action → real impact 🌱")
#     else:
#         st.info("Click **Generate Today's Challenge** or press Enter to begin.")


# # =================================================
# # TAB 2 — MY PROGRESS
# # =================================================
# with tab_progress:
#     log = st.session_state.progress_log

#     if not log:
#         st.info("No progress yet. Complete a challenge to see it here!")
#     else:
#         st.markdown("### 📅 Your Progress History")

#         grouped = defaultdict(list)
#         for e in log:
#             grouped[e["date"]].append(e)

#         for date in sorted(grouped.keys(), reverse=True):
#             st.markdown(f"#### {date}")
#             for e in grouped[date]:
#                 st.markdown(f"**Challenge:** {e['challenge']}")
#                 st.caption(f"Category: {e['category']}")

#                 if e["image_filename"]:
#                     img_path = os.path.join(IMAGE_DIR, e["image_filename"])
#                     if os.path.exists(img_path):
#                         st.image(img_path, use_container_width=True)

#                 st.markdown(f"*Why:* {e['why_it_matters']}")
#                 st.markdown(f"*Impact:* {e['impact_estimate']}")
#                 st.markdown("---")






import os
import datetime
from collections import defaultdict

import streamlit as st

from challenge_config import get_random_fallback
from ai_client import generate_challenge
from progress_store import load_progress, save_progress, IMAGE_DIR


# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(
    page_title="TinyImpact: Daily Eco Challenge",
    page_icon="🌱",
    layout="centered",
)

st.title("🌱 TinyImpact: Daily Eco Challenge")
st.write("Get one small, realistic eco-friendly action you can take **today**.")


# -------------------------------------------------
# Session State
# -------------------------------------------------
if "last_challenge" not in st.session_state:
    st.session_state.last_challenge = None

if "progress_log" not in st.session_state:
    st.session_state.progress_log = load_progress()


# -------------------------------------------------
# TinyImpact score bar (placeholder)
#   We define the placeholder here so it appears at the top,
#   but we'll fill it AFTER all state updates.
# -------------------------------------------------
score_placeholder = st.empty()

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab_today, tab_progress = st.tabs(["🌍 Today's Challenge", "📅 My Progress"])


# =================================================
# TAB 1 — TODAY'S CHALLENGE (WITH ENTER SUPPORT)
# =================================================
with tab_today:
    # Use a form so Enter submits the form
    with st.form("challenge_form"):
        st.markdown("### Tell us a bit about your day:")

        living_choice = st.selectbox(
            "Where do you live?",
            ["Dorm", "Apartment", "House", "Shared housing", "Other"],
        )

        if living_choice == "Other":
            custom_living = st.text_input(
                "Please specify where you live:",
                placeholder="e.g., Studio, Townhouse, Family home",
            )
            resolved_living = custom_living.strip()
        else:
            resolved_living = living_choice

        time_minutes = st.slider(
            "How much time do you have today?",
            5, 60, 10, 5
        )

        focus_areas = st.multiselect(
            "What do you want to focus on?",
            ["Waste", "Energy", "Food", "Transport", "Water", "Digital"],
            default=["Waste"],
        )

        difficulty = st.radio(
            "How hard should it be?",
            ["Easy", "Medium", "Ambitious"],
        )

        st.markdown("---")

        col1, col2 = st.columns([2, 1])
        with col1:
            generate_submit = st.form_submit_button(
                "✨ Generate Today's Challenge", type="primary"
            )
        with col2:
            regen_submit = st.form_submit_button("🔁 New one")

    # -------- Form submission logic --------
    if generate_submit or regen_submit:
        if living_choice == "Other" and not resolved_living:
            st.warning("Please specify where you live before generating a challenge.")
        else:
            with st.spinner("Thinking of a tiny impact you can make today..."):
                data = generate_challenge(
                    living_situation=resolved_living,
                    time_minutes=time_minutes,
                    focus_areas=focus_areas,
                    difficulty=difficulty,
                )

                if not data:
                    data = get_random_fallback(focus_areas)

                st.session_state.last_challenge = data

    st.markdown("---")

    # -------- Display challenge --------
    challenge = st.session_state.last_challenge

    if challenge:
        st.subheader("🌍 Today's Challenge")
        st.markdown(f"**Challenge:** {challenge['challenge']}")
        st.markdown(f"**Why it matters:** {challenge['why_it_matters']}")
        st.markdown(f"**Impact estimate:** {challenge['impact_estimate']}")
        st.caption(f"Category: {challenge['category']}")

        st.markdown("### ✅ Mark as Done")

        uploaded_image = st.file_uploader(
            "Optional: upload a photo of what you did",
            type=["jpg", "jpeg", "png"],
        )

        save_btn = st.button("✅ I did this & save today's progress")

        if save_btn:
            os.makedirs(IMAGE_DIR, exist_ok=True)

            image_filename = None
            if uploaded_image:
                today = datetime.date.today().isoformat()
                # Simple unique filename
                image_filename = f"{today}_{len(st.session_state.progress_log)+1}.jpg"
                with open(os.path.join(IMAGE_DIR, image_filename), "wb") as f:
                    f.write(uploaded_image.getbuffer())

            entry = {
                "date": datetime.date.today().isoformat(),
                "challenge": challenge["challenge"],
                "why_it_matters": challenge["why_it_matters"],
                "impact_estimate": challenge["impact_estimate"],
                "category": challenge["category"],
                "image_filename": image_filename,
            }

            st.session_state.progress_log.append(entry)
            save_progress(st.session_state.progress_log)

            st.success("Saved! Tiny action → real impact 🌱")
    else:
        st.info("Click **Generate Today's Challenge** or press Enter to begin.")


# =================================================
# TAB 2 — MY PROGRESS
# =================================================
with tab_progress:
    log = st.session_state.progress_log

    if not log:
        st.info("No progress yet. Complete a challenge to see it here!")
    else:
        st.markdown("### 📅 Your Progress History")

        grouped = defaultdict(list)
        for e in log:
            grouped[e["date"]].append(e)

        for date in sorted(grouped.keys(), reverse=True):
            st.markdown(f"#### {date}")
            for e in grouped[date]:
                st.markdown(f"**Challenge:** {e['challenge']}")
                st.caption(f"Category: {e['category']}")

                if e["image_filename"]:
                    img_path = os.path.join(IMAGE_DIR, e["image_filename"])
                    if os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)

                st.markdown(f"*Why:* {e['why_it_matters']}")
                st.markdown(f"*Impact:* {e['impact_estimate']}")
                st.markdown("---")


# =================================================
# FINAL: render the TinyImpact score bar with
#        the LATEST total, after any state updates
# =================================================
total_completed = len(st.session_state.progress_log)

score_placeholder.markdown(
    f"""
<div style="padding:0.6rem 1rem; border-radius:0.75rem; background:#f0f9f4;
            border:1px solid #c7ebd6; margin-bottom:1rem;">
  <strong>✨ TinyImpact score:</strong>
  You’ve completed <strong>{total_completed}</strong> challenge(s) total.
</div>
""",
    unsafe_allow_html=True,
)
