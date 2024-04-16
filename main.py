import streamlit as st
from pybit.unified_trading import HTTP
import json

api_key = 'ULI4j96SQhGePVhxCu'
api_secret = 'XnBhumm73kDKJSFDFLKEZSLkkX2KwMvAj4qC'

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret,
)


def open_position(qty):
    try:
        order = session.place_order(
            category="linear",
            symbol="DEGENUSDT",
            side="Buy",
            orderType="Market",
            qty=qty,
        )
        st.write(f"Opened position for DEGENUSDT: {order}")
    except Exception as e:
        st.write(f"Error opening position for DEGENUSDT: {str(e)}")


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
        st.write(f"Closed position for DEGENUSDT: {order}")
    except Exception as e:
        st.write(f"Error closing position for DEGENUSDT: {str(e)}")


def handle_webhook(webhook_data):
    if webhook_data.get("passphrase") != "YOUR_WEBHOOK_PASSPHRASE":
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
            st.write("Invalid JSON format in the alert message.")
        except Exception as e:
            st.write(f"Error processing webhook: {str(e)}")


def main():
    st.title("TradingView Webhook Endpoint")

    webhook_data = st.experimental_get_query_params()
    handle_webhook(webhook_data)


if __name__ == "__main__":
    main()
