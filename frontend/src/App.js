import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI SDLC Orchestrator</h1>
        <p>Welcome to the AI-powered Software Development Lifecycle platform.</p>
        <nav>
          <ul>
            <li><a href="#">Requirements</a></li>
            <li><a href="#">User Stories</a></li>
            <li><a href="#">Test Cases</a></li>
            <li><a href="#">Analytics</a></li>
          </ul>
        </nav>
      </header>
      <main>
        <section className="hero">
          <h2>Transform Your Development Process</h2>
          <p>Leverage AI to streamline requirements gathering, user story creation, estimation, and quality assurance.</p>
          <button className="cta-button">Get Started</button>
        </section>
      </main>
    </div>
  );
}

export default App;