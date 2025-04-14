import axios from 'axios';
import { Vehicle, Sale, Payment, ApiResponse } from '../types';
import { SaleUpdate } from 'types/sale';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

const salesApiInstance = axios.create({
  baseURL: process.env.REACT_APP_SALES_API_URL || 'http://localhost:8001',
  headers: {
    'Content-Type': 'application/json'
  }
});

const vehiclesApiInstance = axios.create({
  baseURL: process.env.REACT_APP_VEHICLES_API_URL || 'http://localhost:8000'
});

export const vehiclesApi = {
  list: async (): Promise<Vehicle[]> => {
    try {
      const response = await api.get<Vehicle[]>('/vehicles');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar veículos:', error);
      throw error;
    }
  },

  create: async (data: Omit<Vehicle, 'id' | 'created_at' | 'updated_at'>): Promise<Vehicle> => {
    const response = await api.post<ApiResponse<Vehicle>>('/vehicles', data);
    return response.data.data;
  },

  update: async (id: string, data: Partial<Vehicle>): Promise<Vehicle> => {
    const response = await api.put<ApiResponse<Vehicle>>(`/vehicles/${id}`, data);
    return response.data.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/vehicles/${id}`);
  },

  markAsAvailable: async (id: string): Promise<Vehicle> => {
    const response = await api.post<ApiResponse<Vehicle>>(`/vehicles/${id}/mark-as-available`);
    return response.data.data;
  },

  markAsReserved: async (id: string): Promise<Vehicle> => {
    const response = await api.post<ApiResponse<Vehicle>>(`/vehicles/${id}/mark-as-reserved`);
    return response.data.data;
  },

  markAsSold: async (id: string): Promise<Vehicle> => {
    try {
      const response = await vehiclesApiInstance.post<Vehicle>(`/vehicles/${id}/mark-as-sold`);
      return response.data;
    } catch (error) {
      console.error('Erro ao marcar veículo como vendido:', error);
      throw error;
    }
  }
};

export const salesApi = {
  list: async (): Promise<Sale[]> => {
    try {
      const response = await salesApiInstance.get<Sale[]>('/sales');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar vendas:', error);
      throw error;
    }
  },

  create: async (data: Omit<Sale, 'id' | 'created_at' | 'updated_at'>): Promise<Sale> => {
    try {
      const response = await salesApiInstance.post<Sale>('/sales', data);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar venda:', error);
      throw error;
    }
  },

  update: async (id: string, sale: SaleUpdate): Promise<Sale> => {
    try {
      
      // Validação dos dados
      if (sale.vehicle_id && sale.vehicle_id.length < 1) {
        throw new Error('ID do veículo inválido');
      }
      
      if (sale.buyer_cpf && (sale.buyer_cpf.length < 11 || sale.buyer_cpf.length > 11)) {
        throw new Error('CPF deve ter 11 dígitos');
      }
      
      if (sale.sale_price && sale.sale_price <= 0) {
        throw new Error('Preço da venda deve ser maior que zero');
      }
      
      if (sale.payment_code && sale.payment_code.length < 1) {
        throw new Error('Código do pagamento inválido');
      }
      
      // Busca a venda atual para obter os valores não alterados
      const currentSale = await salesApiInstance.get<Sale>(`/sales/${id}`);
      
      // Combina os dados atuais com as alterações
      const updateData = {
        vehicle_id: sale.vehicle_id ?? currentSale.data.vehicle_id,
        buyer_cpf: sale.buyer_cpf ?? currentSale.data.buyer_cpf,
        sale_price: sale.sale_price ?? currentSale.data.sale_price,
        payment_code: sale.payment_code ?? currentSale.data.payment_code,
        payment_status: sale.payment_status ?? currentSale.data.payment_status
      };
      
      const response = await salesApiInstance.put<Sale>(`/sales/${id}`, updateData);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar venda:', error);
      throw error;
    }
  },

  delete: async (id: string): Promise<void> => {
    try {
      const response = await salesApiInstance.delete(`/sales/${id}`);
      
      // Se chegou aqui, a requisição foi bem sucedida
      // Não importa se o status é 200, 204 ou 404
      // pois o servidor pode retornar 404 mesmo quando a deleção é bem sucedida
      return;
    } catch (error: any) {
      console.error('Erro ao deletar venda:', error);
      // Se o erro for 404, podemos considerar como sucesso
      // pois pode significar que o item já foi deletado
      if (error.response?.status === 404) {
        console.log('Venda não encontrada (já deletada?)');
        return;
      }
      throw error;
    }
  },

  markAsPending: async (id: string): Promise<Sale> => {
    try {
      const response = await salesApiInstance.patch<Sale>(`/sales/${id}/status/pending`);
      return response.data;
    } catch (error) {
      console.error('Erro ao marcar venda como pendente:', error);
      throw error;
    }
  },

  markAsPaid: async (id: string): Promise<Sale> => {
    try {
      const response = await salesApiInstance.patch<Sale>(`/sales/${id}/status/paid`);
      return response.data;
    } catch (error) {
      console.error('Erro ao marcar venda como paga:', error);
      throw error;
    }
  },

  markAsCancelled: async (id: string): Promise<Sale> => {
    try {
      const response = await salesApiInstance.patch<Sale>(`/sales/${id}/status/cancelled`);
      return response.data;
    } catch (error) {
      console.error('Erro ao marcar venda como cancelada:', error);
      throw error;
    }
  },

  notifyPaymentWebhook: async (paymentCode: string, status: string, vehicleId: string): Promise<void> => {
    try {
      const response = await salesApiInstance.post('/sales/webhook/payment', {
        payment_code: paymentCode,
        status,
        vehicle_id: vehicleId
      });
    } catch (error) {
      console.error('Erro ao notificar webhook de pagamento:', error);
      throw error;
    }
  },

  createPayment: async (saleId: string, paymentCode: string): Promise<Sale> => {
    try {
      const response = await salesApiInstance.post<Sale>(`/sales/${saleId}/payment`, { payment_code: paymentCode });
      return response.data;
    } catch (error) {
      console.error('Erro ao criar pagamento:', error);
      throw error;
    }
  },

  confirmPayment: async (saleId: string): Promise<Sale> => {
    try {
      const response = await salesApiInstance.patch<Sale>(`/sales/${saleId}/payment/confirm`);
      return response.data;
    } catch (error) {
      console.error('Erro ao confirmar pagamento:', error);
      throw error;
    }
  },

  cancelPayment: async (saleId: string): Promise<Sale> => {
    try {
      const response = await salesApiInstance.patch<Sale>(`/sales/${saleId}/mark-as-canceled`);
      return response.data;
    } catch (error) {
      console.error('Erro ao cancelar pagamento:', error);
      throw error;
    }
  }
};

export const paymentsApi = {
  list: async (): Promise<Payment[]> => {
    const response = await api.get<ApiResponse<Payment[]>>('/payments');
    return response.data.data;
  },

  create: async (data: Omit<Payment, 'id' | 'created_at' | 'updated_at'>): Promise<Payment> => {
    const response = await api.post<ApiResponse<Payment>>('/payments', data);
    return response.data.data;
  },

  update: async (id: string, data: Partial<Payment>): Promise<Payment> => {
    const response = await api.put<ApiResponse<Payment>>(`/payments/${id}`, data);
    return response.data.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/payments/${id}`);
  },

  markAsPending: async (id: string): Promise<Payment> => {
    const response = await api.patch<ApiResponse<Payment>>(`/payments/${id}/status/pending`);
    return response.data.data;
  },

  markAsPaid: async (id: string): Promise<Payment> => {
    const response = await api.patch<ApiResponse<Payment>>(`/payments/${id}/status/paid`);
    return response.data.data;
  },

  markAsCancelled: async (id: string): Promise<Payment> => {
    const response = await api.patch<ApiResponse<Payment>>(`/payments/${id}/status/cancelled`);
    return response.data.data;
  },
};

export default api; 