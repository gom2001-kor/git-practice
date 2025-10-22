import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { authService } from '../services/firebase';
import { showToast } from '../utils/helpers';
import BottomNav from '../components/BottomNav';
import './SettingsScreen.css';

function SettingsScreen({ user, theme, onThemeChange }) {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [linking, setLinking] = useState(false);

  const handleLinkGoogle = async () => {
    setLinking(true);
    try {
      await authService.linkWithGoogle();
      showToast('Google account linked successfully');
    } catch (error) {
      console.error('Error linking Google account:', error);
      showToast(t('error'));
    } finally {
      setLinking(false);
    }
  };

  const handleThemeChange = (newTheme) => {
    onThemeChange(newTheme);
    showToast(`${newTheme === 'blue' ? t('blue_theme') : t('pink_theme')} ${t('done')}`);
  };

  const handleLanguageChange = (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
    showToast('Language changed');
  };

  return (
    <div className="screen settings-screen">
      <header className="header">
        <div className="header-content">
          <h1 className="header-title">{t('settings')}</h1>
        </div>
      </header>

      <main className="container">
        <div className="settings-section">
          <h2 className="settings-section-title">{t('account')}</h2>
          <div className="card">
            <div className="settings-item">
              <span>{authService.isAnonymous() ? t('anonymous_user') : t('linked_account')}</span>
            </div>
            {authService.isAnonymous() && (
              <button
                className="btn btn-primary"
                onClick={handleLinkGoogle}
                disabled={linking}
              >
                {linking ? '⏳' : t('link_google')}
              </button>
            )}
          </div>
        </div>

        <div className="settings-section">
          <h2 className="settings-section-title">{t('select_theme')}</h2>
          <div className="card">
            <div className="theme-options">
              <button
                className={`theme-option ${theme === 'blue' ? 'active' : ''}`}
                onClick={() => handleThemeChange('blue')}
              >
                <div className="theme-preview blue-theme-preview"></div>
                <span>{t('blue_theme')}</span>
              </button>
              <button
                className={`theme-option ${theme === 'pink' ? 'active' : ''}`}
                onClick={() => handleThemeChange('pink')}
              >
                <div className="theme-preview pink-theme-preview"></div>
                <span>{t('pink_theme')}</span>
              </button>
            </div>
          </div>
        </div>

        <div className="settings-section">
          <h2 className="settings-section-title">Language</h2>
          <div className="card">
            <select
              className="form-select"
              value={i18n.language}
              onChange={(e) => handleLanguageChange(e.target.value)}
            >
              <option value="ko">한국어</option>
              <option value="en">English</option>
              <option value="zh">中文</option>
              <option value="ja">日本語</option>
            </select>
          </div>
        </div>
      </main>

      <BottomNav active="settings" />
    </div>
  );
}

export default SettingsScreen;
