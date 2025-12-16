import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { ReactNode } from 'react'

interface VIPRouteProps {
  children: ReactNode
}

export default function VIPRoute({ children }: VIPRouteProps) {
  const { isAuthenticated, isVIP } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (!isVIP) {
    return <Navigate to="/pricing" replace />
  }

  return <>{children}</>
}



