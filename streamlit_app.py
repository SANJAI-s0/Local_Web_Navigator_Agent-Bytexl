# streamlit_app.py
"""
Tiny Streamlit UI for the Local Web Agent.
Run: streamlit run streamlit_app.py
"""

import streamlit as st
from agent.orchestrator import Orchestrator

st.set_page_config(page_title="Local Web Agent", layout="centered")
st.title("Local Web Agent (Local LLM + Playwright)")

st.markdown("Enter an instruction like: `search for laptops under 50k and list top 5`")

instr = st.text_area("Instruction", value="Search for laptops under 50k and list top 5", height=140)
col1, col2 = st.columns([1, 1])
headless = col1.checkbox("Headless browser", value=True)
run_btn = col2.button("Run")

if run_btn and instr.strip():
    st.info("Planning and running — this may take a few seconds.")
    orch = Orchestrator(headless=headless)
    with st.spinner("Executing..."):
        res = orch.run(instr.strip())
    st.success("Done")
    st.json(res)

    if "actions" in res:
        st.markdown("### Actions log")
        for a in res["actions"]:
            st.write(a)
