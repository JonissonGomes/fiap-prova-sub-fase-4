import { PaymentStatus } from './payment';

export interface SaleUpdate {
  vehicle_id?: string;
  buyer_cpf?: string;
  sale_price?: number;
  payment_code?: string;
  payment_status?: PaymentStatus;
}

export interface SaleCreate {
  vehicle_id: string;
  buyer_cpf: string;
  sale_price: number;
  payment_code: string;
  payment_status: PaymentStatus;
} 