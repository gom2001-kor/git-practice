/**
 * Zustand Global State Store
 */
import { create } from 'zustand';

interface StoreState {
  selectedTicker: string | null;
  setSelectedTicker: (ticker: string | null) => void;

  watchlist: any[];
  setWatchlist: (items: any[]) => void;

  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useStore = create<StoreState>((set) => ({
  selectedTicker: null,
  setSelectedTicker: (ticker) => set({ selectedTicker: ticker }),

  watchlist: [],
  setWatchlist: (items) => set({ watchlist: items }),

  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));
