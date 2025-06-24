# Email Helper

A web tool that helps you instantly polish and refine your emails using AI.  
See grammar and style feedback, and get real-time suggestions to make your message clearer and more professional.

---

## 🚀 Live Demo

[Try it live here!](https://email-helper-blue.vercel.app/)

### App Screenshot

![image](https://github.com/user-attachments/assets/d1e795e8-b7f4-46e5-8a24-b08ea5962b64)


---

## 🛠️ Features

- **Paste your draft email** and see line-by-line grammar, style, and tone analysis.
- **Instant AI-powered suggestions** to refine or rephrase each sentence.
- **Visual feedback:**
  - Correct sentences highlighted in green
  - Sentences that could be simplified highlighted in yellow, with suggested corrections and explanations
  - Sentences needing improvement highlighted in red, with suggested corrections and explanations
- **No login or sign-up required** — just paste, analyze, and improve.

---

## 🔧 Tech Stack

- **Frontend:** React + Vite + Axios  
- **Backend:** Flask
- **Deployment:** Vercel (frontend), Railway (backend)

---

## ⚡ Getting Started

1. **Clone & Install**
    ```bash
    git clone https://github.com/seungwoo900/email-helper.git
    cd email-helper
    npm install
    ```

2. **Run Locally**
    ```bash
    npm run dev
    ```
    Navigate to [http://localhost:5173](http://localhost:5173) to test the app.

---

## 🔌 Environment Variables

Set up your `.env.local` file in the root:

- VITE_API_BASE_URL=http://localhost:5000
- VITE_PERPLEXITY_API_KEY='YOUR_API_TOKEN_KEY'
