import base64

with open("user_session.session", "rb") as f:
    session_bytes = f.read()
    session_b64 = base64.b64encode(session_bytes).decode()
    print("SESSION_BASE64 environment variable:")
    print(session_b64)
