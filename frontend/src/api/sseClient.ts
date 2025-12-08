import { useEffect, useRef, useCallback } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { EventSourcePolyfill } from 'event-source-polyfill';

export interface SseMessage {
  type: string;
  payload: any;
  timestamp: string;
  id?: string;
}

export type SseEventHandler = (message: SseMessage) => void;
export type SseErrorHandler = (error: Event) => void;

interface SseConnection {
  eventSource: EventSource | null;
  eventHandlers: Map<string, SseEventHandler[]>;
  onErrorHandlers: SseErrorHandler[];
  close: () => void;
}

class SseManager {
  private connections = new Map<string, SseConnection>();
  private authStore = useAuthStore;

  createConnection(url: string, connectionId: string): SseConnection {
    this.closeConnection(connectionId);
    
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMmMzN2RhZC1iZjI2LTRiMTYtOWJkMS1mODdkYzlhZTRkN2EiLCJhdWQiOlsiZmFzdGFwaS11c2VyczphdXRoIl0sImV4cCI6MTc2NTIxOTI1Nn0.R7eoiay_Iqdw8T8x6ViT-xQbDyYgACH91L5yxHVPfSE';
    const headers: Record<string, string> = {};
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const eventSource = new EventSourcePolyfill(url, {headers: headers});
    console.log(eventSource);
    
    const connection: SseConnection = {
      eventSource,
      eventHandlers: new Map(),
      onErrorHandlers: [],
      
      close: () => {
        if (eventSource) {
          eventSource.close();
          console.log(`CloseOperation SSE соединение "${connectionId}" закрыто`);
        }
        this.connections.delete(connectionId);
      }
    };
    
    eventSource.onmessage = (event) => {
      console.log(event);
      if (!event.data) {
        return;
      }
      try {
        const parsedData = JSON.parse(event.data);
        const message: SseMessage = {
          type: event.type || 'message',
          payload: parsedData,
          timestamp: new Date().toISOString(),
          id: event.lastEventId || Date.now().toString()
        };
        
        connection.eventHandlers.forEach((handlers, eventType) => {
          if (message.type === eventType || eventType === '*') {
            handlers.forEach(handler => handler(message));
          }
        });
        
      } catch (error) {
        console.error(`Ошибка обработки сообщения для "${connectionId}"`, error);
      }
    };
    
    eventSource.onerror = (error) => {
      console.error(`Ошибка соединения "${connectionId}"`, error);
      connection.onErrorHandlers.forEach(handler => handler(error));
      
      setTimeout(() => {
        if (this.connections.has(connectionId)) {
          this.createConnection(url, connectionId);
        }
      }, 3000);
    };
    
    eventSource.onopen = () => {
      console.log(`SSE соединение "${connectionId}" установлено`);
    };
    
    this.connections.set(connectionId, connection);
    return connection;
  }
  
  getConnection(url: string, connectionId: string): SseConnection {
    if (this.connections.has(connectionId)) {
      return this.connections.get(connectionId)!;
    }
    return this.createConnection(url, connectionId);
  }
  
  subscribe(connectionId: string, eventType: string, handler: SseEventHandler): () => void {
    const connection = this.connections.get(connectionId);
    if (!connection) {
      console.error(`Соединение "${connectionId}" не найдено`);
      return () => {};
    }
    
    if (!connection.eventHandlers.has(eventType)) {
      connection.eventHandlers.set(eventType, []);
    }
    
    const handlers = connection.eventHandlers.get(eventType) || [];
    handlers.push(handler);
    connection.eventHandlers.set(eventType, handlers);
    
    return () => {
      const currentHandlers = connection.eventHandlers.get(eventType) || [];
      const newHandlers = currentHandlers.filter(h => h !== handler);
      
      if (newHandlers.length === 0) {
        connection.eventHandlers.delete(eventType);
      } else {
        connection.eventHandlers.set(eventType, newHandlers);
      }
    };
  }
  
  onError(connectionId: string, handler: SseErrorHandler): () => void {
    const connection = this.connections.get(connectionId);
    if (!connection) return () => {};
    
    connection.onErrorHandlers.push(handler);
    
    return () => {
      connection.onErrorHandlers = connection.onErrorHandlers.filter(h => h !== handler);
    };
  }
  
  closeConnection(connectionId: string) {
    const connection = this.connections.get(connectionId);
    if (connection) {
      connection.close();
      this.connections.delete(connectionId);
    }
  }
  
  closeAllConnections() {
    this.connections.forEach((connection, id) => {
      connection.close();
    });
    this.connections.clear();
  }
}

export const sseManager = new SseManager();

export const useSseConnection = (url: string, connectionId: string) => {
  const unsubscribeRef = useRef<() => void[]>([]);
  
  useEffect(() => {
    const connection = sseManager.getConnection(url, connectionId);
    
    return () => {
      unsubscribeRef.current.forEach(unsub => unsub());
      unsubscribeRef.current = [];
    };
  }, [url, connectionId]);
  
  const subscribe = useCallback((eventType: string, handler: SseEventHandler) => {
    const unsubscribe = sseManager.subscribe(connectionId, eventType, handler);
    unsubscribeRef.current.push(unsubscribe);
    return unsubscribe;
  }, [connectionId]);
  
  const onError = useCallback((handler: SseErrorHandler) => {
    return sseManager.onError(connectionId, handler);
  }, [connectionId]);
  
  const closeConnection = useCallback(() => {
    sseManager.closeConnection(connectionId);
  }, [connectionId]);
  
  return {
    subscribe,
    onError,
    closeConnection
  };
};
