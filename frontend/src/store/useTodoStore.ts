import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { Todo } from '../types';

interface TodoState {
  todos: Todo[];
  addTodo: (description: string, finalDate: Date) => void;
  toggleTodo: (id: int) => void;
  clearCompleted: () => void;
}


export const useTodoStore = create<TodoState>()(
  persist(
    (set) => ({
      todos: [],

      addTodo: (description, finalDate) =>
        set((state) => ({
          todos: [
            ...state.todos,
            {
              description: description.trim(),
              finalDate: finalDate
            },
          ],
        })),

      toggleTodo: (id) =>
        set((state) => ({
          todos: state.todos.map((todo) =>
            todo.id === id ? { ...todo, done: !todo.done } : todo
          ),
        })),

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
