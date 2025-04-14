import { PaymentStatus } from './payment';

export enum VehicleStatus {
  AVAILABLE = 'DISPONÍVEL',
  RESERVED = 'RESERVADO',
  SOLD = 'VENDIDO'
}

export interface Vehicle {
  id: string;
  brand: string;
  model: string;
  year: number;
  color: string;
  price: number;
  status: VehicleStatus;
  created_at: string;
  updated_at: string;
}

export interface Sale {
  id: string;
  vehicle_id: string;
  buyer_cpf: string;
  sale_price: number;
  payment_code: string;
  payment_status: PaymentStatus;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: string;
  sale_id: string;
  amount: number;
  payment_method: string;
  status: PaymentStatus;
  created_at: string;
  updated_at: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
} 