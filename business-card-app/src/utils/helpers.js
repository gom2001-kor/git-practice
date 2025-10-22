// Helper functions

// Copy text to clipboard
export const copyToClipboard = async (text) => {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    } else {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand('copy');
        textArea.remove();
        return true;
      } catch (error) {
        console.error('Fallback: Could not copy text', error);
        textArea.remove();
        return false;
      }
    }
  } catch (error) {
    console.error('Could not copy text: ', error);
    return false;
  }
};

// Make phone call
export const makePhoneCall = (phoneNumber) => {
  const cleanNumber = phoneNumber.replace(/[^0-9+]/g, '');
  window.location.href = `tel:${cleanNumber}`;
};

// Open email client
export const openEmailClient = (email) => {
  window.location.href = `mailto:${email}`;
};

// Open website
export const openWebsite = (url) => {
  let formattedUrl = url;
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    formattedUrl = 'https://' + url;
  }
  window.open(formattedUrl, '_blank', 'noopener,noreferrer');
};

// Open map application
export const openMap = (address) => {
  const encodedAddress = encodeURIComponent(address);

  // Detect device
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
  const isAndroid = /Android/.test(navigator.userAgent);

  if (isIOS) {
    // Use Apple Maps on iOS
    window.location.href = `maps://maps.apple.com/?q=${encodedAddress}`;
  } else if (isAndroid) {
    // Use Google Maps on Android
    window.location.href = `geo:0,0?q=${encodedAddress}`;
  } else {
    // Use Google Maps in browser
    window.open(`https://www.google.com/maps/search/?api=1&query=${encodedAddress}`, '_blank');
  }
};

// Share card
export const shareCard = async (cardId, cardName) => {
  const shareUrl = `${window.location.origin}/card/${cardId}`;
  const shareText = `${cardName}님의 디지털 명함`;

  if (navigator.share) {
    try {
      await navigator.share({
        title: shareText,
        text: shareText,
        url: shareUrl
      });
      return true;
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Share error:', error);
      }
      return false;
    }
  } else {
    // Fallback: copy link to clipboard
    return await copyToClipboard(shareUrl);
  }
};

// Detect device OS
export const getDeviceOS = () => {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;

  if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
    return 'iOS';
  }

  if (/android/i.test(userAgent)) {
    return 'Android';
  }

  return 'Other';
};

// Get app store URL
export const getAppStoreURL = () => {
  const os = getDeviceOS();

  if (os === 'iOS') {
    return 'https://apps.apple.com'; // TODO: Add actual App Store URL
  } else if (os === 'Android') {
    return 'https://play.google.com'; // TODO: Add actual Play Store URL
  }

  return null;
};

// Format phone number
export const formatPhoneNumber = (phoneNumber) => {
  const cleaned = phoneNumber.replace(/\D/g, '');

  if (cleaned.length === 11) {
    // Korean mobile: 010-1234-5678
    return cleaned.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3');
  } else if (cleaned.length === 10) {
    // Korean landline: 02-1234-5678 or 031-123-4567
    if (cleaned.startsWith('02')) {
      return cleaned.replace(/(\d{2})(\d{4})(\d{4})/, '$1-$2-$3');
    } else {
      return cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
    }
  }

  return phoneNumber;
};

// Validate email
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate URL
export const isValidURL = (url) => {
  try {
    const urlObj = new URL(url.startsWith('http') ? url : 'https://' + url);
    return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
  } catch {
    return false;
  }
};

// Generate QR code URL
export const getQRCodeURL = (cardId) => {
  return `${window.location.origin}/card/${cardId}`;
};

// Show toast message
export const showToast = (message, duration = 3000) => {
  // Create toast element
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 12px 24px;
    border-radius: 24px;
    font-size: 14px;
    z-index: 10000;
    animation: fadeIn 0.3s, fadeOut 0.3s ${duration - 300}ms;
  `;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, duration);
};

// Add CSS for toast animation
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  @keyframes fadeOut {
    from {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    to {
      opacity: 0;
      transform: translateX(-50%) translateY(20px);
    }
  }
`;
document.head.appendChild(style);

// Image compression
export const compressImage = async (file, maxWidth = 800, maxHeight = 800, quality = 0.8) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (event) => {
      const img = new Image();
      img.src = event.target.result;
      img.onload = () => {
        const canvas = document.createElement('canvas');
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }
        }

        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            resolve(new File([blob], file.name, {
              type: 'image/jpeg',
              lastModified: Date.now()
            }));
          },
          'image/jpeg',
          quality
        );
      };
      img.onerror = reject;
    };
    reader.onerror = reject;
  });
};

export default {
  copyToClipboard,
  makePhoneCall,
  openEmailClient,
  openWebsite,
  openMap,
  shareCard,
  getDeviceOS,
  getAppStoreURL,
  formatPhoneNumber,
  isValidEmail,
  isValidURL,
  getQRCodeURL,
  showToast,
  compressImage
};
