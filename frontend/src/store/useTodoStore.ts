import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { api } from '../api/apiClient';
import { Todo } from '../types';

interface TodoState {
  todos: Todo[];
  addTodo: (description: string, finalDate: Date) => void;
  toggleTodo: (id: int) => void;
  clearCompleted: () => void;
  gettingTodos: () => void;
}


export const useTodoStore = create<TodoState>()(
  persist(
    (set, get) => ({
      todos: [],

      gettingTodos: async () => {
        const response_todos = await api.get('/tasks/v1');
        set({ todos: response_todos.data.map((todoArrived) => ({ finalDate: todoArrived.final_dt, id: todoArrived.id, description: todoArrived.description, done: todoArrived.done, doneDate: todoArrived.done_dt, createdAt: todoArrived.created_at }))});
      },
      addTodo: async (description, finalDate) => {
        const response_creation = await api.post('/tasks/v1', { description: description, final_dt: finalDate });
        await get().gettingTodos();
      },

      toggleTodo: async (id) => {
        const state = get()
        const response_toggling = await api.patch(`/tasks/v1/${id}`, { done: !state.todos.find((t) => t.id === id)?.done });
        await state.gettingTodos();
      },

      clearCompleted: () =>
        set((state) => ({
          todos: state.todos.filter((todo) => !todo.completed),
        })),
    }),
    {
      name: 'todo-storage',
    }
  )
);
