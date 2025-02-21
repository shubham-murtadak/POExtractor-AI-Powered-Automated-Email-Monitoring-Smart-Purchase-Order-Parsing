import React, { useState } from "react";
import { TypeAnimation } from "react-type-animation";
import { motion } from "framer-motion";
import Lottie from "lottie-react";
import Particles from "react-tsparticles";
import aiAnimation from "../assets/ai_animation.json";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Link } from "react-router-dom";

const HomePage = () => {
  const [darkMode, setDarkMode] = useState(true);

  return (
    <div className={`${darkMode ? "bg-gray-900 text-white" : "bg-white text-gray-900"} transition-all`}>
      
      {/* 🔥 Background Particles */}
      <Particles
        options={{
          background: { color: darkMode ? "#000" : "#fff" },
          particles: {
            number: { value: 50 },
            shape: { type: "circle" },
            opacity: { value: 0.5 },
            size: { value: 3 },
            move: { speed: 1 },
          },
        }}
      />

      {/* 🚀 Navbar (Fix: Added z-10) */}
      <div className="relative z-10">
        <Navbar darkMode={darkMode} toggleDarkMode={() => setDarkMode(!darkMode)} />
      </div>

      <header className="flex flex-col items-center justify-center h-screen text-center px-6 relative">
        {/* ✅ Background Image */}
        <div
          className="absolute inset-0 bg-no-repeat bg-cover bg-center opacity-50"
          style={{ backgroundImage: "url('https://cdn.pixabay.com/photo/2021/11/04/06/24/ai-6767497_1280.jpg')" }}
        ></div>

        {/* ✅ Enhanced TypeAnimation */}
        <TypeAnimation
          sequence={[
            "🚀 AI-Powered PO Monitoring",
            1500,
            "🤖 Automate Purchase Order Extraction",
            1500,
            "📧 Smart Email & Attachment Handling",
            1500,
            "⚡ AI-Driven Data Insights",
            1500,
            "📂 Intelligent Document Parsing",
            1500,
            "🔍 Real-time Purchase Order Analysis",
            1500,
          ]}
          wrapper="h1"
          speed={50}
          preRenderFirstString={true}
          className="text-5xl font-bold z-10"
        />
        
        <p className="mt-4 text-lg z-10">
          Experience AI-powered automation for your purchase orders, invoices, and documents.
        </p>

        <Link to="/dashboard">
        <button className="mt-6 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-transform transform hover:scale-105 z-10">
          Get Started 🚀
        </button>
      </Link>
      </header>

      {/* 🤖 AI Lottie Animation (Moved Up for Balance) */}
      <section className="flex justify-center py-12">
        <Lottie animationData={aiAnimation} className="w-80 h-80" />
      </section>
{/* 🔄 Features Section */}
<section className="p-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
  {[
    { title: "📬 Email Monitoring", desc: "Seamless email tracking for POs" },
    { title: "📂 Attachment Handling", desc: "Extract PDFs, Excel, and more" },
    { title: "🔍 AI-Powered Parsing", desc: "LLMs extracting structured data" },
    { title: "⚡ Real-time Summarization", desc: "Instant AI-powered summaries" },
    { title: "📈 Intelligent Classification", desc: "Detect PO types accurately" },
    { title: "🧠 Error Handling & Retries", desc: "No failed extractions left behind" },
  ].map((feature, index) => (
    <motion.div
      key={index}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="relative bg-white/10 backdrop-blur-lg border border-white/20 
                hover:border-blue-500 hover:bg-blue-500/20 p-6 rounded-xl 
                transition-all transform hover:scale-105 shadow-md hover:shadow-blue-500/30"
    >
      <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
      <p className="text-gray-300 mt-2 group-hover:text-white transition-colors">
        {feature.desc}
      </p>
    </motion.div>
  ))}
</section>

{/* 🎬 Live PO Processing Demo */}
<section className="p-10 text-center">
  <h2 className="text-4xl font-bold text-white">📧 Live PO Processing Demo</h2>
  <div className="mt-6 p-6 bg-gray-900 border border-gray-700 rounded-lg text-left shadow-lg">
    <p className="text-gray-300">
      📧 New Email Received: "<span className="text-blue-400">Purchase Order #1023 Attached!</span>"
    </p>
    <p className="text-yellow-400">⏳ Processing...</p>
    <motion.p 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      transition={{ delay: 1.5 }}
      className="text-green-400 font-semibold"
    >
      ✅ Extracted: <span>PO# 1023, Item: Laptop, Qty: 5</span>
    </motion.p>
  </div>
</section>


      {/* 💬 Floating AI Chat Icon */}
     

      {/* 👣 Footer */}

      {/* 🚀 Navbar (Fix: Added z-10) */}
      <div className="relative z-10">
      <div className="fixed bottom-6 right-6">
        <button className="p-4 bg-blue-500 rounded-full shadow-lg hover:scale-110 transition">
          💬
        </button>
      </div>
      <Footer />
      </div>

    
    </div>
  );
};

export default HomePage;
