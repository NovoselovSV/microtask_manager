export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface ApiError {
  message: string;
  code?: number;
  details?: any;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost';

const getAuthToken = async (): string | null => {
  const authStore = await import('../store/useAuthStore');
  const token = authStore.useAuthStore.getState().user?.token;
  
  return token;
};

export const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> => {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = await getAuthToken();
  
  const headers = new Headers(options.headers || {});
  
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  
  if (!headers.get('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  
  const requestOptions: RequestInit = {
    ...options,
    headers,
  };
  
  try {
    const response = await fetch(url, requestOptions);
    
    let data: any;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }
    
    if (!response.ok) {
      const error: ApiError = {
        message: data.message || `Ошибка ${response.status}: ${response.statusText}`,
        code: response.status,
        details: data
      };
      
      if (response.status === 401) {
        const authStore = await import('../store/useAuthStore');
        authStore.useAuthStore.getState().logout();
      }
      
      throw error;
    }
    
    return {
      data: data as T,
      success: true
    };
  } catch (error) {
    console.error('API request failed:', error);
    
    if (error instanceof Error) {
      throw {
        message: error.message || 'Ошибка сети',
        code: 0
      } as ApiError;
    }
    
    throw error;
  }
};

export const api = {
  get: <T>(endpoint: string, options?: RequestInit) => 
    apiRequest<T>(endpoint, { method: 'GET', ...options }),
  
  post: <T>(endpoint: string, body?: any, options?: RequestInit) => 
    apiRequest<T>(endpoint, { 
      method: 'POST', 
      body: body ? JSON.stringify(body) : undefined,
      ...options 
    }),
  
  postForm: <T>(endpoint: string, body?: any, options?: RequestInit) => 
    apiRequest<T>(endpoint, { 
      method: 'POST', 
      body: body ? new URLSearchParams(body).toString() : undefined,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      ...options 
    }),
  
  put: <T>(endpoint: string, body?: any, options?: RequestInit) => 
    apiRequest<T>(endpoint, { 
      method: 'PUT', 
      body: body ? JSON.stringify(body) : undefined,
      ...options 
    }),
  
  delete: <T>(endpoint: string, options?: RequestInit) => 
    apiRequest<T>(endpoint, { method: 'DELETE', ...options }),
  
  patch: <T>(endpoint: string, body?: any, options?: RequestInit) => 
    apiRequest<T>(endpoint, { 
      method: 'PATCH', 
      body: body ? JSON.stringify(body) : undefined,
      ...options 
    }),
};
