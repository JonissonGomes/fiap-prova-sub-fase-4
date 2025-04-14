import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  Paper,
  TextField,
  Typography,
  IconButton,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Alert,
  Snackbar
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { Payment, Sale, Vehicle } from '../types';
import { PaymentStatus } from '../types/payment';
import { salesApi, vehiclesApi } from '../services/api';

const Payments: React.FC = () => {
  const [sales, setSales] = useState<Sale[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedSale, setSelectedSale] = useState<Sale | null>(null);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success'
  });

  useEffect(() => {
    fetchSales();
    fetchVehicles();
  }, []);

  const fetchSales = async () => {
    try {
      const data = await salesApi.list();
      // Filtrar apenas vendas que não estão canceladas
      const activeSales = data.filter(sale => sale.payment_status !== PaymentStatus.CANCELLED);
      setSales(activeSales);
    } catch (error) {
      console.error('Error fetching sales:', error);
    }
  };

  const fetchVehicles = async () => {
    try {
      const data = await vehiclesApi.list();
      setVehicles(data);
    } catch (error) {
      console.error('Error fetching vehicles:', error);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const handleStatusChange = async (saleId: string, status: PaymentStatus) => {
    try {
      const sale = sales.find(s => s.id === saleId);
      if (!sale) return;

      switch (status) {
        case PaymentStatus.PAID:
          // Notificar webhook de pagamento
          await salesApi.notifyPaymentWebhook(sale.payment_code, 'PAGO', sale.vehicle_id);
          await vehiclesApi.markAsSold(sale.vehicle_id);
          break;
        case PaymentStatus.CANCELLED:
          await salesApi.cancelPayment(saleId);
          await vehiclesApi.markAsAvailable(sale.vehicle_id);
          break;
      }
      
      setSnackbar({
        open: true,
        message: 'Status atualizado com sucesso',
        severity: 'success'
      });
      
      setTimeout(() => {
        fetchSales();
        fetchVehicles();
      }, 500);
    } catch (error) {
      console.error('Error updating sale status:', error);
    }
  };

  const columns: GridColDef[] = [
    {
      field: 'vehicle_id',
      headerName: 'Veículo',
      width: 300,
      valueGetter: (params) => {
        const vehicle = vehicles.find(v => v.id === params.row.vehicle_id);
        return vehicle ? `${vehicle.brand} ${vehicle.model} - ${vehicle.year}` : 'Veículo não encontrado';
      }
    },
    { field: 'buyer_cpf', headerName: 'CPF do Cliente', width: 150 },
    {
      field: 'sale_price',
      headerName: 'Valor',
      width: 150,
      valueFormatter: (params) => formatCurrency(params.value)
    },
    { field: 'payment_code', headerName: 'Código de Pagamento', width: 200 },
    {
      field: 'payment_status',
      headerName: 'Status do pagamento',
      width: 150,
      renderCell: (params) => {
        const statusColors = {
          [PaymentStatus.PENDING]: '#ed6c02',
          [PaymentStatus.PAID]: '#2e7d32',
          [PaymentStatus.CANCELLED]: '#d32f2f'
        };
        return (
          <Typography sx={{ color: statusColors[params.value as PaymentStatus] }}>
            {params.value}
          </Typography>
        );
      }
    },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 200,
      renderCell: (params) => (
        <Box>
          {params.row.payment_status === PaymentStatus.PENDING && (
            <>
              <Button
                variant="outlined"
                size="small"
                onClick={() => handleStatusChange(params.row.id, PaymentStatus.PAID)}
                sx={{ mr: 1 }}
              >
                Pagar
              </Button>
              <Button
                variant="outlined"
                size="small"
                onClick={() => handleStatusChange(params.row.id, PaymentStatus.CANCELLED)}
                color="error"
              >
                Cancelar
              </Button>
            </>
          )}
        </Box>
      )
    }
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h4">Pagamentos</Typography>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ height: 600, width: '100%' }}>
            <DataGrid
              rows={sales}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: { pageSize: 10 }
                }
              }}
              pageSizeOptions={[10]}
              disableRowSelectionOnClick
              slots={{
                noRowsOverlay: () => (
                  <Box
                    sx={{
                      height: '100%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}
                  >
                    <Typography variant="body1" color="text.secondary">
                      Não há pagamentos pendentes
                    </Typography>
                  </Box>
                )
              }}
            />
          </Paper>
        </Grid>
      </Grid>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Payments; 