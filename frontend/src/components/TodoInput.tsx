import { useState } from 'react';
import { useTodoStore } from '../store/useTodoStore';

export const TodoInput = () => {
  const [description, setDescription] = useState('');
  const [finalDate, setFinalDate] = useState('');
  const addTodo = useTodoStore((state) => state.addTodo);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim() || !finalDate) {
      alert('Пожалуйста, заполните текст задачи и дату окончания');
      return;
    }
    const dueDateObj = new Date(finalDate);
    if (isNaN(dueDateObj.getTime())) {
      alert('Неверный формат даты');
      return;
    }

    await addTodo(description, finalDate);
    setDescription('');
    setFinalDate('');
  };

    return (
    <form onSubmit={handleSubmit} className="mb-6 space-y-3">
      <div>
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Что нужно сделать?"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          autoFocus
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Дата окончания
        </label>
        <input
          type="datetime-local"
          value={finalDate}
          onChange={(e) => setFinalDate(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium"
      >
        Добавить задачу
      </button>
    </form>
    );
};
