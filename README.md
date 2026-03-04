# AI Finance Analyzer

AI Finance Analyzer adalah aplikasi berbasis Streamlit yang dapat menganalisis laporan keuangan (PDF, Excel, atau teks) menggunakan AI untuk memberikan insight otomatis dan ringkasan analisis.

# Features

- Upload file laporan keuangan (PDF, Excel, TXT)
- Analisis otomatis menggunakan AI
- Ringkasan keuangan
- Insight performa bisnis
- Tampilan interaktif berbasis Streamlit

---

# Tech Stack

- Python
- Streamlit
- OpenAI API
- Pandas
- PDF & Excel Processing

---

# Project Structure

ai-finance-analyzer/
│
├── app.py
├── requirements.txt
├── .streamlit/
├── utils/
│ ├── pdf_handler.py
│ ├── excel_handler.py
│ └── text_handler.py
└── assets/

# Installation

1. Clone repository


git clone https://github.com/JundiR02/Ai-finance-analyzer.git


2. Masuk ke folder project


cd Ai-finance-analyzer


3. Install dependencies


pip install -r requirements.txt


4. Buat file `.env`


OPENAI_API_KEY=your_api_key_here


5. Jalankan aplikasi


streamlit run app.py


---

# Environment Variables

Aplikasi membutuhkan:


OPENAI_API_KEY


Pastikan file `.env` tidak di-upload ke GitHub.

---

# Future Improvements

- Dashboard visualisasi rasio keuangan
- Support multi-model AI
- Export hasil analisis ke PDF
- Deploy ke cloud

---

# Author

**Jundi Robbani**  
Informatics Graduate | Aspiring AI & Backend Developer  
