import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './BottomNav.css';

function BottomNav({ active }) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const navItems = [
    { id: 'my_cards', icon: '📇', label: t('my_cards'), path: '/' },
    { id: 'card_collection', icon: '📚', label: t('card_collection'), path: '/collection' },
    { id: 'settings', icon: '⚙️', label: t('settings'), path: '/settings' }
  ];

  return (
    <nav className="bottom-nav">
      {navItems.map((item) => (
        <button
          key={item.id}
          className={`nav-item ${active === item.id ? 'active' : ''}`}
          onClick={() => navigate(item.path)}
        >
          <span className="nav-item-icon">{item.icon}</span>
          <span>{item.label}</span>
        </button>
      ))}
    </nav>
  );
}

export default BottomNav;
