import { v4 as uuidv4 } from 'uuid';

export interface Todo {
  id: int;
  description: string;
  done: boolean;
  doneDate: Date;
  createdAt: Date;
  finalDate: Date;
}

export interface User {
  id: uuidv4;
  email: string;
  token: string;
}

export interface TokenMsg {
  access_token: string;
  token_type: string;
}
