import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';
import { useTodoStore } from '../store/useTodoStore';

export const UserProfile = () => {
  const [newEmail, setNewEmail] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  const currentUser = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const getTodosForUser = useTodoStore((state) => state.getTodosForUser);
  const navigate = useNavigate();

  useEffect(() => {
    if (!currentUser) {
      navigate('/login');
      return;
    }
    
    setNewEmail(currentUser.email);
  }, [currentUser, navigate, isEditingEmail]);

  const handleUpdateProfile = (e: React.FormEvent) => {
    e.preventDefault();

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newEmail)) {
      setError('Пожалуйста, введите корректный email');
      return;
    }
    
    if (newEmail === currentUser?.email) {
      setError('Новый email должен отличаться от текущего');
      return;
    }

    useAuthStore.setState(state => ({
        currentUser: state.user ? {
          ...state.user,
          email: newEmail
        } : null
      }));

    try {
      useAuthStore.setState(state => ({
         user: state.user ? {
           ...state.user,
           email: newEmail
         } : null
        }));
      setIsEditing(false);
      setSuccessMessage('Профиль успешно обновлен!');
    
      setTimeout(() => {
       setSuccessMessage('');
      }, 3000);
    } catch (err) {
      setError('Ошибка при обновлении email. Попробуйте еще раз.');
      console.error('Update email error:', err);
    }
    
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!currentUser) {
    return null;
  }


  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Профиль пользователя
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Информация о вашем аккаунте и статистика
            </p>
          </div>
          
          <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
            <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
              <div className="flex-1 text-center md:text-left">
                <p className="mt-1 text-lg text-gray-500">
                  {currentUser.email}
                </p>
                
              </div>
            </div>
          </div>
        </div>
        
        {successMessage && (
          <div className="mt-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
            {successMessage}
          </div>
        )}
        
        <div className="mt-6 bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {isEditing ? 'Редактирование профиля' : 'Информация о профиле'}
            </h3>
          </div>
          
          {isEditing ? (
            <form onSubmit={handleUpdateProfile} className="px-4 py-5 sm:p-6">
              <div className="space-y-6">
                <div>
                  <label htmlFor="current-email" className="block text-sm font-medium text-gray-700">
                    Текущий email
                  </label>
                  <input
                    type="email"
                    id="current-email"
                    value={currentUser.email}
                    disabled
                    className="mt-1 block w-full bg-gray-100 border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none sm:text-sm"
                  />
                </div>
                
                <div>
                  <label htmlFor="new-email" className="block text-sm font-medium text-gray-700">
                    Новый email
                  </label>
                  <input
                    type="email"
                    id="new-email"
                    value={newEmail}
                    onChange={(e) => setNewEmail(e.target.value)}
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="newemail@example.com"
                  />
                </div>
                
              </div>
              
              <div className="mt-6 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setIsEditingEmail(false);
                    setError('');
                    setNewEmail(currentUser.email);
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Отменить
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Сохранить email
                </button>
              </div>
            </form>
          ) : (
            <div className="px-4 py-5 sm:p-6">
              
              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setIsEditing(true)}
                  className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Редактировать профиль
                </button>
              </div>
            </div>
          )}
        </div>
        
        <div className="mt-6 bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Действия с аккаунтом
            </h3>
          </div>
          
          <div className="border-t border-gray-200 px-4 py-5 sm:px-6">
            <div className="space-y-4">
              <button
                onClick={handleLogout}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Выйти из аккаунта
              </button>
              
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
