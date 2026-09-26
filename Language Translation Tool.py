import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.parse
import urllib.request


def fetch_translation_data(text, source_code="auto", target_code="hi"):
    """Multi-engine translation fetcher:

    1. Google Android Client Gateway (Resistant to IP limits)
    2. Google Web Client Gateway
    3. MyMemory Open API
    """
    # Engine 1: Android Client API Gateway
    try:
        sl = "auto" if source_code == "auto" else source_code
        query_encoded = urllib.parse.quote(text)
        url = (
            f"https://translate.google.com/translate_a/single?"
            f"client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=en&ie=UTF-8&oe=UTF-8"
            f"&sl={sl}&tl={target_code}&q={query_encoded}"
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "GoogleTranslate/6.28.0.05.421483610 (Linux; U; Android"
                    " 12; Pixel 6)"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
            sentences = data.get("sentences", [])
            output = "".join(
                [s.get("trans", "") for s in sentences if "trans" in s]
            )
            if output.strip():
                return output
    except Exception:
        pass

    # Engine 2: Google Direct Web Endpoint
    try:
        query_encoded = urllib.parse.quote(text)
        url = (
            f"https://translate.googleapis.com/translate_a/single?"
            f"client=gtx&sl={source_code}&tl={target_code}&dt=t&q={query_encoded}"
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    " AppleWebKit/537.36 (KHTML, like Gecko)"
                    " Chrome/124.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
            output = "".join([chunk[0] for chunk in data[0] if chunk[0]])
            if output.strip():
                return output
    except Exception:
        pass

    # Engine 3: MyMemory Translation API Gateway
    try:
        sl = "en" if source_code == "auto" else source_code
        query_encoded = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={query_encoded}&langpair={sl}|{target_code}"
        req = urllib.request.Request(
            url, headers={"User-Agent": "TranslaProDesktop/2.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["responseData"]["translatedText"]
    except Exception as err:
        raise Exception(
            "Translation services unreachable. Check your internet connection."
        )


class TranslaProApp:

    def __init__(self, root):
        self.root = root
        self.root.title("TRANSLA PRO - Language Translation Tool")
        self.root.geometry("690x780")
        self.root.resizable(False, False)

        # Light Blue Eye-Catching Color Theme
        self.bg_main = "#e8f1fa"
        self.header_bg = "#d3e5f7"
        self.title_color = "#0369a1"
        self.subtitle_color = "#0284c7"
        self.border_blue = "#bae6fd"

        self.selector_card = "#f0f8ff"
        self.input_card = "#ffffff"
        self.output_card = "#f8faff"

        self.input_tag_color = "#2563eb"
        self.output_tag_color = "#059669"

        # Explicit pure black color for inputs and outputs
        self.text_content_color = "#000000"

        # Action Buttons
        self.btn_blue = "#0284c7"
        self.btn_blue_hover = "#0369a1"
        self.btn_copy_bg = "#ecfdf5"
        self.btn_copy_fg = "#047857"

        self.root.configure(bg=self.bg_main)

        self.languages = {
            "Auto Detect": "auto",
            "English": "en",
            "Hindi": "hi",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Russian": "ru",
            "Arabic": "ar",
            "Bengali": "bn",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Punjabi": "pa",
            "Tamil": "ta",
            "Telugu": "te",
            "Urdu": "ur",
            "Japanese": "ja",
            "Chinese (Simplified)": "zh-CN",
        }

        self._build_ui()

    def _build_ui(self):
        # 1. Header Frame
        header_frame = tk.Frame(
            self.root,
            bg=self.header_bg,
            highlightbackground=self.border_blue,
            highlightthickness=1,
            pady=12,
        )
        header_frame.pack(fill=tk.X, padx=25, pady=(20, 12))

        lbl_title = tk.Label(
            header_frame,
            text="TRANSLA PRO",
            font=("Segoe UI", 25, "bold"),
            bg=self.header_bg,
            fg=self.title_color,
        )
        lbl_title.pack()

        lbl_sub = tk.Label(
            header_frame,
            text="Language Translation Tool",
            font=("Segoe UI", 11, "bold"),
            bg=self.header_bg,
            fg=self.subtitle_color,
        )
        lbl_sub.pack(pady=(2, 0))

        # 2. Main Content Workspace
        main_content = tk.Frame(self.root, bg=self.bg_main)
        main_content.pack(fill=tk.BOTH, expand=True, padx=25)

        # 3. Language Selector Card
        lang_card = tk.Frame(
            main_content,
            bg=self.selector_card,
            highlightbackground=self.border_blue,
            highlightthickness=1,
            padx=16,
            pady=14,
        )
        lang_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            lang_card,
            text="SOURCE LANGUAGE",
            font=("Segoe UI", 9, "bold"),
            bg=self.selector_card,
            fg="#0369a1",
        ).grid(row=0, column=0, sticky="w", padx=(5, 5))

        self.cb_source = ttk.Combobox(
            lang_card,
            values=list(self.languages.keys()),
            state="readonly",
            width=16,
            font=("Segoe UI", 10),
        )
        self.cb_source.set("Auto Detect")
        self.cb_source.grid(row=1, column=0, padx=(5, 10), pady=(3, 0))

        btn_swap = tk.Button(
            lang_card,
            text="⇄",
            font=("Segoe UI", 13, "bold"),
            bg="#e0f2fe",
            fg=self.title_color,
            activebackground=self.border_blue,
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=1,
            command=self.swap_languages,
        )
        btn_swap.grid(row=1, column=1, padx=6, pady=(3, 0))

        tk.Label(
            lang_card,
            text="TARGET LANGUAGE",
            font=("Segoe UI", 9, "bold"),
            bg=self.selector_card,
            fg="#0369a1",
        ).grid(row=0, column=2, sticky="w", padx=(10, 5))

        self.cb_target = ttk.Combobox(
            lang_card,
            values=[k for k in self.languages.keys() if k != "Auto Detect"],
            state="readonly",
            width=16,
            font=("Segoe UI", 10),
        )
        self.cb_target.set("Hindi")
        self.cb_target.grid(row=1, column=2, padx=(10, 5), pady=(3, 0))

        # 4. Input Text Card (Text color set to pure black)
        in_frame = tk.Frame(
            main_content,
            bg=self.input_card,
            highlightbackground=self.border_blue,
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        in_frame.pack(fill=tk.X, pady=(0, 10))

        in_header = tk.Frame(in_frame, bg=self.input_card)
        in_header.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            in_header,
            text="INPUT TEXT",
            font=("Segoe UI", 9, "bold"),
            bg="#eff6ff",
            fg=self.input_tag_color,
            padx=8,
            pady=2,
        ).pack(side=tk.LEFT)

        self.lbl_char_count = tk.Label(
            in_header,
            text="0 characters",
            font=("Segoe UI", 8),
            bg=self.input_card,
            fg="#64748b",
        )
        self.lbl_char_count.pack(side=tk.RIGHT)

        self.txt_source = tk.Text(
            in_frame,
            height=5,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bg="#ffffff",
            fg=self.text_content_color,
            insertbackground="#000000",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            padx=10,
            pady=8,
        )
        self.txt_source.pack(fill=tk.X)
        self.txt_source.bind("<KeyRelease>", self._update_char_count)

        # 5. Buttons Row
        action_row = tk.Frame(main_content, bg=self.bg_main)
        action_row.pack(fill=tk.X, pady=(0, 10))

        self.btn_translate = tk.Button(
            action_row,
            text="⚡ Translate Now",
            font=("Segoe UI", 10, "bold"),
            bg=self.btn_blue,
            fg="white",
            activebackground=self.btn_blue_hover,
            activeforeground="white",
            relief=tk.FLAT,
            padx=22,
            pady=6,
            cursor="hand2",
            command=self.start_translate_worker,
        )
        self.btn_translate.pack(side=tk.LEFT)

        btn_clear = tk.Button(
            action_row,
            text="Clear",
            font=("Segoe UI", 10),
            bg="#e2e8f0",
            fg="#0f172a",
            activebackground="#cbd5e1",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.clear_all,
        )
        btn_clear.pack(side=tk.LEFT, padx=(10, 0))

        self.lbl_status = tk.Label(
            action_row,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg=self.bg_main,
            fg="#0284c7",
        )
        self.lbl_status.pack(side=tk.LEFT, padx=(15, 0))

        # 6. Output Text Card (Output text set to pure black)
        out_frame = tk.Frame(
            main_content,
            bg=self.output_card,
            highlightbackground="#a7f3d0",
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        out_frame.pack(fill=tk.X, pady=(0, 6))

        out_header = tk.Frame(out_frame, bg=self.output_card)
        out_header.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            out_header,
            text="TRANSLATED OUTPUT",
            font=("Segoe UI", 9, "bold"),
            bg="#ecfdf5",
            fg=self.output_tag_color,
            padx=8,
            pady=2,
        ).pack(side=tk.LEFT)

        self.btn_copy = tk.Button(
            out_header,
            text="📋 Copy Output",
            font=("Segoe UI", 9, "bold"),
            bg=self.btn_copy_bg,
            fg=self.btn_copy_fg,
            relief=tk.FLAT,
            highlightbackground="#6ee7b7",
            highlightthickness=1,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.copy_output_text,
        )
        self.btn_copy.pack(side=tk.RIGHT)

        self.txt_output = tk.Text(
            out_frame,
            height=5,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bg="#ffffff",
            fg=self.text_content_color,
            insertbackground="#000000",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            padx=10,
            pady=8,
        )
        self.txt_output.pack(fill=tk.X)

        # 7. Signature Branding Footer
        footer_frame = tk.Frame(self.root, bg=self.bg_main)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 16))

        tk.Label(
            footer_frame,
            text="TRANSLA PRO  •  CREATED WITH ❤️ BY AYUSH ARYAN",
            font=("Segoe UI", 9, "bold"),
            bg=self.bg_main,
            fg="#0369a1",
        ).pack()

    def _update_char_count(self, event=None):
        chars = len(self.txt_source.get("1.0", tk.END).strip())
        self.lbl_char_count.config(text=f"{chars} characters")

    def swap_languages(self):
        curr_source = self.cb_source.get()
        curr_target = self.cb_target.get()
        if curr_source == "Auto Detect":
            return
        self.cb_source.set(curr_target)
        self.cb_target.set(curr_source)

    def start_translate_worker(self):
        text = self.txt_source.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning(
                "Input Empty", "Please type or paste text to translate."
            )
            return

        self.btn_translate.config(state=tk.DISABLED, text="Translating...")
        self.lbl_status.config(text="Processing...", fg="#0284c7")

        threading.Thread(
            target=self._run_network_translation, args=(text,), daemon=True
        ).start()

    def _run_network_translation(self, text):
        src_code = self.languages.get(self.cb_source.get(), "auto")
        tgt_code = self.languages.get(self.cb_target.get(), "hi")

        try:
            result = fetch_translation_data(
                text, source_code=src_code, target_code=tgt_code
            )
            self.root.after(0, self._show_result, result)
        except Exception as e:
            self.root.after(0, self._handle_error, str(e))

    def _show_result(self, result):
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, result)
        self.lbl_status.config(text="Completed!", fg="#059669")
        self.btn_translate.config(state=tk.NORMAL, text="⚡ Translate Now")

    def _handle_error(self, err_info):
        self.btn_translate.config(state=tk.NORMAL, text="⚡ Translate Now")
        self.lbl_status.config(text="Failed!", fg="#dc2626")
        messagebox.showerror(
            "Translation Error",
            f"Unable to complete translation.\n\nDetails: {err_info}",
        )

    def copy_output_text(self):
        content = self.txt_output.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Empty", "No translated text available to copy.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)

        self.btn_copy.config(text="✓ Copied!", bg="#d1fae5")
        self.lbl_status.config(text="Copied to clipboard!", fg="#059669")
        self.root.after(
            1500,
            lambda: self.btn_copy.config(
                text="📋 Copy Output", bg=self.btn_copy_bg
            ),
        )

    def clear_all(self):
        self.txt_source.delete("1.0", tk.END)
        self.txt_output.delete("1.0", tk.END)
        self.lbl_status.config(text="")
        self._update_char_count()


if __name__ == "__main__":
    app_window = tk.Tk()
    app = TranslaProApp(app_window)
    app_window.mainloop()