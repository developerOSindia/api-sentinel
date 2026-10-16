"""
API Sentinel - DeveloperOS Flagship Application
"""

import streamlit as st
import json
from core.sentinel_core import MockRouteRegistry
from ui.components import render_sentinel_header, render_sentinel_footer, render_main_promotional_banner

st.set_page_config(
    page_title="API Sentinel — DeveloperOS Flagship",
    page_icon="🛡️",
    layout="wide"
)

if "sentinel_registry" not in st.session_state:
    st.session_state.sentinel_registry = MockRouteRegistry()
    # Add seed demo route
    st.session_state.sentinel_registry.add_route(
        path="/v1/users",
        method="GET",
        status_code=200,
        response_body={"status": "ok", "users": [{"id": 1, "name": "DeveloperOS Engineer"}]}
    )


def main():
    render_sentinel_header()

    tab_test, tab_manage = st.tabs(["Dispatch Simulated Request", "Manage Mock Endpoints"])

    with tab_test:
        st.subheader("Simulate Incoming API Call")
        col_m, col_p = st.columns([1, 3])
        with col_m:
            method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
        with col_p:
            path = st.text_input("Endpoint Path", value="/v1/users")

        if st.button("Dispatch Request", type="primary"):
            res = st.session_state.sentinel_registry.simulate_request(path, method)
            if res["matched"]:
                st.success(f"Status: {res['status_code']} OK")
                st.json(res["body"])
            else:
                st.error(f"Status: 404 Not Found")
                st.json(res["body"])

    with tab_manage:
        st.subheader("Register New Mock Route")
        new_method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"], key="new_method")
        new_path = st.text_input("Path (e.g. /v1/products)", value="/v1/products")
        new_status = st.number_input("Response Status Code", value=200, min_value=100, max_value=599)
        new_body = st.text_area("JSON Response Payload", value='{"items": ["item1", "item2"]}')

        if st.button("Save Endpoint"):
            try:
                body_json = json.loads(new_body)
                st.session_state.sentinel_registry.add_route(new_path, new_method, int(new_status), body_json)
                st.success(f"Route '{new_method} {new_path}' registered successfully!")
            except json.JSONDecodeError as err:
                st.error(f"Invalid JSON payload: {err.msg}")

        st.divider()
        st.subheader("Registered Mock Routes")
        routes = st.session_state.sentinel_registry.list_routes()
        for r in routes:
            st.markdown(f"- **{r['method']}** `{r['path']}` -> `{r['status_code']}`")

    render_main_promotional_banner(tool_name="API Sentinel")
    render_sentinel_footer()


if __name__ == "__main__":
    main()
