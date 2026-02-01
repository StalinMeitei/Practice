import { useEffect, useState } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Avatar,
  ToggleButton,
  ToggleButtonGroup,
  CircularProgress,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  People,
  VpnKey,
  Message,
  CheckCircle,
  ShowChart,
  GridOn,
} from '@mui/icons-material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, Legend } from 'recharts'
import axios from 'axios'
import MessageHeatmap from '../components/MessageHeatmap'

const StatCard = ({ title, value, change, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box sx={{ flex: 1 }}>
          <Typography color="textSecondary" variant="overline" sx={{ fontSize: 11, lineHeight: 1.2 }}>
            {title}
          </Typography>
          <Typography variant="h5" sx={{ mt: 0.5, mb: 0.5, fontWeight: 600 }}>
            {value}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {change >= 0 ? (
              <TrendingUp sx={{ fontSize: 14, color: 'success.main', mr: 0.5 }} />
            ) : (
              <TrendingDown sx={{ fontSize: 14, color: 'error.main', mr: 0.5 }} />
            )}
            <Typography
              variant="body2"
              sx={{ color: change >= 0 ? 'success.main' : 'error.main', fontSize: 12 }}
            >
              {Math.abs(change)}%
            </Typography>
          </Box>
        </Box>
        <Avatar sx={{ bgcolor: color, width: 40, height: 40 }}>
          {icon}
        </Avatar>
      </Box>
    </CardContent>
  </Card>
)

export default function Dashboard() {
  const [stats, setStats] = useState({
    partners: 0,
    keys: 0,
    messages: 0,
    successRate: 0,
  })

  const [messageData, setMessageData] = useState([])
  const [statusData, setStatusData] = useState([])
  const [trendData, setTrendData] = useState([])
  const [heatmapData, setHeatmapData] = useState([])
  const [loading, setLoading] = useState(true)
  const [heatmapLoading, setHeatmapLoading] = useState(false)
  const [chartView, setChartView] = useState('line') // 'line' or 'heatmap'
  const [heatmapGranularity, setHeatmapGranularity] = useState('weekly') // 'hourly', 'daily', 'weekly', 'monthly', 'yearly'

  const handleChartViewChange = (event, newView) => {
    if (newView !== null) {
      setChartView(newView)
    }
  }

  const handleGranularityChange = (event, newGranularity) => {
    if (newGranularity !== null) {
      setHeatmapGranularity(newGranularity)
      // Fetch new data for the selected granularity
      fetchHeatmapData(newGranularity)
    }
  }

  const fetchHeatmapData = async (granularity) => {
    try {
      setHeatmapLoading(true)
      const response = await axios.get(`/api/heatmap-data/?granularity=${granularity}`)
      setHeatmapData(response.data.heatmapData)
    } catch (error) {
      console.error('Error fetching heatmap data:', error)
      setHeatmapData([])
    } finally {
      setHeatmapLoading(false)
    }
  }

  useEffect(() => {
    // Fetch stats and chart data from API
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Fetch stats
        const statsResponse = await axios.get('/api/stats/')
        setStats(statsResponse.data)
        
        // Fetch chart data
        const chartResponse = await axios.get('/api/chart-data/')
        setMessageData(chartResponse.data.messageData)
        setStatusData(chartResponse.data.statusData)
        setTrendData(chartResponse.data.trendData)
        
        // Fetch heatmap data (default weekly)
        await fetchHeatmapData('weekly')
      } catch (error) {
        console.error('Error fetching data:', error)
        // Use empty data if API fails
        setMessageData([
          { month: 'Jan', messages: 0 },
          { month: 'Feb', messages: 0 },
          { month: 'Mar', messages: 0 },
          { month: 'Apr', messages: 0 },
          { month: 'May', messages: 0 },
          { month: 'Jun', messages: 0 },
          { month: 'Jul', messages: 0 },
          { month: 'Aug', messages: 0 },
          { month: 'Sep', messages: 0 },
          { month: 'Oct', messages: 0 },
          { month: 'Nov', messages: 0 },
          { month: 'Dec', messages: 0 },
        ])
        setStatusData([
          { name: 'Success', value: 0, count: 0, color: '#10B981' },
          { name: 'Pending', value: 0, count: 0, color: '#F59E0B' },
          { name: 'Failed', value: 0, count: 0, color: '#EF4444' },
        ])
        setTrendData([
          { month: 'Jan', sent: 0, received: 0, failed: 0 },
          { month: 'Feb', sent: 0, received: 0, failed: 0 },
          { month: 'Mar', sent: 0, received: 0, failed: 0 },
          { month: 'Apr', sent: 0, received: 0, failed: 0 },
          { month: 'May', sent: 0, received: 0, failed: 0 },
          { month: 'Jun', sent: 0, received: 0, failed: 0 },
          { month: 'Jul', sent: 0, received: 0, failed: 0 },
          { month: 'Aug', sent: 0, received: 0, failed: 0 },
          { month: 'Sep', sent: 0, received: 0, failed: 0 },
          { month: 'Oct', sent: 0, received: 0, failed: 0 },
          { month: 'Nov', sent: 0, received: 0, failed: 0 },
          { month: 'Dec', sent: 0, received: 0, failed: 0 },
        ])
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
        Overview
      </Typography>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
          <Typography variant="body1" color="textSecondary">Loading dashboard data...</Typography>
        </Box>
      ) : (
        <Grid container spacing={2}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="TOTAL PARTNERS"
            value={stats.partners}
            change={12}
            icon={<People />}
            color="#10B981"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="ACTIVE KEYS"
            value={stats.keys}
            change={8}
            icon={<VpnKey />}
            color="#F59E0B"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="MESSAGES"
            value={stats.messages}
            change={-5}
            icon={<Message />}
            color="#5048E5"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="SUCCESS RATE"
            value={`${stats.successRate}%`}
            change={2.5}
            icon={<CheckCircle />}
            color="#06B6D4"
          />
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, fontSize: 16 }}>
                Messages
              </Typography>
            </Box>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={messageData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" style={{ fontSize: 12 }} />
                <YAxis style={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="messages" fill="#5048E5" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, fontSize: 16 }}>
              Message Status
            </Typography>
            <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value, name, props) => {
                      const count = props.payload.count || 0
                      return [`${value}% (${count} messages)`, props.payload.name]
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <Box sx={{ mt: 2 }}>
                {statusData.map((item) => (
                  <Box
                    key={item.name}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      mb: 1,
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          bgcolor: item.color,
                          mr: 1,
                        }}
                      />
                      <Typography variant="body2" sx={{ fontSize: 13 }}>{item.name}</Typography>
                    </Box>
                    <Typography variant="body2" sx={{ fontWeight: 600, fontSize: 13 }}>
                      {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, fontSize: 16 }}>
                Message Trends
              </Typography>
              <ToggleButtonGroup
                value={chartView}
                exclusive
                onChange={handleChartViewChange}
                size="small"
                sx={{ height: 32 }}
              >
                <ToggleButton value="line" sx={{ px: 2, textTransform: 'none' }}>
                  <ShowChart sx={{ fontSize: 18, mr: 0.5 }} />
                  Line Chart
                </ToggleButton>
                <ToggleButton value="heatmap" sx={{ px: 2, textTransform: 'none' }}>
                  <GridOn sx={{ fontSize: 18, mr: 0.5 }} />
                  Heatmap
                </ToggleButton>
              </ToggleButtonGroup>
            </Box>
            
            {chartView === 'line' ? (
              <>
                <Typography variant="body2" color="textSecondary" sx={{ fontSize: 12, mb: 2 }}>
                  Last 12 months
                </Typography>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="month" style={{ fontSize: 12 }} />
                    <YAxis style={{ fontSize: 12 }} />
                    <Tooltip />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                    <Line 
                      type="monotone" 
                      dataKey="sent" 
                      stroke="#5048E5" 
                      strokeWidth={2}
                      dot={{ r: 3 }}
                      activeDot={{ r: 5 }}
                      name="Sent"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="received" 
                      stroke="#10B981" 
                      strokeWidth={2}
                      dot={{ r: 3 }}
                      activeDot={{ r: 5 }}
                      name="Received"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="failed" 
                      stroke="#EF4444" 
                      strokeWidth={2}
                      dot={{ r: 3 }}
                      activeDot={{ r: 5 }}
                      name="Failed"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </>
            ) : (
              <Box sx={{ mt: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="body2" color="textSecondary" sx={{ fontSize: 11 }}>
                    Success rate by time period - Green indicates high success, Red indicates failures
                  </Typography>
                  <ToggleButtonGroup
                    value={heatmapGranularity}
                    exclusive
                    onChange={handleGranularityChange}
                    size="small"
                    sx={{ height: 28 }}
                    disabled={heatmapLoading}
                  >
                    <ToggleButton value="hourly" sx={{ px: 1.5, py: 0.5, textTransform: 'none', fontSize: 11 }}>
                      Hourly
                    </ToggleButton>
                    <ToggleButton value="daily" sx={{ px: 1.5, py: 0.5, textTransform: 'none', fontSize: 11 }}>
                      Daily
                    </ToggleButton>
                    <ToggleButton value="weekly" sx={{ px: 1.5, py: 0.5, textTransform: 'none', fontSize: 11 }}>
                      Weekly
                    </ToggleButton>
                    <ToggleButton value="monthly" sx={{ px: 1.5, py: 0.5, textTransform: 'none', fontSize: 11 }}>
                      Monthly
                    </ToggleButton>
                    <ToggleButton value="yearly" sx={{ px: 1.5, py: 0.5, textTransform: 'none', fontSize: 11 }}>
                      Yearly
                    </ToggleButton>
                  </ToggleButtonGroup>
                </Box>
                {heatmapLoading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 300 }}>
                    <CircularProgress size={40} />
                  </Box>
                ) : (
                  <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                    <MessageHeatmap data={heatmapData} width={900} height={300} granularity={heatmapGranularity} />
                  </Box>
                )}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
      )}
    </Box>
  )
}
