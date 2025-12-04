import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { AuthGuard } from './components/auth/AuthGuard';
import { LoginForm } from './components/auth/LoginForm';
import { RegisterForm } from './components/auth/RegisterForm';
import { TodoList } from './components/TodoList';
import { TodoInput } from './components/TodoInput';
import { UserProfile } from './components/UserProfile';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          
          <Route 
            path="/" 
            element={
              <AuthGuard>
                <TodoInput />
                <TodoList />
              </AuthGuard>
            } 
          />
          
          <Route 
            path="/profile" 
            element={
              <AuthGuard>
                <UserProfile />
              </AuthGuard>
            } 
          />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}
export default App;
