import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import RequirementForm from './components/RequirementForm';
import UserStoryForm from './components/UserStoryForm';
import TestCaseForm from './components/TestCaseForm';
import DesignForm from './components/DesignForm';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>AI SDLC Orchestrator</h1>
          <nav>
            <ul>
              <li><a href="/">Dashboard</a></li>
              <li><a href="/requirements">Requirements</a></li>
              <li><a href="/stories">User Stories</a></li>
              <li><a href="/test-cases">Test Cases</a></li>
              <li><a href="/design">Design</a></li>
            </ul>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/requirements" element={<RequirementForm />} />
            <Route path="/stories" element={<UserStoryForm />} />
            <Route path="/test-cases" element={<TestCaseForm />} />
            <Route path="/design" element={<DesignForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;