import { useTranslation } from 'react-i18next';
import './DynamicFieldEditor.css';

function DynamicFieldEditor({ label, fields, onAdd, onChange, onRemove }) {
  const { t } = useTranslation();

  return (
    <div className="dynamic-field-editor">
      <div className="field-editor-header">
        <label className="form-label">{label}</label>
        <button className="btn-add-field" onClick={onAdd} disabled={fields.length >= 3}>
          + {t('add')}
        </button>
      </div>

      {fields.map((field, index) => (
        <div key={index} className="field-item">
          <input
            type="text"
            className="form-input field-label-input"
            placeholder={t('label')}
            value={field.label}
            onChange={(e) => onChange(index, 'label', e.target.value)}
          />
          <input
            type="text"
            className="form-input field-value-input"
            placeholder={t('value')}
            value={field.value}
            onChange={(e) => onChange(index, 'value', e.target.value)}
          />
          <button className="btn-remove-field" onClick={() => onRemove(index)}>
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}

export default DynamicFieldEditor;
