---

# 📧 POExtractor: 🤖 AI-Powered Automated Email Monitoring & 📝 Smart Purchase Order Parsing
🚀 *AI-powered tool to classify and process purchase orders effortlessly!*  
💼 **Built for B2B businesses to streamline purchase order management and optimize workflows.**

---

## 🌟 **Features**  
🛠️ **Our system comes packed with exciting functionalities:**

1. **📬 Automatic Email Monitoring and Classification**  
   - Leverages `imap_tools` for seamless email monitoring.  
   - Automatically identifies whether an email contains a **Purchase Order (PO)**.  
   - ⏱️ **Real-time PO classification** as emails arrive!

2. **📂 Attachment Handling**  
   - Downloads and processes various attachment formats:  
     - **PDFs** 📝  
     - **Excel/CSV** 📊  
     - **Images** 🖼️  
     - **Word Documents** 📄  
   - 📥 Supports multiple formats, ensuring no attachment is left behind!

3. **🔍 Intelligent PO Parsing**  
   - Powered by **Mixtral-8x7B-32768** OpenSource LLM for email classification.  
   - **LLAMA Parser** extracts key details from **PDF POs**, such as:  
     - Customer PO Number 📑  
     - Item Name, Quantity, Delivery Dates 📦  
     - Rate, Taxes, Payment Terms 💵  
   - **LangChain Unstructured Parser** for precise data extraction from **Excel/CSV POs**.  
   - 🧠 **AI-powered accuracy** for handling unstructured data with precision.

4. **🌐 User-Friendly Interface**  
   - Extracted data is displayed in an intuitive UI built using **FastAPI** (backend) and **React** (frontend).  
   - ✍️ Manual corrections for missing or inaccurate fields to ensure data accuracy.

5. **⚡ Retry and Error Handling**  
   - **Automatic retries** for failed extraction attempts.  
   - 🚨 Errors and missing fields are highlighted for easy resolution.

6. **📈 AI-Powered Summarization**  
   - Summarizes email bodies and attachments for a quick overview.  
   - ⚡ Fast, reliable summarization for enhanced productivity.

---

## 🚧 **Technical Stack**  

🔧 **What powers POExtractor?**  

- **Email Monitoring**: `imap_tools`  
- **Data Extraction**:  
  - **Mixtral-8x7B-32768** OpenSource LLM for email classification.  
  - **LLAMA Parser** for extracting details from **PDF POs**.  
  - **LangChain Unstructured Parser** for **Excel/CSV POs**.  
- **Backend**: **FastAPI** (Python-based)  
- **Frontend**: **React** (JavaScript-based UI)  
- **Database**: **SQLite** (for temporary data storage)

---

## 🚧 **Project Status**  
⚠️ *This project is a work in progress!*  
- **New features** and updates are continually being rolled out.  
- **Stay tuned** for improvements in parsing accuracy, UI enhancements, and new integrations. 🚀

---
---

## 🚀 **Future Plans & Updates**  
We have exciting plans for **POExtractor**, including:  
- **🤖Fine-Tuned LLaMA 3.2** to Enhanced Classification and **🔍Fine-Tuned LLAVA** for Image Data Extraction.
- **🌐 Real-time Document Link Support**: Support for document links (e.g., **Google Docs**, cloud links).  
- **💬 AI-Powered Feedback Loop**: Implementing feedback to continuously improve prediction accuracy.  
- **🏷️ Multi-category Classification**: For various PO types, **❌ spam**, and **📩 inquiries**.  
- **⚡ Faster and Smarter AI Models**: Continuous optimization for performance improvements.  
- **👥 Expansion for HR Professionals**: A future update will expand POExtractor to classify emails based on **💼 job openings** and perform similar data extraction for recruitment processes.
---

## 👨‍💻 **Built By**  
✨ **Shubham Murtadak**  *GenAI Engineer* 💻💡  
---
Here is a more polished and visually appealing version of your setup instructions:

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/shubham-murtadak/POExtractor-Smart-Purchase-Order-Parsing.git
cd POExtractor-Smart-Purchase-Order-Parsing
```

---

### 2. **Backend Setup (FastAPI)**

The **backend** of this project is built using **FastAPI**.

#### Step 1: Navigate to the Backend Folder

```bash
cd backend
```

#### Step 2: Create a Virtual Environment

Create a virtual environment to isolate the backend dependencies:

```bash
python3 -m venv venv
```

#### Step 3: Activate the Virtual Environment

- **On Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

#### Step 4: Install Backend Dependencies

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Step 5: Set Up Environment Variables

Create a `.env` file in the **backend** folder and add the following details:

```env
# Add your email and app password here
EMAIL="your-email@example.com"
PASSWORD="your-app-password"  # App password required for IMAP access (Video guide: https://youtu.be/MkLX85XU5rU?si=J8HoRukRP49Dk3xV)

# API Keys
GROQ_API_KEY="your-groq-api-key"  # Get it from https://console.groq.com/keys
LLMA_API_KEY="your-llma-api-key"  # Get it from https://docs.cloud.llamaindex.ai/llamaparse/getting_started/get_an_api_key

# Project Home Path
PROJECT_HOME_PATH="your-project-homepath"
```

Make sure to replace the placeholders with your actual values.

#### Step 6: Run the Backend

To start the FastAPI server, use:

```bash
uvicorn app:app --reload
```

The backend will be available at: `http://127.0.0.1:8000`.

---

### 3. **Frontend Setup (React)**

The **frontend** is built using **React**.

#### Step 1: Navigate to the Frontend Folder

```bash
cd frontend
```

#### Step 2: Install Frontend Dependencies

Install the required Node.js packages:

```bash
npm install
```

#### Step 3: Run the Frontend

Start the React development server:

```bash
npm start
```

The frontend will be available at: `http://localhost:3000`.

---

### 4. **Testing the Application**

Once both the backend and frontend are running, you should be able to:

- **Access the Backend** at `http://127.0.0.1:8000` (FastAPI).
- **Access the Frontend** at `http://localhost:3000` (React).

Ensure that the frontend is making correct API calls to the backend.

---

### 5. **Important Notes**

- **Environment Variables**: Make sure your `.env` files are properly configured with your email, app password, and API keys for Groq and Llama services.
- **Email and App Password**: Ensure your Gmail account and app password are valid (for monitoring the Gmail account).
  
  Refer to the [video guide](https://youtu.be/MkLX85XU5rU?si=J8HoRukRP49Dk3xV) for setting up the app password.

---

### 6. **Project Structure**

Here’s a general overview of the project folder structure:

         ```
         /POExtractor-Smart-Purchase-Order-Parsing
             /backend
                 /app.py
                 /requirements.txt
                 /.env
             /frontend
                 /src
                 /public
                 /package.json
                 /.env
             README.md
         ```

---
---

## 👩‍💻 **Contribute**  
Want to help make **POExtractor** even better? 🎉  
- **Fork the repo**  
- **Submit pull requests**  
- Open **issues** with ideas or suggestions!  

🚀 **Looking for a React Developer** to help build an even more **awesome UI**! If you’re passionate about frontend development and want to contribute to creating an amazing user experience, **I’d love to have you on board!** 🌟

---

### ✨ **Stay Connected**  
⭐ **Star this repo** if you’re excited!  
🙌 **Reach out** for ideas, suggestions, or collaborations. Let’s make this tool even better together!  

---

## 📸 **Screenshots**  

Here’s a preview of the **POExtractor** interface in action! 🔥  

![Frontend Screenshot](screenshots/uia.png)  
![Frontend Screenshot](screenshots/uib.png)  
![Frontend Screenshot](screenshots/uic.png)  
![Frontend Screenshot](screenshots/uid.png)  
![Frontend Screenshot](screenshots/uie.png)  

This screenshot shows the **React** frontend where the extracted data is displayed for easy review and correction. ✨

---

### 🌍 **Join the Journey**  
We’re just getting started. Join me in making **POExtractor** the ultimate tool for automatic **Purchase Order parsing**. ⭐  

Reach out with ideas, feedback, or if you’re interested in contributing! Let's build something amazing together. 🚀

---
