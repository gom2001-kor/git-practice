/**
 * App Main Component
 */
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './components/Home';
import { Diagnosis } from './components/Diagnosis';
import { Watchlist } from './components/Watchlist';
import { DemoModeBanner } from './components/DemoModeBanner';

function App() {
  return (
    <BrowserRouter>
      <DemoModeBanner />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/diagnosis/:ticker" element={<Diagnosis />} />
        <Route path="/watchlist" element={<Watchlist />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
