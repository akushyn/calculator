import logging
import os

import requests  # type: ignore
import streamlit as st  # type: ignore

BACKEND_URL = os.getenv("BACKEND_URL", "")


@st.cache_resource
def configure_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return log


@st.cache_resource
def get_operators():
    logger.info("Get operators call")

    url = f"{BACKEND_URL.rstrip('/')}/operators/"
    response = requests.get(url)
    response.raise_for_status()

    logger.info("Get operators done")
    return response.json()


def calculate(expression: str, colorize: bool = False):
    data = {
        "expression": expression,
        "colorize": colorize,
    }
    logger.info(f"Calculation call: {data}")

    url = f"{BACKEND_URL}/calculate/"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        if response.status_code == 200:
            result = response.json()
            message = f"Calculation completed: {result}"
            logger.info(message)

            return response.json()
    except requests.exceptions.HTTPError as error:
        logger.error(
            f"HTTP Error: {str(error)}",
        )
        st.error("Calculation failed.")


logger = configure_logger()


def main():
    logger.info("Start rerun")
    st.title("Calculator Challenge")

    # get operators
    operators = get_operators()
    if "calculation_key" not in st.session_state:
        st.session_state.calculation_key = None

    # create a horizontal container
    container = st.container()

    with container:
        left_value = st.number_input("Enter the first number:")
        operator = st.selectbox("Select an operator:", operators)
        right_value = st.number_input("Enter the second number:")

        # colorize_checkbox = st.checkbox("Colorize Result")

        expression = f"{left_value}{operator}{right_value}"
        st.text_input(label="Expression", disabled=True, value=expression)

        if st.button("Calculate"):
            result = calculate(expression)
            result_value = result["result"]
            result_color = result.get("color")

            # display result with colored background
            st.markdown(
                f"<div style='background-color: {result_color}; padding: 10px;'>"
                f"Result: {result_value}</div>",
                unsafe_allow_html=True,
            )

    logger.info("End rerun")


if __name__ == "__main__":
    main()
