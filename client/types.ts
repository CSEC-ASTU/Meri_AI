
export interface CampusNode {
  id: string;
  name: string;
  description: string;
  category: 'academic' | 'administrative' | 'residential' | 'amenity' | 'gate';
  x: number;
  y: number;
}

export interface RouteEdge {
  from: string;
  to: string;
  weight: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export enum AppRoute {
  HOME = '/',
  MAP = '/map',
  INFO = '/info',
  ASSISTANT = '/assistant',
  DIRECTORY = '/directory'
}
