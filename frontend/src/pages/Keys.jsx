import { useEffect, useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Button,
  TextField,
  InputAdornment,
  Card,
  CardContent,
  Grid,
} from '@mui/material'
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Add as AddIcon,
  VpnKey,
  Lock,
  LockOpen,
  Download,
} from '@mui/icons-material'

export default function Keys() {
  const [keys, setKeys] = useState([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchKeys()
  }, [])

  const fetchKeys = async () => {
    try {
      // Mock data - replace with actual API call
      const mockKeys = [
        {
          id: 1,
          name: 'P1 Private Key',
          type: 'Private',
          algorithm: 'RSA 2048',
          organization: 'P1 Organization',
          expires: '2027-01-20',
          status: 'active',
          fingerprint: 'A1:B2:C3:D4:E5:F6',
        },
        {
          id: 2,
          name: 'P1 Public Certificate',
          type: 'Public',
          algorithm: 'RSA 2048',
          organization: 'P1 Organization',
          expires: '2027-01-20',
          status: 'active',
          fingerprint: 'A1:B2:C3:D4:E5:F6',
        },
        {
          id: 3,
          name: 'P2 Private Key',
          type: 'Private',
          algorithm: 'RSA 2048',
          organization: 'P2 Organization',
          expires: '2027-01-20',
          status: 'active',
          fingerprint: 'B2:C3:D4:E5:F6:A1',
        },
        {
          id: 4,
          name: 'P2 Public Certificate',
          type: 'Public',
          algorithm: 'RSA 2048',
          organization: 'P2 Organization',
          expires: '2027-01-20',
          status: 'active',
          fingerprint: 'B2:C3:D4:E5:F6:A1',
        },
        {
          id: 5,
          name: 'Partner A Certificate',
          type: 'Public',
          algorithm: 'RSA 4096',
          organization: 'Partner A Corp',
          expires: '2026-06-15',
          status: 'expiring',
          fingerprint: 'C3:D4:E5:F6:A1:B2',
        },
      ]
      setKeys(mockKeys)
    } catch (error) {
      console.error('Error fetching keys:', error)
    }
  }

  const filteredKeys = keys.filter(
    (key) =>
      key.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      key.organization.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success'
      case 'expiring':
        return 'warning'
      case 'expired':
        return 'error'
      default:
        return 'default'
    }
  }

  const getTypeIcon = (type) => {
    return type === 'Private' ? <Lock /> : <LockOpen />
  }

  const getTypeColor = (type) => {
    return type === 'Private' ? '#EF4444' : '#10B981'
  }

  const keyStats = {
    total: keys.length,
    private: keys.filter((k) => k.type === 'Private').length,
    public: keys.filter((k) => k.type === 'Public').length,
    expiring: keys.filter((k) => k.status === 'expiring').length,
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          Keys & Certificates
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          sx={{ textTransform: 'none' }}
        >
          Add Key
        </Button>
      </Box>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 1,
                    bgcolor: '#5048E5',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  <VpnKey />
                </Box>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {keyStats.total}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Total Keys
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 1,
                    bgcolor: '#EF4444',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  <Lock />
                </Box>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {keyStats.private}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Private Keys
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 1,
                    bgcolor: '#10B981',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  <LockOpen />
                </Box>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {keyStats.public}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Public Certificates
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 1,
                    bgcolor: '#F59E0B',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  <VpnKey />
                </Box>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {keyStats.expiring}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Expiring Soon
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            placeholder="Search keys..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Key Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Algorithm</TableCell>
                <TableCell>Organization</TableCell>
                <TableCell>Expires</TableCell>
                <TableCell>Fingerprint</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredKeys.map((key) => (
                <TableRow key={key.id} hover>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Box
                        sx={{
                          width: 32,
                          height: 32,
                          borderRadius: 1,
                          bgcolor: getTypeColor(key.type),
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white',
                        }}
                      >
                        {getTypeIcon(key.type)}
                      </Box>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {key.name}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={key.type}
                      size="small"
                      sx={{
                        bgcolor: getTypeColor(key.type),
                        color: 'white',
                        fontWeight: 500,
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{key.algorithm}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="textSecondary">
                      {key.organization}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{key.expires}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography
                      variant="body2"
                      sx={{ fontFamily: 'monospace', fontSize: 11 }}
                    >
                      {key.fingerprint}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={key.status}
                      color={getStatusColor(key.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="right">
                    <IconButton size="small" color="primary">
                      <Download fontSize="small" />
                    </IconButton>
                    <IconButton size="small" color="primary">
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton size="small" color="error">
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {filteredKeys.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography color="textSecondary">No keys found</Typography>
          </Box>
        )}
      </Paper>
    </Box>
  )
}
