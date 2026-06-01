// src/main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Set default theme
document.documentElement.setAttribute('data-theme',
  localStorage.getItem('rubiks-theme') || 'dark'
);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
