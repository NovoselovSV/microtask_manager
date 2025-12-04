import { create } from 'zustand';
import { api } from '../api/apiClient';
import { persist, createJSONStorage } from 'zustand/middleware';
import { User, TokenMsg } from '../types';

interface AuthState {
  user: User | null;
  login: (email: string, password: string) => boolean;
  logout: () => void;
  register: (email: string, password: string) => boolean;
}


export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      
      login: async (email, password) => {
        const user = get().user;

        if (user?.token) {
          response = await api.get<User>('/users/v1/me');
        } else {
          response = await api.postForm<TokenMsg>('/users/v1/auth/login', 
                                                  {username: email, password: password}
                                                  );
        }
        console.log(response);
        
        if (user) {
          set({ user: { id: user.id, email: user.email } });
          return true;
        }
        return false;
      },
      
      logout: () => set({ user: null }),
      
      register: (email, password) => {
        
        const newUser = {
          id: crypto.randomUUID(),
          email,
        };
        
        set({ user: { id: newUser.id, email: newUser.email } });
        return true;
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
