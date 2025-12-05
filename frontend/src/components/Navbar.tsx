import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';

export const Navbar = () => {
  const currentUser = useAuthStore((state) => state.user);
  const navigate = useNavigate();

  if (!currentUser) {
    return null;
  }

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            
            <div className="hidden md:flex md:ml-10 md:space-x-8">
              <Link 
                to="/" 
                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Список дел
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:block">
              <Link 
                to="/profile" 
                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                <span className="text-gray-700 font-medium">{currentUser.email}</span>
              </Link>
            </div>
            
          </div>
        </div>
      </div>
      
    </nav>
  );
};
