import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../lib/api'
import { useWebSocket } from '../hooks/useWebSocket'
import { ExternalLink, Trash2 } from 'lucide-react'

interface Signal {
  id: number
  coin_name: string
  hourly_profit: number
  gate_rate?: number
  gate_url?: string
  binance_rate?: number
  binance_url?: string
  mexc_rate?: number
  mexc_url?: string
  ourbit_rate?: number
  ourbit_url?: string
  bitget_rate?: number
  bitget_url?: string
  bitget_position?: string
  bybit_rate?: number
  bybit_url?: string
  bybit_position?: string
  created_at: string
}

export default function FundingRate() {
  const [minProfit, setMinProfit] = useState('')
  const [search, setSearch] = useState('')
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['funding-rate', minProfit, search],
    queryFn: async () => {
      const params = new URLSearchParams({ limit: '30', offset: '0' })
      if (minProfit) params.append('min_profit', minProfit)
      if (search) params.append('search', search)
      const response = await api.get(`/api/v1/signals/funding-rate?${params}`)
      return response.data
    },
  })

  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/api/v1/signals/${id}?signal_type=funding_rate`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['funding-rate'] })
    },
  })

  useWebSocket((message) => {
    if (message.type === 'new_signal' && message.signal_type === 'funding_rate') {
      queryClient.invalidateQueries({ queryKey: ['funding-rate'] })
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Funding Rate Spread</h1>
        <p className="mt-2 text-sm text-gray-600">Funding rate differentials across exchanges</p>
      </div>

      <div className="mb-4 flex gap-4">
        <input
          type="number"
          placeholder="Min profit %"
          value={minProfit}
          onChange={(e) => setMinProfit(e.target.value)}
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
        <div className="space-y-4">
          {data.data.map((signal: Signal) => (
            <div key={signal.id} className="bg-white rounded-lg shadow p-6 border border-gray-200">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{signal.coin_name}</h3>
                  <span className="text-lg font-semibold text-green-600">
                    Profit: {signal.hourly_profit}%
                  </span>
                </div>
                <button
                  onClick={() => deleteMutation.mutate(signal.id)}
                  className="text-red-600 hover:text-red-800"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {signal.gate_rate !== undefined && (
                  <div className="border rounded p-2">
                    <div className="font-medium">GATE</div>
                    <div className={signal.gate_rate >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {signal.gate_rate}%
                    </div>
                    {signal.gate_url && (
                      <a
                        href={signal.gate_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-primary-600 hover:underline"
                      >
                        <ExternalLink className="w-3 h-3 inline" /> Open
                      </a>
                    )}
                  </div>
                )}
                {signal.binance_rate !== undefined && (
                  <div className="border rounded p-2">
                    <div className="font-medium">BINANCE</div>
                    <div className={signal.binance_rate >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {signal.binance_rate}%
                    </div>
                    {signal.binance_url && (
                      <a
                        href={signal.binance_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-primary-600 hover:underline"
                      >
                        <ExternalLink className="w-3 h-3 inline" /> Open
                      </a>
                    )}
                  </div>
                )}
                {signal.mexc_rate !== undefined && (
                  <div className="border rounded p-2">
                    <div className="font-medium">MEXC</div>
                    <div className={signal.mexc_rate >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {signal.mexc_rate}%
                    </div>
                    {signal.mexc_url && (
                      <a
                        href={signal.mexc_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-primary-600 hover:underline"
                      >
                        <ExternalLink className="w-3 h-3 inline" /> Open
                      </a>
                    )}
                  </div>
                )}
                {signal.bybit_rate !== undefined && (
                  <div className="border rounded p-2">
                    <div className="font-medium">BYBIT</div>
                    <div className={signal.bybit_rate >= 0 ? 'text-green-600' : 'text-red-600'}>
                      {signal.bybit_rate}%
                    </div>
                    {signal.bybit_position && (
                      <div className="text-xs text-gray-500">{signal.bybit_position}</div>
                    )}
                    {signal.bybit_url && (
                      <a
                        href={signal.bybit_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-primary-600 hover:underline"
                      >
                        <ExternalLink className="w-3 h-3 inline" /> Open
                      </a>
                    )}
                  </div>
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



