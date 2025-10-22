import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { firestoreService } from '../services/firebase';
import { QRCodeSVG } from 'qrcode.react';
import {
  copyToClipboard,
  makePhoneCall,
  openEmailClient,
  openWebsite,
  openMap,
  shareCard,
  showToast,
  getQRCodeURL
} from '../utils/helpers';
import './CardDetailScreen.css';

function CardDetailScreen({ user, theme }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { id } = useParams();
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showQR, setShowQR] = useState(false);

  useEffect(() => {
    loadCard();
  }, [id]);

  const loadCard = async () => {
    try {
      const cardData = await firestoreService.getCard(id);
      setCard(cardData);
    } catch (error) {
      console.error('Error loading card:', error);
      showToast(t('error_loading'));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(t('delete') + '?')) {
      try {
        await firestoreService.deleteCard(id);
        showToast(t('card_deleted'));
        navigate('/');
      } catch (error) {
        console.error('Error deleting card:', error);
        showToast(t('error'));
      }
    }
  };

  const handleShare = async () => {
    const success = await shareCard(id, card.name);
    if (success) {
      showToast(t('copied'));
    }
  };

  if (loading) {
    return (
      <div className="screen">
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (!card) {
    return (
      <div className="screen">
        <div className="empty-state">
          <p>{t('error_loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="screen card-detail-screen" data-theme={card.colorTheme}>
      <header className="header">
        <div className="header-content">
          <button className="icon-btn" onClick={() => navigate('/')}>
            ←
          </button>
          <h1 className="header-title">{card.name}</h1>
          <div className="header-actions">
            <button className="icon-btn" onClick={() => navigate(`/edit/${id}`)}>
              ✏️
            </button>
            <button className="icon-btn" onClick={handleDelete}>
              🗑️
            </button>
          </div>
        </div>
      </header>

      <main className="container">
        <div className="card card-detail">
          {card.photoUrl && (
            <img src={card.photoUrl} alt={card.name} className="card-detail-photo" />
          )}

          <h2 className="card-detail-name">{card.name}</h2>

          {card.address && (
            <div className="detail-section">
              <h3 className="detail-section-title">📍 {t('address')}</h3>
              <button className="detail-item" onClick={() => openMap(card.address)}>
                {card.address}
              </button>
            </div>
          )}

          {card.phones && card.phones.length > 0 && (
            <div className="detail-section">
              <h3 className="detail-section-title">📞 {t('phone')}</h3>
              {card.phones.map((phone, index) => (
                <button
                  key={index}
                  className="detail-item"
                  onClick={() => makePhoneCall(phone.value)}
                >
                  <span className="detail-label">{phone.label}</span>
                  <span className="detail-value">{phone.value}</span>
                </button>
              ))}
            </div>
          )}

          {card.emails && card.emails.length > 0 && (
            <div className="detail-section">
              <h3 className="detail-section-title">📧 {t('email')}</h3>
              {card.emails.map((email, index) => (
                <button
                  key={index}
                  className="detail-item"
                  onClick={async () => {
                    await copyToClipboard(email.value);
                    showToast(t('email_copied'));
                  }}
                >
                  <span className="detail-label">{email.label}</span>
                  <span className="detail-value">{email.value}</span>
                </button>
              ))}
            </div>
          )}

          {card.websites && card.websites.length > 0 && (
            <div className="detail-section">
              <h3 className="detail-section-title">🌐 {t('website')}</h3>
              {card.websites.map((website, index) => (
                <button
                  key={index}
                  className="detail-item"
                  onClick={() => openWebsite(website.value)}
                >
                  <span className="detail-label">{website.label}</span>
                  <span className="detail-value">{website.value}</span>
                </button>
              ))}
            </div>
          )}

          {card.faxes && card.faxes.length > 0 && (
            <div className="detail-section">
              <h3 className="detail-section-title">📠 {t('fax')}</h3>
              {card.faxes.map((fax, index) => (
                <button
                  key={index}
                  className="detail-item"
                  onClick={async () => {
                    await copyToClipboard(fax.value);
                    showToast(t('fax_copied'));
                  }}
                >
                  <span className="detail-label">{fax.label}</span>
                  <span className="detail-value">{fax.value}</span>
                </button>
              ))}
            </div>
          )}

          <div className="card-actions">
            <button className="btn btn-primary" onClick={handleShare}>
              {t('share_card')}
            </button>
            <button className="btn btn-secondary" onClick={() => setShowQR(!showQR)}>
              {t('qr_code')}
            </button>
          </div>

          {showQR && (
            <div className="qr-code-container">
              <QRCodeSVG value={getQRCodeURL(id)} size={200} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default CardDetailScreen;
