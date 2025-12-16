import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import LandingPage from './pages/LandingPage'
import MarketData from './pages/MarketData'
import MEXCSpotFutures from './pages/MEXCSpotFutures'
import FundingRate from './pages/FundingRate'
import MEXCDEX from './pages/MEXCDEX'
import Login from './pages/Login'
import Register from './pages/Register'
import Profile from './pages/Profile'
import Pricing from './pages/Pricing'
import ProtectedRoute from './components/ProtectedRoute'
import VIPRoute from './components/VIPRoute'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<LandingPage />} />
            <Route path="market" element={<MarketData />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="pricing" element={<Pricing />} />
            <Route
              path="mexc-spot-futures"
              element={
                <VIPRoute>
                  <MEXCSpotFutures />
                </VIPRoute>
              }
            />
            <Route
              path="funding-rate"
              element={
                <VIPRoute>
                  <FundingRate />
                </VIPRoute>
              }
            />
            <Route
              path="mexc-dex"
              element={
                <VIPRoute>
                  <MEXCDEX />
                </VIPRoute>
              }
            />
            <Route
              path="profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App



