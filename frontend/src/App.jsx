import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Partners from './pages/Partners'
import Keys from './pages/Keys'
import Messages from './pages/Messages'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#5048E5',
    },
    secondary: {
      main: '#10B981',
    },
    background: {
      default: '#F9FAFC',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  shape: {
    borderRadius: 8,
  },
})

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/partners" element={<Partners />} />
            <Route path="/keys" element={<Keys />} />
            <Route path="/messages" element={<Messages />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  )
}

export default App
