import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState, useEffect } from 'react'
import api from '../lib/api'
import { useWebSocket } from '../hooks/useWebSocket'
import { ExternalLink, Trash2 } from 'lucide-react'

interface Signal {
  id: number
  coin_name: string
  position: string
  spread: number
  mexc_spot_price: number
  mexc_futures_price: number
  spot_url: string
  futures_url: string
  deposit_enabled: boolean
  withdrawal_enabled: boolean
  dex_url: string
  created_at: string
}

export default function MEXCSpotFutures() {
  const [minSpread, setMinSpread] = useState('')
  const [position, setPosition] = useState('ALL')
  const [search, setSearch] = useState('')
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['mexc-signals', minSpread, position, search],
    queryFn: async () => {
      const params = new URLSearchParams({
        limit: '30',
        offset: '0',
      })
      if (minSpread) params.append('min_spread', minSpread)
      if (position !== 'ALL') params.append('position', position)
      if (search) params.append('search', search)
      const response = await api.get(`/api/v1/signals/mexc-spot-futures?${params}`)
      return response.data
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/api/v1/signals/${id}?signal_type=mexc_spot_futures`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mexc-signals'] })
    },
  })

  // WebSocket for real-time updates
  useWebSocket((message) => {
    if (message.type === 'new_signal' && message.signal_type === 'mexc_spot_futures') {
      queryClient.invalidateQueries({ queryKey: ['mexc-signals'] })
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">MEXC Spot & Futures</h1>
        <p className="mt-2 text-sm text-gray-600">Arbitrage opportunities between MEXC Spot and Futures</p>
      </div>

      <div className="mb-4 flex gap-4 flex-wrap">
        <input
          type="number"
          placeholder="Min spread %"
          value={minSpread}
          onChange={(e) => setMinSpread(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md"
        />
        <select
          value={position}
          onChange={(e) => setPosition(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md"
        >
          <option value="ALL">All Positions</option>
          <option value="LONG">LONG</option>
          <option value="SHORT">SHORT</option>
        </select>
        <input
          type="text"
          placeholder="Search coin..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md flex-1"
        />
      </div>

      {isLoading && <div className="text-center py-8">Loading...</div>}

      {data && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.data.map((signal: Signal) => (
            <div key={signal.id} className="bg-white rounded-lg shadow p-6 border border-gray-200">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{signal.coin_name}</h3>
                  <span
                    className={`inline-block mt-1 px-2 py-1 text-xs font-semibold rounded ${
                      signal.position === 'LONG'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {signal.position}
                  </span>
                </div>
                <button
                  onClick={() => deleteMutation.mutate(signal.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-2 mb-4">
                <div className="flex justify-between">
                  <span className="text-gray-600">Spread:</span>
                  <span className="font-semibold text-green-600">{signal.spread}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Spot Price:</span>
                  <span className="font-medium">${signal.mexc_spot_price}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Futures Price:</span>
                  <span className="font-medium">${signal.mexc_futures_price}</span>
                </div>
                <div className="flex gap-2 mt-2">
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      signal.deposit_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {signal.deposit_enabled ? '✅ Deposit' : '❌ Deposit'}
                  </span>
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      signal.withdrawal_enabled
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {signal.withdrawal_enabled ? '✅ Withdraw' : '❌ Withdraw'}
                  </span>
                </div>
              </div>

              <div className="flex gap-2">
                {signal.spot_url && (
                  <a
                    href={signal.spot_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center px-3 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 text-sm"
                  >
                    <ExternalLink className="w-4 h-4 inline mr-1" />
                    Spot
                  </a>
                )}
                {signal.futures_url && (
                  <a
                    href={signal.futures_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center px-3 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 text-sm"
                  >
                    <ExternalLink className="w-4 h-4 inline mr-1" />
                    Futures
                  </a>
                )}
                {signal.dex_url && (
                  <a
                    href={signal.dex_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center px-3 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 text-sm"
                  >
                    <ExternalLink className="w-4 h-4 inline mr-1" />
                    DEX
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {data && data.data.length === 0 && (
        <div className="text-center py-8 text-gray-500">No signals found</div>
      )}
    </div>
  )
}



