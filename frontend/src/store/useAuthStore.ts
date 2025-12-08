import { create } from 'zustand';
import { api } from '../api/apiClient';
import { persist, createJSONStorage } from 'zustand/middleware';
import { User, TokenMsg } from '../types';

interface AuthState {
  user: User | null;
  login: (email: string, password: string) => boolean;
  isTokenCorrect: () => boolean;
  update: () => boolean;
  logout: () => void;
  register: (email: string, password: string) => boolean;
}


export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      
      login: async (email, password) => {
        const user = get().user;
        let token = user?.token;

        try {
          if (!token) {
           const response_token = await api.postForm<TokenMsg>('/users/v1/auth/login', 
                                                   {username: email, password: password}
                                                   );
           token = response_token.data.access_token;
          }

          const response_user = await api.get<User>('/users/v1/me', { headers: { Authorization: `Bearer ${token}`}});
          set({ user: { id: response_user.data.id, email: response_user.data.email, token: token } });

        } catch {
          return false;
        }
        
        return true;
      },
      
      logout: () => set({ user: null }),
      update: async () => {
        return await get().isTokenCorrect();
      },
      isTokenCorrect: async () => {
        const token = get().user?.token;
        if (!token) {
          return false;
        }
        try {
          const response_user = await api.get<User>('/users/v1/me');
          set({ user: { id: response_user.data.id, email: response_user.data.email, token: token } });
        } catch {
          return false;
        }
        return true;
      },
      
      register: async (email, password) => {
        const response_register = await api.post<User>('/users/v1/auth/register', { email: email, password: password })
        
        set({ user: { id: response_register.data.id, email: response_register.data.email } });
        return true;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
