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
  TextField,
  InputAdornment,
  Tabs,
  Tab,
} from '@mui/material'
import {
  Visibility as VisibilityIcon,
  Search as SearchIcon,
  CheckCircle,
  Error,
  Schedule,
} from '@mui/icons-material'

export default function Messages() {
  const [messages, setMessages] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [tabValue, setTabValue] = useState(0)

  useEffect(() => {
    fetchMessages()
  }, [])

  const fetchMessages = async () => {
    try {
      // Mock data - replace with actual API call
      const mockMessages = [
        {
          id: 1,
          message_id: 'MSG-2026-001',
          direction: 'outbound',
          partner: 'P2',
          status: 'success',
          timestamp: '2026-01-31 10:30:00',
          size: '2.5 MB',
        },
        {
          id: 2,
          message_id: 'MSG-2026-002',
          direction: 'inbound',
          partner: 'P1',
          status: 'success',
          timestamp: '2026-01-31 10:25:00',
          size: '1.8 MB',
        },
        {
          id: 3,
          message_id: 'MSG-2026-003',
          direction: 'outbound',
          partner: 'Partner A',
          status: 'pending',
          timestamp: '2026-01-31 10:20:00',
          size: '3.2 MB',
        },
        {
          id: 4,
          message_id: 'MSG-2026-004',
          direction: 'inbound',
          partner: 'Partner B',
          status: 'failed',
          timestamp: '2026-01-31 10:15:00',
          size: '1.2 MB',
        },
        {
          id: 5,
          message_id: 'MSG-2026-005',
          direction: 'outbound',
          partner: 'P2',
          status: 'success',
          timestamp: '2026-01-31 10:10:00',
          size: '4.1 MB',
        },
      ]
      setMessages(mockMessages)
    } catch (error) {
      console.error('Error fetching messages:', error)
    }
  }

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue)
  }

  const getFilteredMessages = () => {
    let filtered = messages.filter(
      (msg) =>
        msg.message_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        msg.partner.toLowerCase().includes(searchTerm.toLowerCase())
    )

    if (tabValue === 1) {
      filtered = filtered.filter((msg) => msg.direction === 'inbound')
    } else if (tabValue === 2) {
      filtered = filtered.filter((msg) => msg.direction === 'outbound')
    }

    return filtered
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'success'
      case 'pending':
        return 'warning'
      case 'failed':
        return 'error'
      default:
        return 'default'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle />
      case 'pending':
        return <Schedule />
      case 'failed':
        return <Error />
      default:
        return null
    }
  }

  const getDirectionColor = (direction) => {
    return direction === 'inbound' ? '#10B981' : '#5048E5'
  }

  const filteredMessages = getFilteredMessages()

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Messages
      </Typography>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="All Messages" />
            <Tab label="Inbound" />
            <Tab label="Outbound" />
          </Tabs>
        </Box>

        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            placeholder="Search messages..."
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
                <TableCell>Message ID</TableCell>
                <TableCell>Direction</TableCell>
                <TableCell>Partner</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Size</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredMessages.map((message) => (
                <TableRow key={message.id} hover>
                  <TableCell>
                    <Typography
                      variant="body2"
                      sx={{ fontFamily: 'monospace', fontWeight: 500 }}
                    >
                      {message.message_id}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={message.direction}
                      size="small"
                      sx={{
                        bgcolor: getDirectionColor(message.direction),
                        color: 'white',
                        fontWeight: 500,
                        textTransform: 'capitalize',
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{message.partner}</Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={message.status}
                      color={getStatusColor(message.status)}
                      size="small"
                      icon={getStatusIcon(message.status)}
                      sx={{ textTransform: 'capitalize' }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="textSecondary">
                      {message.timestamp}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">{message.size}</Typography>
                  </TableCell>
                  <TableCell align="right">
                    <IconButton size="small" color="primary">
                      <VisibilityIcon fontSize="small" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {filteredMessages.length === 0 && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography color="textSecondary">No messages found</Typography>
          </Box>
        )}
      </Paper>
    </Box>
  )
}
