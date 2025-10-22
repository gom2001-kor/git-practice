import './BusinessCardPreview.css';

function BusinessCardPreview({ card, theme, onClick }) {
  return (
    <div className="business-card-preview" data-theme={theme} onClick={onClick}>
      <div className="card-preview-header">
        {card.photoUrl && (
          <img src={card.photoUrl} alt={card.name} className="card-preview-photo" />
        )}
        <div className="card-preview-info">
          <h3 className="card-preview-name">{card.name}</h3>
          {card.phones && card.phones.length > 0 && (
            <p className="card-preview-detail">📞 {card.phones[0].value}</p>
          )}
          {card.emails && card.emails.length > 0 && (
            <p className="card-preview-detail">📧 {card.emails[0].value}</p>
          )}
        </div>
      </div>
      <div className="card-preview-footer">
        <span className="card-preview-template">Template {card.templateId || 1}</span>
        <span className="card-preview-privacy">{card.privacy || 'public'}</span>
      </div>
    </div>
  );
}

export default BusinessCardPreview;
