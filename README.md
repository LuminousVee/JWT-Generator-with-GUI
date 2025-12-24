# Production-Ready JWT Generator with GUI

This repository contains a Python script that provides a Graphical User Interface for generating JSON Web Tokens.It uses the modern **CustomTkinter** library for the GUI and 
 the industry-standard **PyJWT** library for token generation. This tool is designed to assist developers and security professionals in creating 
 and inspecting JWTs.

## Features

*   **Modern GUI:** Built with CustomTkinter for a modern, customizable look and feel, providing an intuitive user experience.
*   **Production-Ready Claims:** Automatically includes essential JWT claims for robust token management:
    *   `iat` (Issued At): Timestamp of when the token was issued.
    *   `exp` (Expiration Time): Timestamp after which the token is no longer valid.
    *   `nbf` (Not Before): Timestamp before which the token must not be accepted for processing.
    *   `iss` (Issuer): Identifies the principal that issued the JWT.
    *   `sub` (Subject): Identifies the principal that is the subject of the JWT.
    *   `jti` (JWT ID): A unique identifier for the JWT, useful for token revocation and tracking.
*   **Configurable:** Allows setting the **Secret Key**, **Algorithm** (e.g., HS256, RS256), **Expiration Time**, and **Custom Header** parameters directly from the GUI.
*   **JSON Payload Input:** Provides a dedicated text area for entering custom claims (the token's data) in JSON format, with pre-filled examples.
*   **Real-time Status:** Offers immediate feedback on the token generation process, displaying success messages or detailed error information.
*   **Token Tracking & Revocation Ready:** The automatic inclusion of the `jti` claim makes tokens suitable for backend systems implementing tracking and revocation mechanisms.

## Prerequisites

You need Python 3.6+ installed on your system.

## Installation

1.  **Clone the repository (or download the `jwt_generator.py` file):**
    ```bash
    git clone https://github.com/LuminousVee/JWT-Generator-with-GUI.git # Replace with actual repo URL
    cd repo-dir/
    ```
    (If you downloaded the file directly, navigate to its directory.)

2.  **Install dependencies:**
    Open your terminal or command prompt, navigate to the directory where you saved the file, and run the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the script:**

    ```bash
    python jwt_generator.py
    ```

2.  **Configure Parameters:**
    *   **Secret Key:** Enter the secret key used to sign the token. **This is crucial for security.**
    *   **Algorithm:** Select the desired signing algorithm from the dropdown (e.g., `HS256` for symmetric signing).
    *   **Expiry (Minutes):** Set the token's validity period in minutes (e.g., `60` for 1 hour).
    *   **Custom Header (JSON):** Modify the JWT header in JSON format if needed (defaults to `{"typ": "JWT"}`).
    *   **Payload (JSON):** Enter the custom claims (user ID, roles, etc.) you want to include in the token. The text area comes pre-filled with a sample payload.

3.  **Generate Token:**
    Click the **"Generate JWT"** button. The resulting encoded JWT token will appear in the "Generated JWT Token" box, and the status label will update with details about the generation and expiration.

## Security Notes (Production Best Practices)

*   **Keep your Secret Key _absolutely_ secret:** Never expose your secret key in client-side code or commit it to public repositories.
*   **Change Default Credentials:** If using this in a context where default credentials like `admin` are set, always change them to strong, unique values.
*   **Use Strong Algorithms:** For production environments, consider using asymmetric algorithms like `RS256` or `ES256`. These allow the private key to sign the token and the public key to verify it, which is beneficial when the token is verified by a different service than the one that generated it.
*   **Validate All Claims:** Any service consuming these JWTs should rigorously validate all claims, especially `exp` (expiration time), `nbf` (not before), `iat` (issued at), `iss` (issuer), and `sub` (subject).
*   **Leverage `jti` for Revocation:** The generated `jti` (JWT ID) is a unique identifier. In a production system, you can use this `jti` to implement token revocation (e.g., by adding it to a blacklist if a user logs out or a token is compromised before its natural expiration).
*   **Short Expiration Times:** Set a reasonably short expiration time (`exp`) to limit the window of opportunity for token misuse if it falls into the wrong hands.

## Script Details

The core logic is encapsulated within the `JWTGeneratorApp` class. Key aspects include:
*   **GUI Construction:** Uses `customtkinter` widgets for input fields, buttons, and display areas.
*   **Input Validation:** Ensures that the secret key is provided, expiration time is a valid positive integer, and JSON inputs for payload and header are well-formed.
*   **Claim Handling:** The `generate_jwt` method automatically adds standard claims (`iat`, `exp`, `nbf`, `iss`, `sub`, and `jti`) to the payload before encoding.
*   **JWT Encoding:** Utilizes the `PyJWT` library's `jwt.encode()` function to create the signed token.
*   **Status Updates:** Provides user feedback via a dedicated status label.
