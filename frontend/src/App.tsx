import { TodoInput } from './components/TodoInput';
import { TodoList } from './components/TodoList';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
          Список задач
        </h1>
        <TodoInput />
        <TodoList />
      </div>
    </div>
  );
}

export default App;
