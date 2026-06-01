// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useTheme } from './hooks/useTheme';
import { useCubeState } from './hooks/useCubeState';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import LoadingPage from './pages/LoadingPage';
import InputPage from './pages/InputPage';
import SolutionPage from './pages/SolutionPage';
import PatternsPage from './pages/PatternsPage';
import HistoryPage from './pages/HistoryPage';

export default function App() {
  const { theme, toggleTheme } = useTheme();
  const cube = useCubeState(3);

  return (
    <BrowserRouter>
      <Navbar theme={theme} toggleTheme={toggleTheme} />
      <Routes>
        <Route path="/" element={
          <LandingPage size={cube.size} onSizeChange={cube.setSize} />
        } />
        <Route path="/input" element={
          <InputPage cube={cube} />
        } />
        <Route path="/loading" element={
          <LoadingPage />
        } />
        <Route path="/solution" element={
          <SolutionPage cube={cube} />
        } />
        <Route path="/patterns" element={
          <PatternsPage />
        } />
        <Route path="/history" element={
          <HistoryPage />
        } />
      </Routes>
    </BrowserRouter>
  );
}
