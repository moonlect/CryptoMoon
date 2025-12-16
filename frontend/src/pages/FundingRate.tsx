import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../lib/api'
import { useWebSocket } from '../hooks/useWebSocket'
import { ExternalLink, Trash2 } from 'lucide-react'

interface Signal {
  id: number
  coin_name: string
  hourly_profit: number | string
  gate_rate?: number | string
  gate_url?: string
  gate_interval?: string
  gate_position?: string
  binance_rate?: number | string
  binance_url?: string
  binance_interval?: string
  binance_position?: string
  mexc_rate?: number | string
  mexc_url?: string
  mexc_interval?: string
  mexc_position?: string
  ourbit_rate?: number | string
  ourbit_url?: string
  ourbit_interval?: string
  ourbit_position?: string
  bitget_rate?: number | string
  bitget_url?: string
  bitget_interval?: string
  bitget_position?: string
  bybit_rate?: number | string
  bybit_url?: string
  bybit_interval?: string
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

  const renderExchange = (
    name: string,
    rate: number | string | undefined | null,
    url: string | undefined,
    interval: string | undefined,
    position: string | undefined
  ) => {
    // Convert rate to number if it's a string
    const rateNum = rate !== undefined && rate !== null ? Number(rate) : null
    if (rateNum === null || isNaN(rateNum)) return null

    return (
      <div className="border rounded p-2">
        <div className="font-medium">{name}</div>
        <div className={rateNum >= 0 ? 'text-green-600' : 'text-red-600'}>
          {rateNum.toFixed(4)}%
        </div>
        {interval && (
          <div className="text-xs text-gray-500">Interval: {interval}</div>
        )}
        {position && (
          <div className="text-xs font-semibold text-blue-600">{position}</div>
        )}
        {url && (
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-primary-600 hover:underline mt-1 inline-block"
          >
            <ExternalLink className="w-3 h-3 inline" /> Open Futures
          </a>
        )}
      </div>
    )
  }

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
                    Profit: {signal.hourly_profit !== undefined && signal.hourly_profit !== null 
                      ? Number(signal.hourly_profit).toFixed(4) 
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

              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {renderExchange('GATE', signal.gate_rate, signal.gate_url, signal.gate_interval, signal.gate_position)}
                {renderExchange('BINANCE', signal.binance_rate, signal.binance_url, signal.binance_interval, signal.binance_position)}
                {renderExchange('MEXC', signal.mexc_rate, signal.mexc_url, signal.mexc_interval, signal.mexc_position)}
                {renderExchange('OURBIT', signal.ourbit_rate, signal.ourbit_url, signal.ourbit_interval, signal.ourbit_position)}
                {renderExchange('BITGET', signal.bitget_rate, signal.bitget_url, signal.bitget_interval, signal.bitget_position)}
                {renderExchange('BYBIT', signal.bybit_rate, signal.bybit_url, signal.bybit_interval, signal.bybit_position)}
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



