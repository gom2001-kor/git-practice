import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, GoogleAuthProvider, linkWithPopup } from 'firebase/auth';
import { getFirestore, collection, doc, setDoc, getDoc, getDocs, query, where, deleteDoc, orderBy } from 'firebase/firestore';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';

// Firebase configuration
// TODO: Replace with your Firebase config
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

// Auth Services
export const authService = {
  // Anonymous sign in
  async signInAnonymously() {
    try {
      const result = await signInAnonymously(auth);
      return result.user;
    } catch (error) {
      console.error('Anonymous sign in error:', error);
      throw error;
    }
  },

  // Link with Google
  async linkWithGoogle() {
    try {
      const provider = new GoogleAuthProvider();
      const result = await linkWithPopup(auth.currentUser, provider);
      return result.user;
    } catch (error) {
      console.error('Google link error:', error);
      throw error;
    }
  },

  // Get current user
  getCurrentUser() {
    return auth.currentUser;
  },

  // Check if user is anonymous
  isAnonymous() {
    return auth.currentUser?.isAnonymous || false;
  }
};

// Firestore Services
export const firestoreService = {
  // Create or update business card
  async saveCard(card) {
    try {
      const cardData = card.toFirestore();
      const cardRef = card.id
        ? doc(db, 'cards', card.id)
        : doc(collection(db, 'cards'));

      await setDoc(cardRef, cardData);
      return cardRef.id;
    } catch (error) {
      console.error('Save card error:', error);
      throw error;
    }
  },

  // Get card by ID
  async getCard(cardId) {
    try {
      const cardRef = doc(db, 'cards', cardId);
      const cardSnap = await getDoc(cardRef);

      if (cardSnap.exists()) {
        return { id: cardSnap.id, ...cardSnap.data() };
      } else {
        throw new Error('Card not found');
      }
    } catch (error) {
      console.error('Get card error:', error);
      throw error;
    }
  },

  // Get all cards for a user
  async getUserCards(userId) {
    try {
      const cardsRef = collection(db, 'cards');
      const q = query(
        cardsRef,
        where('userId', '==', userId),
        orderBy('updatedAt', 'desc')
      );
      const querySnapshot = await getDocs(q);

      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Get user cards error:', error);
      throw error;
    }
  },

  // Delete card
  async deleteCard(cardId) {
    try {
      const cardRef = doc(db, 'cards', cardId);
      await deleteDoc(cardRef);
    } catch (error) {
      console.error('Delete card error:', error);
      throw error;
    }
  },

  // Save card to collection (received cards)
  async saveToCollection(userId, cardId) {
    try {
      const collectionRef = doc(collection(db, 'collections'));
      await setDoc(collectionRef, {
        userId,
        cardId,
        savedAt: new Date()
      });
      return collectionRef.id;
    } catch (error) {
      console.error('Save to collection error:', error);
      throw error;
    }
  },

  // Get user's card collection
  async getCardCollection(userId) {
    try {
      const collectionsRef = collection(db, 'collections');
      const q = query(
        collectionsRef,
        where('userId', '==', userId),
        orderBy('savedAt', 'desc')
      );
      const querySnapshot = await getDocs(q);

      // Get card details for each saved card
      const cardIds = querySnapshot.docs.map(doc => doc.data().cardId);
      const cards = await Promise.all(
        cardIds.map(cardId => this.getCard(cardId))
      );

      return cards;
    } catch (error) {
      console.error('Get card collection error:', error);
      throw error;
    }
  }
};

// Storage Services
export const storageService = {
  // Upload photo
  async uploadPhoto(file, userId) {
    try {
      const timestamp = Date.now();
      const fileName = `${userId}/${timestamp}_${file.name}`;
      const storageRef = ref(storage, `photos/${fileName}`);

      await uploadBytes(storageRef, file);
      const downloadURL = await getDownloadURL(storageRef);

      return downloadURL;
    } catch (error) {
      console.error('Upload photo error:', error);
      throw error;
    }
  }
};

export default {
  auth: authService,
  firestore: firestoreService,
  storage: storageService
};
