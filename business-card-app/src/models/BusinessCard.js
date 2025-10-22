// Business Card Model

export class DynamicField {
  constructor(label = '', value = '') {
    this.label = label;
    this.value = value;
  }

  static fromJSON(json) {
    return new DynamicField(json.label, json.value);
  }

  toJSON() {
    return {
      label: this.label,
      value: this.value
    };
  }
}

export class BusinessCard {
  constructor({
    id = null,
    userId = null,
    name = '',
    photoUrl = '',
    address = '',
    phones = [],
    emails = [],
    websites = [],
    faxes = [],
    templateId = 1,
    colorTheme = 'blue',
    privacy = 'public',
    isAnonymous = true,
    linkedAccountType = null,
    createdAt = null,
    updatedAt = null
  } = {}) {
    this.id = id;
    this.userId = userId;
    this.name = name;
    this.photoUrl = photoUrl;
    this.address = address;
    this.phones = phones.map(p => typeof p === 'object' ? DynamicField.fromJSON(p) : p);
    this.emails = emails.map(e => typeof e === 'object' ? DynamicField.fromJSON(e) : e);
    this.websites = websites.map(w => typeof w === 'object' ? DynamicField.fromJSON(w) : w);
    this.faxes = faxes.map(f => typeof f === 'object' ? DynamicField.fromJSON(f) : f);
    this.templateId = templateId;
    this.colorTheme = colorTheme;
    this.privacy = privacy;
    this.isAnonymous = isAnonymous;
    this.linkedAccountType = linkedAccountType;
    this.createdAt = createdAt || new Date();
    this.updatedAt = updatedAt || new Date();
  }

  static fromFirestore(doc) {
    const data = doc.data();
    return new BusinessCard({
      id: doc.id,
      ...data,
      createdAt: data.createdAt?.toDate(),
      updatedAt: data.updatedAt?.toDate()
    });
  }

  toFirestore() {
    return {
      userId: this.userId,
      name: this.name,
      photoUrl: this.photoUrl,
      address: this.address,
      phones: this.phones.map(p => p.toJSON()),
      emails: this.emails.map(e => e.toJSON()),
      websites: this.websites.map(w => w.toJSON()),
      faxes: this.faxes.map(f => f.toJSON()),
      templateId: this.templateId,
      colorTheme: this.colorTheme,
      privacy: this.privacy,
      isAnonymous: this.isAnonymous,
      linkedAccountType: this.linkedAccountType,
      createdAt: this.createdAt,
      updatedAt: new Date()
    };
  }

  // Helper methods
  addPhone(label, value) {
    if (this.phones.length < 3) {
      this.phones.push(new DynamicField(label, value));
    }
  }

  addEmail(label, value) {
    if (this.emails.length < 3) {
      this.emails.push(new DynamicField(label, value));
    }
  }

  addWebsite(label, value) {
    if (this.websites.length < 3) {
      this.websites.push(new DynamicField(label, value));
    }
  }

  addFax(label, value) {
    if (this.faxes.length < 3) {
      this.faxes.push(new DynamicField(label, value));
    }
  }

  removePhone(index) {
    this.phones.splice(index, 1);
  }

  removeEmail(index) {
    this.emails.splice(index, 1);
  }

  removeWebsite(index) {
    this.websites.splice(index, 1);
  }

  removeFax(index) {
    this.faxes.splice(index, 1);
  }

  isValid() {
    return this.name.trim() !== '';
  }
}

export default BusinessCard;
