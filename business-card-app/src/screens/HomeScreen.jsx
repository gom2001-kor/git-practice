import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { firestoreService } from '../services/firebase';
import BusinessCardPreview from '../components/BusinessCardPreview';
import BottomNav from '../components/BottomNav';
import './HomeScreen.css';

function HomeScreen({ user, theme }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCards();
  }, [user]);

  const loadCards = async () => {
    try {
      if (user) {
        const userCards = await firestoreService.getUserCards(user.uid);
        setCards(userCards);
      }
    } catch (error) {
      console.error('Error loading cards:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCard = () => {
    navigate('/create');
  };

  const handleCardClick = (cardId) => {
    navigate(`/detail/${cardId}`);
  };

  return (
    <div className="screen home-screen">
      <header className="header">
        <div className="header-content">
          <h1 className="header-title">{t('my_cards')}</h1>
          <div className="header-actions">
            <button className="icon-btn" onClick={() => navigate('/settings')}>
              ⚙️
            </button>
          </div>
        </div>
      </header>

      <main className="container">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
          </div>
        ) : cards.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📇</div>
            <p className="empty-state-text">{t('create_card')}</p>
            <button className="btn btn-primary" onClick={handleCreateCard}>
              {t('create_card')}
            </button>
          </div>
        ) : (
          <div className="cards-grid">
            {cards.map((card) => (
              <BusinessCardPreview
                key={card.id}
                card={card}
                theme={theme}
                onClick={() => handleCardClick(card.id)}
              />
            ))}
          </div>
        )}
      </main>

      <button className="fab" onClick={handleCreateCard}>
        +
      </button>

      <BottomNav active="my_cards" />
    </div>
  );
}

export default HomeScreen;
