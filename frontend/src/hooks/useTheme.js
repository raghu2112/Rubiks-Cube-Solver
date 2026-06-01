// src/hooks/useTheme.js
import { useState, useEffect, useCallback } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('rubiks-theme');
    return saved || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('rubiks-theme', theme);
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  }, []);

  return { theme, toggleTheme, isDark: theme === 'dark' };
}
