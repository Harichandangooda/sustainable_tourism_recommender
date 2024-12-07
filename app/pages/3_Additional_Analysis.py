import streamlit as st
import streamlit.components.v1 as components

with open("Additional.html", "r") as f:
    html_content = f.read()

scrollable_html = f"""
<div style="overflow-y: auto; height: 700px; border: 1px solid #ddd; padding: 10px;">
    {html_content}
</div>
"""

components.html(scrollable_html, height=700)