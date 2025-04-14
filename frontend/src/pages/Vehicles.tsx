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
  MenuItem
} from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { NumericFormat } from 'react-number-format';
import vehicleService from '../services/vehicleService';
import { Vehicle, VehicleCreate, VehicleStatus } from '../types/vehicle';

const Vehicles: React.FC = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [open, setOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);
  const [formData, setFormData] = useState<VehicleCreate>({
    brand: '',
    model: '',
    year: new Date().getFullYear(),
    color: '',
    price: 0,
    status: VehicleStatus.AVAILABLE,
  });

  useEffect(() => {
    fetchVehicles();
  }, []);

  const fetchVehicles = async () => {
    try {
      const data = await vehicleService.getAll();
      setVehicles(data);
    } catch (error) {
      console.error('Erro ao buscar veículos:', error);
    }
  };

  const handleOpen = () => setOpen(true);

  const handleClose = () => {
    setOpen(false);
    setSelectedVehicle(null);
    setFormData({
      brand: '',
      model: '',
      year: new Date().getFullYear(),
      color: '',
      price: 0,
      status: VehicleStatus.AVAILABLE,
    });
  };

  const handleEdit = (vehicle: Vehicle) => {
    setSelectedVehicle(vehicle);
    setFormData({
      brand: vehicle.brand,
      model: vehicle.model,
      year: vehicle.year,
      color: vehicle.color,
      price: vehicle.price,
      status: vehicle.status,
    });
    handleOpen();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este veículo?')) {
      try {
        await vehicleService.delete(id);
        await fetchVehicles();
      } catch (error) {
        console.error('Erro ao excluir veículo:', error);
      }
    }
  };

  const handleStatusChange = async (id: string, status: VehicleStatus) => {
    try {
      await vehicleService.updateStatus(id, status);
      await fetchVehicles();
    } catch (error) {
      console.error('Erro ao atualizar status do veículo:', error);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      if (selectedVehicle) {
        if (selectedVehicle.status !== formData.status) {
          if (formData.status === VehicleStatus.RESERVED) {
            await vehicleService.markAsReserved(selectedVehicle.id);
          } else if (formData.status === VehicleStatus.AVAILABLE) {
            await vehicleService.markAsAvailable(selectedVehicle.id);
          }
        }

        const { status, ...vehicleData } = formData;
        await vehicleService.update(selectedVehicle.id, vehicleData);
      } else {
        await vehicleService.create(formData);
      }
      await fetchVehicles();
      handleClose();
    } catch (error) {
      console.error('Erro ao salvar veículo:', error);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'price' ? parseFloat(value.replace(/[^\d,]/g, '').replace(',', '.')) : value
    }));
  };

  const columns: GridColDef[] = [
    { field: 'brand', headerName: 'Marca', flex: 1 },
    { field: 'model', headerName: 'Modelo', flex: 1 },
    { field: 'year', headerName: 'Ano', width: 100 },
    { field: 'color', headerName: 'Cor', width: 120 },
    {
      field: 'price',
      headerName: 'Preço',
      width: 130,
      valueFormatter: params => {
        return new Intl.NumberFormat('pt-BR', {
          style: 'currency',
          currency: 'BRL',
        }).format(params.value);
      },
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 250,
      renderCell: params => {
        const statusColors = {
          [VehicleStatus.AVAILABLE]: '#2e7d32',
          [VehicleStatus.RESERVED]: '#ffa000',
          [VehicleStatus.SOLD]: '#d32f2f'
        };
        return (
          <Box>
            <Typography sx={{ color: statusColors[params.value as VehicleStatus] }}>
              {params.value}
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary', display: 'block' }}>
              Atualizado em: {new Date(params.row.updated_at).toLocaleString('pt-BR')}
            </Typography>
          </Box>
        );
      }
    },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 150,
      sortable: false,
      renderCell: params => {
        if (params.row.status === VehicleStatus.SOLD) {
          return null;
        }
        return (
          <Box>
            <IconButton
              onClick={() => handleEdit(params.row)}
              size="small"
              color="primary"
            >
              <EditIcon />
            </IconButton>
            <IconButton
              onClick={() => handleDelete(params.row.id)}
              size="small"
              color="error"
            >
              <DeleteIcon />
            </IconButton>
          </Box>
        );
      }
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h4">Veículos</Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleOpen}
            >
              Novo Veículo
            </Button>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ height: 600, width: '100%' }}>
            <DataGrid
              rows={vehicles}
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
                      Nenhum veículo cadastrado
                    </Typography>
                  </Box>
                )
              }}
            />
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedVehicle ? 'Editar Veículo' : 'Novo Veículo'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Marca"
                  name="brand"
                  value={formData.brand}
                  onChange={handleInputChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Modelo"
                  name="model"
                  value={formData.model}
                  onChange={handleInputChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Ano"
                  name="year"
                  type="number"
                  value={formData.year}
                  onChange={handleInputChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Cor"
                  name="color"
                  value={formData.color}
                  onChange={handleInputChange}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <NumericFormat
                  customInput={TextField}
                  fullWidth
                  label="Preço"
                  name="price"
                  value={formData.price}
                  onValueChange={(values: { floatValue?: number }) => {
                    setFormData(prev => ({
                      ...prev,
                      price: values.floatValue || 0
                    }));
                  }}
                  thousandSeparator="."
                  decimalSeparator=","
                  prefix="R$ "
                  decimalScale={2}
                  fixedDecimalScale
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  label="Status"
                  name="status"
                  value={formData.status}
                  onChange={handleInputChange}
                  required
                >
                  {Object.values(VehicleStatus)
                    .filter(status => status !== VehicleStatus.SOLD)
                    .map(status => (
                      <MenuItem key={status} value={status}>
                        {status}
                      </MenuItem>
                    ))}
                </TextField>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancelar</Button>
            <Button type="submit" variant="contained">
              Salvar
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Vehicles; 