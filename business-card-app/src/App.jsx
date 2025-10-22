import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { authService } from './services/firebase';
import HomeScreen from './screens/HomeScreen';
import CreateCardScreen from './screens/CreateCardScreen';
import CardDetailScreen from './screens/CardDetailScreen';
import CardCollectionScreen from './screens/CardCollectionScreen';
import SettingsScreen from './screens/SettingsScreen';
import ViewCardScreen from './screens/ViewCardScreen';
import './App.css';

function App() {
  const { i18n } = useTranslation();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState('blue');

  useEffect(() => {
    // Initialize authentication
    const initAuth = async () => {
      try {
        const currentUser = authService.getCurrentUser();
        if (!currentUser) {
          const user = await authService.signInAnonymously();
          setUser(user);
        } else {
          setUser(currentUser);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
      } finally {
        setLoading(false);
      }
    };

    initAuth();

    // Load theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'blue';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Load language from localStorage
    const savedLanguage = localStorage.getItem('language') || 'ko';
    i18n.changeLanguage(savedLanguage);
  }, [i18n]);

  const changeTheme = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="app" data-theme={theme}>
        <Routes>
          <Route path="/" element={<HomeScreen user={user} theme={theme} />} />
          <Route path="/create" element={<CreateCardScreen user={user} theme={theme} />} />
          <Route path="/edit/:id" element={<CreateCardScreen user={user} theme={theme} />} />
          <Route path="/detail/:id" element={<CardDetailScreen user={user} theme={theme} />} />
          <Route path="/collection" element={<CardCollectionScreen user={user} theme={theme} />} />
          <Route path="/settings" element={<SettingsScreen user={user} theme={theme} onThemeChange={changeTheme} />} />
          <Route path="/card/:id" element={<ViewCardScreen theme={theme} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
