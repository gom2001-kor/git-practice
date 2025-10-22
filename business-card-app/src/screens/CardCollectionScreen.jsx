import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { firestoreService } from '../services/firebase';
import BusinessCardPreview from '../components/BusinessCardPreview';
import BottomNav from '../components/BottomNav';

function CardCollectionScreen({ user, theme }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadCollection();
  }, [user]);

  const loadCollection = async () => {
    try {
      if (user) {
        const collection = await firestoreService.getCardCollection(user.uid);
        setCards(collection);
      }
    } catch (error) {
      console.error('Error loading collection:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredCards = cards.filter(card =>
    card.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="screen">
      <header className="header">
        <div className="header-content">
          <h1 className="header-title">{t('card_collection')}</h1>
        </div>
      </header>

      <main className="container">
        <div style={{ padding: '1rem' }}>
          <input
            type="text"
            className="form-input"
            placeholder={t('search')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
          </div>
        ) : filteredCards.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📚</div>
            <p className="empty-state-text">{t('card_collection')}</p>
          </div>
        ) : (
          <div className="cards-grid">
            {filteredCards.map((card) => (
              <BusinessCardPreview
                key={card.id}
                card={card}
                theme={theme}
                onClick={() => navigate(`/card/${card.id}`)}
              />
            ))}
          </div>
        )}
      </main>

      <BottomNav active="card_collection" />
    </div>
  );
}

export default CardCollectionScreen;
