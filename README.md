# 🖋️ H Type - Typing Simulator

A modern typing simulator with advanced features like H+ Ultra Type, error simulation, and customizable delays. Built using **Python**, **CustomTkinter**, **Tkinter**, **PyAutoGUI**, and optionally **python-docx** for `.docx` support.

---

## 🌟 Features

- **Custom Typing Simulation**
  - Simulates human-like typing with letter and word delays.
  - Option to enable **H+ Ultra Type** (introduces errors for realistic typing).
- **Load Text or Files**
  - Paste text directly or load `.txt` / `.docx` files (requires `python-docx`).
- **Customizable Delays**
  - Configure **min/max letter** and **min/max word** delays.
- **Start & Stop Controls**
  - Start typing with 5-second window to focus target window.
  - Stop typing anytime safely.
- **Lightweight GUI**
  - Built with **CustomTkinter** for a modern dark/light themed interface.

---

## 🛠️ Tech Stack

- **Python 3.x**
- **CustomTkinter** – Modern GUI framework for Tkinter.
- **Tkinter** – GUI components & message boxes.
- **PyAutoGUI** – Automates keyboard typing.
- **python-docx** *(optional)* – Load `.docx` files.

---

## ⚡ Installation

Install required libraries using `pip`:

```bash
pip install customtkinter pyautogui python-docx
```

> `python-docx` is optional; without it, `.docx` files cannot be loaded.

---

## 🖥️ Usage

1. Run the script:

```bash
python htype.py
```

2. Paste your text into the **text area** or click **Load File**.  
3. Enable **H+ Type** for ultra-realistic typing errors (optional).  
4. Adjust **letter** and **word delays** as desired.  
5. Click **Start Typing**, then focus the target window within 5 seconds.  
6. Click **Stop Typing** anytime to interrupt.

---

## 📂 File Structure

```
H-Type/
│
├── htype.py            # Main script
├── README.md           # This file
└── requirements.txt    # list dependencies
 
```

---

## ⚙️ Customization

- Adjust `error_probability` in the script to control likelihood of typos.  
- Change default delays (`min_letter_delay`, `max_letter_delay`, etc.) for faster or slower typing.  
- GUI appearance: Dark / Light themes via `ctk.set_appearance_mode()`.

---

## 💡 Notes

- Make sure the target window is focused before typing starts.  
- Some applications may block `pyautogui` from typing (e.g., elevated permissions required).  
- `.docx` support requires `python-docx`; without it, only `.txt` files work.

---

## 🤝 Contributing

Contributions welcome! You can:

- Improve typing algorithms  
- Add new features (e.g., punctuation patterns, more realistic errors)  
- Enhance GUI design  
- Add multi-language support

---

## 📬 Contact

- GitHub: [titan7k-zc](https://github.com/titan7k-zc)  
- Email: yourname@example.com

---

Made with ❤️ using Python & CustomTkinter
