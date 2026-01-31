import { useEffect, useState } from 'react'
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Avatar,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  People,
  VpnKey,
  Message,
  CheckCircle,
} from '@mui/icons-material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import axios from 'axios'

const StatCard = ({ title, value, change, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography color="textSecondary" variant="overline" sx={{ fontSize: 12 }}>
            {title}
          </Typography>
          <Typography variant="h4" sx={{ mt: 1, fontWeight: 600 }}>
            {value}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
            {change >= 0 ? (
              <TrendingUp sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
            ) : (
              <TrendingDown sx={{ fontSize: 16, color: 'error.main', mr: 0.5 }} />
            )}
            <Typography
              variant="body2"
              sx={{ color: change >= 0 ? 'success.main' : 'error.main' }}
            >
              {Math.abs(change)}%
            </Typography>
            <Typography variant="body2" color="textSecondary" sx={{ ml: 0.5 }}>
              Since last month
            </Typography>
          </Box>
        </Box>
        <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>
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

  const messageData = [
    { month: 'Jan', messages: 65 },
    { month: 'Feb', messages: 59 },
    { month: 'Mar', messages: 80 },
    { month: 'Apr', messages: 81 },
    { month: 'May', messages: 56 },
    { month: 'Jun', messages: 55 },
    { month: 'Jul', messages: 40 },
    { month: 'Aug', messages: 95 },
    { month: 'Sep', messages: 120 },
    { month: 'Oct', messages: 140 },
    { month: 'Nov', messages: 160 },
    { month: 'Dec', messages: 150 },
  ]

  const statusData = [
    { name: 'Success', value: 85, color: '#10B981' },
    { name: 'Pending', value: 10, color: '#F59E0B' },
    { name: 'Failed', value: 5, color: '#EF4444' },
  ]

  useEffect(() => {
    // Fetch stats from API
    const fetchStats = async () => {
      try {
        // Mock data for now
        setStats({
          partners: 12,
          keys: 24,
          messages: 1847,
          successRate: 95.5,
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }
    fetchStats()
  }, [])

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        Overview
      </Typography>

      <Grid container spacing={3}>
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
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Messages
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Sync
              </Typography>
            </Box>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={messageData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="messages" fill="#5048E5" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
              Message Status
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
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
                    <Typography variant="body2">{item.name}</Typography>
                  </Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {item.value}%
                  </Typography>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
