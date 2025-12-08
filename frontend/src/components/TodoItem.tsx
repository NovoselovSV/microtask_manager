import { useEffect, useState } from 'react';
import { Todo } from '../types';
import { useTodoStore } from '../store/useTodoStore';
import { useSseConnection } from '../api/sseClient';

interface TodoItemProps {
  todo: Todo;
}

export const TodoItem = ({ todo }: TodoItemProps) => {
  const [isHighlighted, setIsHighlighted] = useState(false);
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
  const url = `${import.meta.env.VITE_API_BASE_URL || 'http://localhost'}/tasks/v1/sse`
  const todosEndConnection = useSseConnection(
    url,
    'todos-end-connection'
  );
  const triggerHighlight = () => {
    setIsHighlighted(false);
    
    setTimeout(() => {
      setIsHighlighted(true);
      
      setTimeout(() => {
        setIsHighlighted(false);
      }, 2000);
    }, 50);
  };
  useEffect(() => {
    const unsubTodos = todosEndConnection.subscribe('*', (message) => {
      console.log('Время задачи вышло', message.payload);
      triggerHighlight();
    });
    
    
    const unsubErrorTodos = todosEndConnection.onError((error) => {
      console.error('Ошибка окончания времени задачи:', error);
    });
    
    
    return () => {
      unsubTodos();
      unsubErrorTodos();
    };
  }, [todosEndConnection]);

  return (
    <div className={`flex items-center justify-between p-3 border-b ${isHighlighted ? "bg-red-100 border-red-300 animate-pulse" : "border-gray-200"}`}>
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
