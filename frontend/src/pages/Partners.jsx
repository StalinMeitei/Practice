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
  Avatar,
  IconButton,
  Button,
  TextField,
  InputAdornment,
} from '@mui/material'
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Add as AddIcon,
  CheckCircle,
  Cancel,
} from '@mui/icons-material'
import axios from 'axios'

export default function Partners() {
  const [partners, setPartners] = useState([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchPartners()
  }, [])

  const fetchPartners = async () => {
    try {
      // Mock data - replace with actual API call
      const mockPartners = [
        {
          id: 1,
          as2_name: 'P1',
          name: 'P1 Organization',
          target_url: 'http://p1:8000/pyas2/as2receive',
          encryption: 'tripledes_192_cbc',
          signature: 'sha256',
          status: 'active',
        },
        {
          id: 2,
          as2_name: 'P2',
          name: 'P2 Organization',
          target_url: 'http://p2:8002/pyas2/as2receive',
          encryption: 'tripledes_192_cbc',
          signature: 'sha256',
          status: 'active',
        },
        {
          id: 3,
          as2_name: 'PARTNER_A',
          name: 'Partner A Corp',
          target_url: 'https://partner-a.com/as2',
          encryption: 'aes_256_cbc',
          signature: 'sha512',
          status: 'active',
        },
        {
          id: 4,
          as2_name: 'PARTNER_B',
          name: 'Partner B Inc',
          target_url: 'https://partner-b.com/as2',
          encryption: 'aes_128_cbc',
          signature: 'sha256',
          status: 'inactive',
        },
      ]
      setPartners(mockPartners)
    } catch (error) {
      console.error('Error fetching partners:', error)
    }
  }

  const filteredPartners = partners.filter(
    (partner) =>
      partner.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      partner.as2_name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const getStatusColor = (status) => {
    return status === 'active' ? 'success' : 'default'
  }

  const getInitials = (name) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 600 }}>
          Partners
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          sx={{ textTransform: 'none' }}
        >
          Add Partner
        </Button>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            placeholder="Search partners..."
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
                <TableCell>Partner</TableCell>
                <TableCell>AS2 Name</TableCell>
                <TableCell>Target URL</TableCell>
                <TableCell>Encryption</TableCell>
                <TableCell>Signature</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredPartners.map((partner) => (
                <TableRow key={partner.id} hover>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Avatar sx={{ bgcolor: '#5048E5' }}>
                        {getInitials(partner.name)}
                      </Avatar>
                      <Typography variant="body2" sx={{ fontWeight: 500 }}>
                        {partner.name}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={partner.as2_name}
                      size="small"
                      sx={{ fontWeight: 500 }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="textSecondary">
                      {partner.target_url}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{partner.encryption}</Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{partner.signature}</Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={partner.status}
                      color={getStatusColor(partner.status)}
                      size="small"
                      icon={partner.status === 'active' ? <CheckCircle /> : <Cancel />}
                    />
                  </TableCell>
                  <TableCell align="right">
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

        {filteredPartners.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography color="textSecondary">No partners found</Typography>
          </Box>
        )}
      </Paper>
    </Box>
  )
}
