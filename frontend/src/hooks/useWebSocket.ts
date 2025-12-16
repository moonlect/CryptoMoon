import { useEffect, useRef, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'

interface WebSocketMessage {
  type: string
  data?: any
  signal_type?: string
  signal_id?: number
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function useWebSocket(onMessage?: (message: WebSocketMessage) => void) {
  const { token, isVIP } = useAuth()
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  const pingIntervalRef = useRef<NodeJS.Timeout>()
  const onMessageRef = useRef(onMessage)

  // Update ref when callback changes (without recreating connection)
  useEffect(() => {
    onMessageRef.current = onMessage
  }, [onMessage])

  useEffect(() => {
    if (!token || !isVIP) {
      // Close existing connection if user is no longer VIP
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
        setConnected(false)
      }
      return
    }

    const connect = () => {
      // Close existing connection if any
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }

      const wsBaseUrl = API_URL.replace('http://', 'ws://').replace('https://', 'wss://')
      const wsUrl = `${wsBaseUrl}/ws/signals?token=${token}`
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        setConnected(true)
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current)
          reconnectTimeoutRef.current = undefined
        }
      }

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          // Use ref to get latest callback without recreating connection
          if (onMessageRef.current) {
            onMessageRef.current(message)
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      ws.onclose = (event) => {
        setConnected(false)
        // Don't reconnect if closed with error code (e.g., 1008 = policy violation)
        // Only reconnect on normal closure or network errors
        if (event.code !== 1008 && event.code !== 1003 && event.code !== 1011) {
          // Reconnect after 5 seconds
          reconnectTimeoutRef.current = setTimeout(connect, 5000)
        } else {
          console.warn('WebSocket closed with error code:', event.code, event.reason)
        }
      }

      wsRef.current = ws

      // Keepalive ping every 30 seconds
      pingIntervalRef.current = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'ping' }))
        }
      }, 30000)
    }

    connect()

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
        reconnectTimeoutRef.current = undefined
      }
      if (pingIntervalRef.current) {
        clearInterval(pingIntervalRef.current)
        pingIntervalRef.current = undefined
      }
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
      setConnected(false)
    }
  }, [token, isVIP]) // Remove onMessage from dependencies

  return { connected }
}

