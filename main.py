import streamlit as st
from pybit.unified_trading import HTTP
import json

api_key = 'ULI4j96SQhGePVhxCu'
api_secret = 'XnBhumm73kDKJSFDFLKEZSLkkX2KwMvAj4qC'
st.set_option("server.enableCORS", True)

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret,
)

log_messages = []

def open_position(qty):
    try:
        order = session.place_order(
            category="linear",
            symbol="DEGENUSDT",
            side="Buy",
            orderType="Market",
            qty=qty,
        )
        message = f"Opened position for DEGENUSDT: {order}"
        log_messages.append(message)
        st.write(message)
    except Exception as e:
        message = f"Error opening position for DEGENUSDT: {str(e)}"
        log_messages.append(message)
        st.write(message)

def close_position(qty):
    try:
        order = session.place_order(
            category="linear",
            symbol="DEGENUSDT",
            side="Sell",
            orderType="Market",
            qty=qty,
            reduce_only=True,
            close_on_trigger=False,
        )
        message = f"Closed position for DEGENUSDT: {order}"
        log_messages.append(message)
        st.write(message)
    except Exception as e:
        message = f"Error closing position for DEGENUSDT: {str(e)}"
        log_messages.append(message)
        st.write(message)

def handle_webhook(webhook_data):
    if webhook_data.get("passphrase") != "Armjansk12!!":
        return

    alert_message = webhook_data.get("message")

    if alert_message:
        try:
            alert_data = json.loads(alert_message)
            qty = alert_data.get("qty")
            action = alert_data.get("action")

            if action == "buy":
                open_position(qty)
            elif action == "sell":
                close_position(qty)
        except json.JSONDecodeError:
            message = "Invalid JSON format in the alert message."
            log_messages.append(message)
            st.write(message)
        except Exception as e:
            message = f"Error processing webhook: {str(e)}"
            log_messages.append(message)
            st.write(message)

def main():
    st.title("TradingView Webhook Endpoint")

    webhook_data = st.experimental_get_query_params()
    handle_webhook(webhook_data)

    st.header("Log")
    for message in log_messages:
        st.write(message)


if __name__ == "__main__":
    main()