import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { firestoreService } from '../services/firebase';
import {
  copyToClipboard,
  makePhoneCall,
  openEmailClient,
  openWebsite,
  openMap,
  showToast,
  getDeviceOS,
  getAppStoreURL
} from '../utils/helpers';
import './ViewCardScreen.css';

function ViewCardScreen({ theme }) {
  const { t } = useTranslation();
  const { id } = useParams();
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(true);

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

  const handleInstallApp = () => {
    const appStoreURL = getAppStoreURL();
    if (appStoreURL) {
      window.open(appStoreURL, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="view-card-screen">
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (!card) {
    return (
      <div className="view-card-screen">
        <div className="empty-state">
          <p>{t('error_loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="view-card-screen" data-theme={card.colorTheme}>
      <div className="view-card-container">
        <div className="view-card">
          {card.photoUrl && (
            <img src={card.photoUrl} alt={card.name} className="view-card-photo" />
          )}

          <h1 className="view-card-name">{card.name}</h1>

          {card.address && (
            <div className="view-section">
              <div className="view-section-title">📍 {t('address')}</div>
              <button className="view-item" onClick={() => openMap(card.address)}>
                {card.address}
              </button>
            </div>
          )}

          {card.phones && card.phones.length > 0 && (
            <div className="view-section">
              <div className="view-section-title">📞 {t('phone')}</div>
              {card.phones.map((phone, index) => (
                <button
                  key={index}
                  className="view-item"
                  onClick={() => makePhoneCall(phone.value)}
                >
                  <span className="view-label">{phone.label}</span>
                  <span className="view-value">{phone.value}</span>
                </button>
              ))}
            </div>
          )}

          {card.emails && card.emails.length > 0 && (
            <div className="view-section">
              <div className="view-section-title">📧 {t('email')}</div>
              {card.emails.map((email, index) => (
                <button
                  key={index}
                  className="view-item"
                  onClick={async () => {
                    await copyToClipboard(email.value);
                    showToast(t('email_copied'));
                  }}
                >
                  <span className="view-label">{email.label}</span>
                  <span className="view-value">{email.value}</span>
                </button>
              ))}
            </div>
          )}

          {card.websites && card.websites.length > 0 && (
            <div className="view-section">
              <div className="view-section-title">🌐 {t('website')}</div>
              {card.websites.map((website, index) => (
                <button
                  key={index}
                  className="view-item"
                  onClick={() => openWebsite(website.value)}
                >
                  <span className="view-label">{website.label}</span>
                  <span className="view-value">{website.value}</span>
                </button>
              ))}
            </div>
          )}

          {card.faxes && card.faxes.length > 0 && (
            <div className="view-section">
              <div className="view-section-title">📠 {t('fax')}</div>
              {card.faxes.map((fax, index) => (
                <button
                  key={index}
                  className="view-item"
                  onClick={async () => {
                    await copyToClipboard(fax.value);
                    showToast(t('fax_copied'));
                  }}
                >
                  <span className="view-label">{fax.label}</span>
                  <span className="view-value">{fax.value}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <button className="install-app-btn" onClick={handleInstallApp}>
          {t('install_app')}
        </button>
      </div>
    </div>
  );
}

export default ViewCardScreen;
