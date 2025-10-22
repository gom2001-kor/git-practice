import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { firestoreService, storageService } from '../services/firebase';
import BusinessCard, { DynamicField } from '../models/BusinessCard';
import DynamicFieldEditor from '../components/DynamicFieldEditor';
import { showToast, compressImage } from '../utils/helpers';
import './CreateCardScreen.css';

function CreateCardScreen({ user, theme }) {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { id } = useParams();
  const isEdit = !!id;

  const [card, setCard] = useState(new BusinessCard({ userId: user?.uid }));
  const [loading, setLoading] = useState(false);
  const [photoFile, setPhotoFile] = useState(null);

  useEffect(() => {
    if (isEdit && id) {
      loadCard();
    }
  }, [id]);

  const loadCard = async () => {
    try {
      const cardData = await firestoreService.getCard(id);
      setCard(new BusinessCard(cardData));
    } catch (error) {
      console.error('Error loading card:', error);
      showToast(t('error_loading'));
    }
  };

  const handlePhotoSelect = async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        const compressed = await compressImage(file);
        setPhotoFile(compressed);
        const reader = new FileReader();
        reader.onload = (e) => {
          setCard(new BusinessCard({ ...card, photoUrl: e.target.result }));
        };
        reader.readAsDataURL(compressed);
      } catch (error) {
        console.error('Error compressing image:', error);
      }
    }
  };

  const handleSave = async () => {
    if (!card.isValid()) {
      showToast(t('required_field'));
      return;
    }

    setLoading(true);
    try {
      let photoUrl = card.photoUrl;

      if (photoFile) {
        photoUrl = await storageService.uploadPhoto(photoFile, user.uid);
      }

      const cardToSave = new BusinessCard({
        ...card,
        photoUrl,
        userId: user.uid,
        id: isEdit ? id : null
      });

      await firestoreService.saveCard(cardToSave);
      showToast(t('card_saved'));
      navigate('/');
    } catch (error) {
      console.error('Error saving card:', error);
      showToast(t('error_saving'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screen create-card-screen">
      <header className="header">
        <div className="header-content">
          <button className="icon-btn" onClick={() => navigate('/')}>
            ←
          </button>
          <h1 className="header-title">{isEdit ? t('edit_card') : t('create_card')}</h1>
          <button className="icon-btn" onClick={handleSave} disabled={loading}>
            {loading ? '⏳' : '✓'}
          </button>
        </div>
      </header>

      <main className="container">
        <div className="card form-card">
          <div className="form-group">
            <label className="form-label">{t('photo')}</label>
            <div className="photo-upload">
              {card.photoUrl && (
                <img src={card.photoUrl} alt="Preview" className="photo-preview" />
              )}
              <input
                type="file"
                accept="image/*"
                onChange={handlePhotoSelect}
                id="photo-input"
                style={{ display: 'none' }}
              />
              <button
                className="btn btn-secondary"
                onClick={() => document.getElementById('photo-input').click()}
              >
                {t('select_photo')}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">{t('name')} *</label>
            <input
              type="text"
              className="form-input"
              value={card.name}
              onChange={(e) => setCard(new BusinessCard({ ...card, name: e.target.value }))}
              placeholder={t('name')}
            />
          </div>

          <div className="form-group">
            <label className="form-label">{t('address')}</label>
            <textarea
              className="form-textarea"
              value={card.address}
              onChange={(e) => setCard(new BusinessCard({ ...card, address: e.target.value }))}
              placeholder={t('address')}
            />
          </div>

          <DynamicFieldEditor
            label={t('phone')}
            fields={card.phones}
            onAdd={() => {
              if (card.phones.length < 3) {
                setCard(new BusinessCard({
                  ...card,
                  phones: [...card.phones, new DynamicField('', '')]
                }));
              } else {
                showToast(t('max_fields'));
              }
            }}
            onChange={(index, field, value) => {
              const newPhones = [...card.phones];
              newPhones[index][field] = value;
              setCard(new BusinessCard({ ...card, phones: newPhones }));
            }}
            onRemove={(index) => {
              const newPhones = card.phones.filter((_, i) => i !== index);
              setCard(new BusinessCard({ ...card, phones: newPhones }));
            }}
          />

          <DynamicFieldEditor
            label={t('email')}
            fields={card.emails}
            onAdd={() => {
              if (card.emails.length < 3) {
                setCard(new BusinessCard({
                  ...card,
                  emails: [...card.emails, new DynamicField('', '')]
                }));
              } else {
                showToast(t('max_fields'));
              }
            }}
            onChange={(index, field, value) => {
              const newEmails = [...card.emails];
              newEmails[index][field] = value;
              setCard(new BusinessCard({ ...card, emails: newEmails }));
            }}
            onRemove={(index) => {
              const newEmails = card.emails.filter((_, i) => i !== index);
              setCard(new BusinessCard({ ...card, emails: newEmails }));
            }}
          />

          <DynamicFieldEditor
            label={t('website')}
            fields={card.websites}
            onAdd={() => {
              if (card.websites.length < 3) {
                setCard(new BusinessCard({
                  ...card,
                  websites: [...card.websites, new DynamicField('', '')]
                }));
              } else {
                showToast(t('max_fields'));
              }
            }}
            onChange={(index, field, value) => {
              const newWebsites = [...card.websites];
              newWebsites[index][field] = value;
              setCard(new BusinessCard({ ...card, websites: newWebsites }));
            }}
            onRemove={(index) => {
              const newWebsites = card.websites.filter((_, i) => i !== index);
              setCard(new BusinessCard({ ...card, websites: newWebsites }));
            }}
          />

          <DynamicFieldEditor
            label={t('fax')}
            fields={card.faxes}
            onAdd={() => {
              if (card.faxes.length < 3) {
                setCard(new BusinessCard({
                  ...card,
                  faxes: [...card.faxes, new DynamicField('', '')]
                }));
              } else {
                showToast(t('max_fields'));
              }
            }}
            onChange={(index, field, value) => {
              const newFaxes = [...card.faxes];
              newFaxes[index][field] = value;
              setCard(new BusinessCard({ ...card, faxes: newFaxes }));
            }}
            onRemove={(index) => {
              const newFaxes = card.faxes.filter((_, i) => i !== index);
              setCard(new BusinessCard({ ...card, faxes: newFaxes }));
            }}
          />

          <div className="form-group">
            <label className="form-label">{t('select_template')}</label>
            <select
              className="form-select"
              value={card.templateId}
              onChange={(e) => setCard(new BusinessCard({ ...card, templateId: parseInt(e.target.value) }))}
            >
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                <option key={num} value={num}>
                  {t('template')} {num}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">{t('select_theme')}</label>
            <select
              className="form-select"
              value={card.colorTheme}
              onChange={(e) => setCard(new BusinessCard({ ...card, colorTheme: e.target.value }))}
            >
              <option value="blue">{t('blue_theme')}</option>
              <option value="pink">{t('pink_theme')}</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">{t('privacy_setting')}</label>
            <select
              className="form-select"
              value={card.privacy}
              onChange={(e) => setCard(new BusinessCard({ ...card, privacy: e.target.value }))}
            >
              <option value="public">{t('public')}</option>
              <option value="link_only">{t('link_only')}</option>
              <option value="private">{t('private')}</option>
            </select>
          </div>
        </div>
      </main>
    </div>
  );
}

export default CreateCardScreen;
