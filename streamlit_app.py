# streamlit_app.py
"""
Tiny Streamlit UI for the Local Web Agent.
Run: streamlit run streamlit_app.py
"""

import asyncio
import sys

# Fix for Windows + Streamlit + Playwright NotImplementedError
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

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

    if "actions" in res:
        st.markdown("### Actions log")
        for idx, a in enumerate(res["actions"], 1):
            st.write(f"### Action {idx}")
            st.write(f"**Type:** {a.get('action', '')}")
            st.write(f"**Engine:** {a.get('engine', '')}")
            results = a.get("results", [])
            if results:
                st.markdown("**Results:**")
                for i, result in enumerate(results[:5], 1):
                    st.write(f"{i}. {result}")
            else:
                st.write("No results found.")
    else:
        st.write("No actions to display.")
