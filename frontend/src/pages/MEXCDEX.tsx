import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../lib/api'
import { useWebSocket } from '../hooks/useWebSocket'
import { ExternalLink, Trash2 } from 'lucide-react'

interface Signal {
  id: number
  coin_name: string
  spread_percent: number
  mexc_price: number
  dex_price: number
  mexc_url: string
  dexscreener_url: string
  max_size_usd: number
  deposit_enabled: boolean
  withdrawal_enabled: boolean
  deposit_url?: string
  withdrawal_url?: string
  token_contract?: string
  token_chain?: string
  created_at: string
}

export default function MEXCDEX() {
  const [minSpread, setMinSpread] = useState('')
  const [search, setSearch] = useState('')
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['mexc-dex', minSpread, search],
    queryFn: async () => {
      const params = new URLSearchParams({ limit: '30', offset: '0' })
      if (minSpread) params.append('min_spread', minSpread)
      if (search) params.append('search', search)
      const response = await api.get(`/api/v1/signals/mexc-dex?${params}`)
      return response.data
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/api/v1/signals/${id}?signal_type=mexc_dex`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mexc-dex'] })
    },
  })

  useWebSocket((message) => {
    if (message.type === 'new_signal' && message.signal_type === 'mexc_dex') {
      queryClient.invalidateQueries({ queryKey: ['mexc-dex'] })
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">MEXC & DEX Price Spread</h1>
        <p className="mt-2 text-sm text-gray-600">Arbitrage opportunities between MEXC and DEX</p>
      </div>

      <div className="mb-4 flex gap-4">
        <input
          type="number"
          placeholder="Min spread %"
          value={minSpread}
          onChange={(e) => setMinSpread(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md"
        />
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.data.map((signal: Signal) => (
            <div key={signal.id} className="bg-white rounded-lg shadow p-6 border border-gray-200">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`w-3 h-3 rounded-full ${
                        signal.dex_price < signal.mexc_price ? 'bg-red-500' : 'bg-green-500'
                      }`}
                    ></span>
                    <h3 className="text-xl font-bold text-gray-900">{signal.coin_name}</h3>
                  </div>
                  <span className="text-lg font-semibold text-primary-600">
                    Spread: {signal.spread_percent !== undefined && signal.spread_percent !== null 
                      ? Number(signal.spread_percent).toFixed(2)
                      : 'N/A'}%
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
                  <span className="text-gray-600">MEXC Price:</span>
                  <span className="font-medium">
                    {signal.mexc_price !== undefined && signal.mexc_price !== null 
                      ? `$${Number(signal.mexc_price).toFixed(8)}`
                      : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">DEX Price:</span>
                  <span className="font-medium">
                    {signal.dex_price !== undefined && signal.dex_price !== null 
                      ? `$${Number(signal.dex_price).toFixed(8)}`
                      : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Max Size:</span>
                  <span className="font-medium">
                    {signal.max_size_usd !== undefined && signal.max_size_usd !== null 
                      ? `$${Number(signal.max_size_usd).toFixed(2)}`
                      : 'N/A'}
                  </span>
                </div>
                {signal.token_contract && (
                  <div className="text-xs text-gray-500 break-all">
                    {signal.token_chain}: {signal.token_contract}
                  </div>
                )}
              </div>

              <div className="flex gap-2">
                {signal.mexc_url && (
                  <a
                    href={signal.mexc_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 text-center px-3 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 text-sm"
                  >
                    <ExternalLink className="w-4 h-4 inline mr-1" />
                    MEXC
                  </a>
                )}
                {signal.dexscreener_url && (
                  <a
                    href={signal.dexscreener_url}
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



