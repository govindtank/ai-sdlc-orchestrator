import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import App from './App';
import Login from './pages/Login';
import Register from './pages/Register';
import Requirements from './pages/Requirements';
import UserStories from './pages/UserStories';
import Estimates from './pages/Estimates';
import TestCases from './pages/TestCases';
import DesignSuggestions from './pages/DesignSuggestions';
import ResourceGaps from './pages/ResourceGaps';
import Analytics from './pages/Analytics';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<App />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
