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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Divider,
  CircularProgress,
} from '@mui/material'
import {
  Visibility as VisibilityIcon,
  Search as SearchIcon,
  CheckCircle,
  Error,
  Schedule,
  Close as CloseIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material'
import axios from 'axios'

export default function Messages() {
  const [messages, setMessages] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [tabValue, setTabValue] = useState(0)
  const [openDialog, setOpenDialog] = useState(false)
  const [selectedMessage, setSelectedMessage] = useState(null)
  const [loadingDetail, setLoadingDetail] = useState(false)
  const [retrying, setRetrying] = useState(false)

  useEffect(() => {
    fetchMessages()
  }, [])

  const fetchMessages = async () => {
    try {
      const response = await axios.get('/api/messages/')
      setMessages(response.data.messages || [])
    } catch (error) {
      console.error('Error fetching messages:', error)
      // Use mock data as fallback
      const mockMessages = [
        {
          id: 1,
          message_id: 'MSG-2026-001',
          direction: 'OUT',
          partner: 'P2',
          status: 'success',
          timestamp: '2026-01-31 10:30:00',
          size: '2.5 KB',
        },
      ]
      setMessages(mockMessages)
    }
  }

  const handleViewMessage = async (messageId) => {
    setLoadingDetail(true)
    setOpenDialog(true)
    
    try {
      const response = await axios.get(`/api/messages/${messageId}/`)
      setSelectedMessage(response.data)
    } catch (error) {
      console.error('Error fetching message details:', error)
      setSelectedMessage({
        error: 'Failed to load message details'
      })
    } finally {
      setLoadingDetail(false)
    }
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setSelectedMessage(null)
  }

  const handleRetryMessage = async (messageId) => {
    if (!window.confirm('Are you sure you want to retry this message?')) {
      return
    }
    
    setRetrying(true)
    try {
      const response = await axios.post(`/api/messages/${messageId}/retry/`)
      
      if (response.data.success) {
        alert('Message retried successfully!')
        // Refresh messages list
        fetchMessages()
        handleCloseDialog()
      } else {
        alert(`Failed to retry message: ${response.data.error}`)
      }
    } catch (error) {
      console.error('Error retrying message:', error)
      alert(`Error retrying message: ${error.response?.data?.error || error.message}`)
    } finally {
      setRetrying(false)
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
      filtered = filtered.filter((msg) => msg.direction === 'IN')
    } else if (tabValue === 2) {
      filtered = filtered.filter((msg) => msg.direction === 'OUT')
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
    return direction === 'IN' ? '#10B981' : '#5048E5'
  }

  const getDirectionLabel = (direction) => {
    return direction === 'IN' ? 'Inbound' : 'Outbound'
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
                      label={getDirectionLabel(message.direction)}
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
                    <IconButton 
                      size="small" 
                      color="primary"
                      onClick={() => handleViewMessage(message.id)}
                      title="View message details"
                    >
                      <VisibilityIcon fontSize="small" />
                    </IconButton>
                    {message.status === 'failed' && message.direction === 'OUT' && (
                      <IconButton 
                        size="small" 
                        color="warning"
                        onClick={() => handleRetryMessage(message.id)}
                        title="Retry failed message"
                      >
                        <RefreshIcon fontSize="small" />
                      </IconButton>
                    )}
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

      {/* Message Detail Dialog */}
      <Dialog 
        open={openDialog} 
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">Message Details</Typography>
          <IconButton onClick={handleCloseDialog} size="small">
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {loadingDetail ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : selectedMessage && !selectedMessage.error ? (
            <Box>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Message ID
                  </Typography>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', fontWeight: 500 }}>
                    {selectedMessage.message_id}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Direction
                  </Typography>
                  <Typography variant="body2">
                    <Chip
                      label={selectedMessage.direction}
                      size="small"
                      sx={{
                        bgcolor: selectedMessage.direction === 'Inbound' ? '#10B981' : '#5048E5',
                        color: 'white',
                        fontWeight: 500,
                      }}
                    />
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Partner
                  </Typography>
                  <Typography variant="body2">{selectedMessage.partner}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Status
                  </Typography>
                  <Typography variant="body2">
                    <Chip
                      label={selectedMessage.status}
                      size="small"
                      color={
                        selectedMessage.status === 'Success' ? 'success' :
                        selectedMessage.status === 'Pending' ? 'warning' : 'error'
                      }
                    />
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Timestamp
                  </Typography>
                  <Typography variant="body2">{selectedMessage.timestamp}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Size
                  </Typography>
                  <Typography variant="body2">{selectedMessage.size}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Filename
                  </Typography>
                  <Typography variant="body2">{selectedMessage.filename}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="textSecondary">
                    Content Type
                  </Typography>
                  <Typography variant="body2">{selectedMessage.content_type}</Typography>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                Payload Content
              </Typography>
              <Paper
                variant="outlined"
                sx={{
                  p: 2,
                  bgcolor: '#f5f5f5',
                  maxHeight: 400,
                  overflow: 'auto',
                  fontFamily: 'monospace',
                  fontSize: 12,
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                }}
              >
                {selectedMessage.payload || '[No payload content]'}
              </Paper>
            </Box>
          ) : (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography color="error">
                {selectedMessage?.error || 'Failed to load message details'}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          {selectedMessage && selectedMessage.status === 'Failed' && selectedMessage.direction === 'Outbound' && (
            <Button 
              onClick={() => handleRetryMessage(selectedMessage.id)}
              color="warning"
              variant="contained"
              startIcon={<RefreshIcon />}
              disabled={retrying}
            >
              {retrying ? 'Retrying...' : 'Retry Message'}
            </Button>
          )}
          <Button onClick={handleCloseDialog}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
