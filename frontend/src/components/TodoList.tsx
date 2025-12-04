import { useTodoStore } from '../store/useTodoStore';
import { TodoItem } from './TodoItem';

export const TodoList = () => {
  const todos = useTodoStore((state) => state.todos);
  const clearCompleted = useTodoStore((state) => state.clearCompleted);

  const completedCount = todos.filter((t) => t.completed).length;

  return (
    <div className="w-full bg-white rounded-lg shadow">
      <div className="p-4">
        {todos.length === 0 ? (
          <p className="text-gray-500 text-center py-4">Нет задач</p>
        ) : (
          todos.map((todo) => <TodoItem key={todo.description/*TODO change to id*/} todo={todo} />)
        )}
      </div>

      {completedCount > 0 && (
        <div className="px-4 py-2 bg-gray-50 border-t border-gray-200 flex justify-between items-center">
          <span className="text-sm text-gray-600">
            Завершено: {completedCount} из {todos.length}
          </span>
          <button
            onClick={clearCompleted}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Очистить завершённые
          </button>
        </div>
      )}
    </div>
  );
};
