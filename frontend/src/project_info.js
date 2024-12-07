// src/ProjectInfo.js

import React, { useState, useEffect } from "react";
import axios from "axios";

const ProjectInfo = () => {
  const [projectInfo, setProjectInfo] = useState(null);

  useEffect(() => {
    // Fetch data from FastAPI backend
    axios
      .get("http://localhost:8000/api/project-info")
      .then((response) => {
        setProjectInfo(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the project info!", error);
      });
  }, []);

  if (!projectInfo) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>{projectInfo.title}</h1>
      <p>{projectInfo.description}</p>
      <h3>Features:</h3>
      <ul>
        {projectInfo.features.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>
    </div>
  );
};

export default ProjectInfo;
