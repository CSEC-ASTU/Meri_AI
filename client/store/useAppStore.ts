import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { AppRoute } from '../types';

interface AppState {
  // Navigation
  currentRoute: AppRoute;
  setCurrentRoute: (route: AppRoute) => void;
  
  // Map & Location
  selectedDestId: string | undefined;
  setSelectedDestId: (id: string | undefined) => void;
  
  // Search
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  
  // AI Assistant
  messages: Array<{ role: 'user' | 'assistant'; content: string }>;
  addMessage: (message: { role: 'user' | 'assistant'; content: string }) => void;
  clearMessages: () => void;
  
  // Actions
  handleSearch: (query: string) => void;
  navigateToDestination: (destId: string) => void;
  reset: () => void;
}

const initialState = {
  currentRoute: AppRoute.HOME,
  selectedDestId: undefined,
  searchQuery: '',
  messages: [],
};

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        // Navigation
        setCurrentRoute: (route) => set({ currentRoute: route }),

        // Map & Location
        setSelectedDestId: (id) => set({ selectedDestId: id }),

        // Search
        setSearchQuery: (query) => set({ searchQuery: query }),

        // AI Assistant Messages
        addMessage: (message) =>
          set((state) => ({
            messages: [...state.messages, message],
          })),

        clearMessages: () => set({ messages: [] }),

        // Combined Actions
        handleSearch: (query) => {
          set({ searchQuery: query, currentRoute: AppRoute.MAP });
        },

        navigateToDestination: (destId) => {
          set({
            selectedDestId: destId,
            currentRoute: AppRoute.MAP,
          });
        },

        // Reset
        reset: () => set(initialState),
      }),
      {
        name: 'astu-route-storage',
        partialize: (state) => ({
          // Only persist these fields
          searchQuery: state.searchQuery,
          messages: state.messages,
        }),
      }
    ),
    { name: 'ASTU Route Store' }
  )
);
