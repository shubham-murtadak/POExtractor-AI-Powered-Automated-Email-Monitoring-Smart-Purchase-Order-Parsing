import React, { useEffect, useState } from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import "./App.css";

const App = () => {
  const [projectInfo, setProjectInfo] = useState({
    title: "",
    description: "",
    features: [],
  });

  // Fetch project info from the FastAPI backend
  useEffect(() => {
    const fetchProjectInfo = async () => {
      const response = await fetch("http://localhost:8000/api/project-info");
      const data = await response.json();
      setProjectInfo(data);
    };
    fetchProjectInfo();
  }, []);

  return (
    <div className="App">
      <div className="hero-section">
        <h1>{projectInfo.title}</h1>
        <p className="lead">{projectInfo.description}</p>

        {/* Features section */}
        <h3>Features</h3>
        <ul className="features-list">
          {projectInfo.features.map((feature, index) => (
            <li key={index}>
              <strong>✔</strong> {feature}
            </li>
          ))}
        </ul>

        <Button variant="primary" size="lg">
          Get Started
        </Button>
      </div>
    </div>
  );
};

export default App;
