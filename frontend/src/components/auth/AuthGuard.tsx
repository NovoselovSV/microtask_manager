import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/useAuthStore';

interface AuthGuardProps {
  children: React.ReactNode;
}

export const AuthGuard = ({ children }: AuthGuardProps) => {
  const currentUser = useAuthStore((state) => state.user);
  const location = useLocation();
  const isTokenCorrect = useAuthStore((state) => state.isTokenCorrect);
  const [isValidToken, setIsValidToken] = useState(false);
  const [isChecking, setIsChecking] = useState(true);
  useEffect(() => {
    const checkAuth = async () => {
      setIsValidToken(await isTokenCorrect());
      setIsChecking(false);
    }
    checkAuth();
  }, [isTokenCorrect]);
  
  if (isChecking) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Проверка аутентификации...</p>
        </div>
      </div>
    );
  }
  if (!currentUser || !isValidToken) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  return <>{children}</>;
};
