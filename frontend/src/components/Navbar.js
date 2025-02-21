import React from "react";
import { Link } from "react-router-dom";

const Navbar = ({ darkMode, toggleDarkMode }) => {
  return (
    <nav className={`flex items-center p-5 transition-all ${darkMode ? "bg-gray-900 text-white" : "bg-white text-gray-900 shadow-lg"}`}>
      {/* 🚀 Logo on the Left */}
      <Link to="/" className="text-3xl font-bold">🚀 POExtractor</Link>
      
      {/* 📌 Shifted Links to Right */}
      <div className="ml-auto space-x-6">
        <Link to="/" className="hover:text-blue-400 transition">Home</Link>
        <Link to="/about" className="hover:text-blue-400 transition">About</Link>
        <Link to="/contact" className="hover:text-blue-400 transition">Contact</Link>
      </div>

      {/* 🌙 Dark Mode Toggle */}
      <button onClick={toggleDarkMode} className="ml-6 p-2 bg-gray-700 hover:bg-gray-600 text-white rounded-md transition">
        {darkMode ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>
    </nav>
  );
};

export default Navbar;
