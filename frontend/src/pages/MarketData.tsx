import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../lib/api'
import { ArrowUp, ArrowDown } from 'lucide-react'

interface Cryptocurrency {
  id: number
  name: string
  symbol: string
  rank: number
  price_usd: string
  change_24h: number
  change_7d: number
  market_cap_usd: string
  volume_24h_usd: string
  market_cap_dominance: number
}

export default function MarketData() {
  const [page, setPage] = useState(0)
  const [sort, setSort] = useState('rank')
  const [order, setOrder] = useState<'asc' | 'desc'>('asc')
  const [search, setSearch] = useState('')
  const limit = 50

  const { data, isLoading, error } = useQuery({
    queryKey: ['cryptocurrencies', page, sort, order, search],
    queryFn: async () => {
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: (page * limit).toString(),
        sort,
        order,
      })
      if (search) params.append('search', search)
      const response = await api.get(`/api/v1/market/cryptocurrencies?${params}`)
      return response.data
    },
  })

  const handleSort = (column: string) => {
    if (sort === column) {
      setOrder(order === 'asc' ? 'desc' : 'asc')
    } else {
      setSort(column)
      setOrder('asc')
    }
  }

  const formatNumber = (num: string | number) => {
    const n = typeof num === 'string' ? parseFloat(num) : num
    if (n >= 1e9) return `$${(n / 1e9).toFixed(2)}B`
    if (n >= 1e6) return `$${(n / 1e6).toFixed(2)}M`
    if (n >= 1e3) return `$${(n / 1e3).toFixed(2)}K`
    return `$${n.toFixed(2)}`
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Market Data</h1>
        <p className="mt-2 text-sm text-gray-600">Real-time cryptocurrency prices and market data</p>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Search by name or symbol..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
        />
      </div>

      {isLoading && <div className="text-center py-8">Loading...</div>}
      {error && <div className="text-center py-8 text-red-600">Error loading data</div>}

      {data && (
        <>
          <div className="overflow-x-auto bg-white shadow-sm rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => handleSort('rank')}
                  >
                    Rank {sort === 'rank' && (order === 'asc' ? '↑' : '↓')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Symbol
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => handleSort('price_usd')}
                  >
                    Price {sort === 'price_usd' && (order === 'asc' ? '↑' : '↓')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => handleSort('change_24h')}
                  >
                    24h {sort === 'change_24h' && (order === 'asc' ? '↑' : '↓')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => handleSort('market_cap_usd')}
                  >
                    Market Cap {sort === 'market_cap_usd' && (order === 'asc' ? '↑' : '↓')}
                  </th>
                  <th
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => handleSort('volume_24h_usd')}
                  >
                    Volume 24h {sort === 'volume_24h_usd' && (order === 'asc' ? '↑' : '↓')}
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.data.map((crypto: Cryptocurrency) => (
                  <tr key={crypto.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {crypto.rank}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {crypto.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {crypto.symbol}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${parseFloat(crypto.price_usd).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`inline-flex items-center ${
                          crypto.change_24h >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}
                      >
                        {crypto.change_24h >= 0 ? (
                          <ArrowUp className="w-4 h-4 mr-1" />
                        ) : (
                          <ArrowDown className="w-4 h-4 mr-1" />
                        )}
                        {Math.abs(crypto.change_24h).toFixed(2)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatNumber(crypto.market_cap_usd)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(crypto.volume_24h_usd)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-4 flex items-center justify-between">
            <button
              onClick={() => setPage(Math.max(0, page - 1))}
              disabled={page === 0}
              className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50"
            >
              Previous
            </button>
            <span className="text-sm text-gray-700">
              Page {page + 1} of {Math.ceil(data.pagination.total / limit)}
            </span>
            <button
              onClick={() => setPage(page + 1)}
              disabled={(page + 1) * limit >= data.pagination.total}
              className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  )
}



