import { Todo } from '../types';
import { useTodoStore } from '../store/useTodoStore';

interface TodoItemProps {
  todo: Todo;
}

export const TodoItem = ({ todo }: TodoItemProps) => {
  const toggleTodo = useTodoStore((state) => state.toggleTodo);
  const formatDate = (date: Date | undefined | null) => {
    if (!date) return '—';
  
    if (isNaN(new Date(date).getTime())) {
      return 'Неверная дата';
    }
    return new Date(date).toLocaleString('ru-RU', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    });
  };

  return (
    <div className="flex items-center justify-between p-3 border-b border-gray-200">
      <div className="flex-1 mr-3">
          <label className="flex items-start cursor-pointer">
            <input
              type="checkbox"
              checked={todo.done}
              onChange={async () => await toggleTodo(todo.id)}
              className="h-5 w-5 mt-1 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
            />
            <div className="ml-3">
              <span
                className={`text-lg font-medium ${
                  todo.done ? 'line-through text-gray-500' : 'text-gray-800'
                }`}
              >
                {todo.description}
              </span>
              
              <div className="mt-2 pt-2 border-t border-gray-100 text-sm text-gray-600 space-y-1">
                <div>
                  <span className="font-medium">ID:</span> <span className="font-mono text-xs">{todo.id}</span>
                </div>
                
                <div>
                  <span className="font-medium">Создано:</span> {formatDate(todo.createdAt)}
                </div>
                
                <div>
                  <span className="font-medium">Дедлайн:</span> {formatDate(todo.finalDate)}
                </div>
                
                {todo.done && (
                  <div className="text-green-600">
                    <span className="font-medium">Завершено:</span> {formatDate(todo.doneDate)}
                  </div>
                )}
              </div>
            </div>
          </label>
        </div>
    </div>
  );
};
