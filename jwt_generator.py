import customtkinter as ctk
import jwt
import json
import time
from datetime import datetime, timedelta, timezone
import uuid

class JWTGeneratorApp(ctk.CTk):
    """
    A production-ready JWT Generator application with a modern GUI using CustomTkinter.
    """
    def __init__(self):
        super().__init__()

        # --- Configuration ---
        self.title("Production-Ready JWT Generator")
        self.geometry("1000x700")
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"

        # --- Grid Layout Configuration ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # --- Header Frame ---
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_label = ctk.CTkLabel(self.header_frame, text="JWT Generation Parameters", font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # --- Input Frame (Left) ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=0)
        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_rowconfigure(5, weight=1) # Payload Textbox

        # Secret Key
        self.secret_label = ctk.CTkLabel(self.input_frame, text="Secret Key:", anchor="w")
        self.secret_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.secret_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter your secret key")
        self.secret_entry.grid(row=0, column=1, padx=(0, 20), pady=(20, 5), sticky="ew")

        # Algorithm
        self.algorithm_label = ctk.CTkLabel(self.input_frame, text="Algorithm:", anchor="w")
        self.algorithm_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.algorithm_var = ctk.StringVar(value="HS256")
        self.algorithm_optionmenu = ctk.CTkOptionMenu(self.input_frame, values=["HS256", "HS384", "HS512", "RS256", "ES256"], variable=self.algorithm_var)
        self.algorithm_optionmenu.grid(row=1, column=1, padx=(0, 20), pady=5, sticky="ew")

        # Expiration Time (Minutes)
        self.expiry_label = ctk.CTkLabel(self.input_frame, text="Expiry (Minutes):", anchor="w")
        self.expiry_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.expiry_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g., 60 (for 1 hour)")
        self.expiry_entry.insert(0, "60")
        self.expiry_entry.grid(row=2, column=1, padx=(0, 20), pady=5, sticky="ew")

        # Custom Header (Optional)
        self.header_label = ctk.CTkLabel(self.input_frame, text="Custom Header (JSON):", anchor="w")
        self.header_label.grid(row=3, column=0, padx=20, pady=5, sticky="nw")
        self.header_textbox = ctk.CTkTextbox(self.input_frame, height=50)
        self.header_textbox.grid(row=3, column=1, padx=(0, 20), pady=5, sticky="ew")
        self.header_textbox.insert("0.0", '{"typ": "JWT"}') # Default header

        # Payload
        self.payload_label = ctk.CTkLabel(self.input_frame, text="Payload (JSON):", anchor="w")
        self.payload_label.grid(row=4, column=0, padx=20, pady=5, sticky="nw")
        self.payload_textbox = ctk.CTkTextbox(self.input_frame, height=200)
        self.payload_textbox.grid(row=5, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="nsew")
        self.payload_textbox.insert("0.0", '{\n  "user_id": 123,\n  "username": "testuser",\n  "roles": ["admin", "user"]\n}')

        # Generate Button
        self.generate_button = ctk.CTkButton(self.input_frame, text="Generate JWT", command=self.generate_jwt)
        self.generate_button.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        # --- Output Frame (Right) ---
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Generated JWT Token", font=ctk.CTkFont(size=16, weight="bold"))
        self.output_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.jwt_textbox = ctk.CTkTextbox(self.output_frame, height=200, wrap="word")
        self.jwt_textbox.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="nsew")

        self.status_label = ctk.CTkLabel(self.output_frame, text="Status: Ready", text_color="green")
        self.status_label.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

    def generate_jwt(self):
        """
        Handles the JWT generation logic based on user input.
        """
        self.status_label.configure(text="Status: Generating...", text_color="orange")
        self.update_idletasks()

        secret = self.secret_entry.get()
        algorithm = self.algorithm_var.get()
        expiry_minutes_str = self.expiry_entry.get()
        payload_json_str = self.payload_textbox.get("1.0", "end-1c")
        header_json_str = self.header_textbox.get("1.0", "end-1c")

        if not secret:
            self.update_status("Error: Secret Key is required.", "red")
            return

        try:
            expiry_minutes = int(expiry_minutes_str)
            if expiry_minutes <= 0:
                raise ValueError("Expiry must be a positive integer.")
        except ValueError as e:
            self.update_status(f"Error: Invalid Expiry Minutes. {e}", "red")
            return

        try:
            payload = json.loads(payload_json_str)
        except json.JSONDecodeError:
            self.update_status("Error: Invalid Payload JSON format.", "red")
            return

        try:
            header = json.loads(header_json_str)
        except json.JSONDecodeError:
            self.update_status("Error: Invalid Custom Header JSON format.", "red")
            return

        # --- JWT Claims Handling (Production Ready) ---
        # 1. Add 'iat' (Issued At) claim
        now = datetime.now(timezone.utc)
        payload['iat'] = int(now.timestamp())

        # 2. Add 'exp' (Expiration Time) claim
        expiry_time = now + timedelta(minutes=expiry_minutes)
        payload['exp'] = int(expiry_time.timestamp())

        # 3. Add 'nbf' (Not Before) claim (optional, but good practice)
        # We'll set it to a few seconds before 'iat' to account for clock skew
        payload['nbf'] = int((now - timedelta(seconds=5)).timestamp())

        # 4. Add 'jti' (JWT ID) claim for token revocation and tracking
        payload['jti'] = str(uuid.uuid4())

        # 5. Add 'iss' (Issuer) and 'sub' (Subject) claims if not present
        if 'iss' not in payload:
            payload['iss'] = "ManusJWTGenerator"
        if 'sub' not in payload:
            # Use a combination of user_id or username if available, otherwise a generic subject
            payload['sub'] = payload.get('username', payload.get('user_id', 'generic_subject'))

        # --- Encoding ---
        try:
            encoded_jwt = jwt.encode(
                payload,
                secret,
                algorithm=algorithm,
                headers=header
            )
            self.jwt_textbox.delete("1.0", "end")
            self.jwt_textbox.insert("1.0", encoded_jwt)
            self.update_status(f"Status: JWT generated successfully ({algorithm}). Expires: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')} UTC", "green")

        except Exception as e:
            self.update_status(f"JWT Encoding Error: {e}", "red")

    def update_status(self, message, color):
        """
        Updates the status label with a message and color.
        """
        self.status_label.configure(text=message, text_color=color)

if __name__ == "__main__":
    app = JWTGeneratorApp()
    app.mainloop()
