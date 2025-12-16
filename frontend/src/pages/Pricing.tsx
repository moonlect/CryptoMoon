import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../lib/api'
import { Check } from 'lucide-react'

export default function Pricing() {
  const { isAuthenticated, isVIP } = useAuth()
  const navigate = useNavigate()

  const upgradeMutation = useMutation({
    mutationFn: async () => {
      await api.put('/api/v1/users/me/subscription', { plan: 'vip' })
    },
    onSuccess: () => {
      alert('VIP subscription activated!')
      window.location.reload()
    },
  })

  const handleUpgrade = () => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    if (confirm('Activate VIP subscription? (MVP: Instant activation)')) {
      upgradeMutation.mutate()
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900">Choose Your Plan</h1>
        <p className="mt-4 text-xl text-gray-600">Select the plan that works best for you</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        {/* Free Plan */}
        <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900">Free</h3>
          <p className="mt-4 text-4xl font-extrabold text-gray-900">$0</p>
          <p className="mt-2 text-base text-gray-500">per month</p>
          <ul className="mt-6 space-y-4">
            <li className="flex items-start">
              <Check className="flex-shrink-0 h-6 w-6 text-green-500" />
              <span className="ml-3 text-base text-gray-700">Market Data</span>
            </li>
            <li className="flex items-start">
              <Check className="flex-shrink-0 h-6 w-6 text-green-500" />
              <span className="ml-3 text-base text-gray-700">Basic Features</span>
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 h-6 w-6 text-gray-400">×</span>
              <span className="ml-3 text-base text-gray-500">Trading Signals</span>
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 h-6 w-6 text-gray-400">×</span>
              <span className="ml-3 text-base text-gray-500">Real-time Notifications</span>
            </li>
          </ul>
          {isVIP && (
            <div className="mt-8 text-center text-sm text-gray-500">Current Plan</div>
          )}
        </div>

        {/* VIP Plan */}
        <div className="bg-primary-600 rounded-lg shadow-xl border-2 border-primary-700 p-8 relative">
          <div className="absolute top-0 right-0 -mt-4 -mr-4">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-400 text-yellow-900">
              Popular
            </span>
          </div>
          <h3 className="text-2xl font-bold text-white">VIP</h3>
          <p className="mt-4 text-4xl font-extrabold text-white">$100</p>
          <p className="mt-2 text-base text-primary-100">per month</p>
          <ul className="mt-6 space-y-4">
            <li className="flex items-start">
              <Check className="flex-shrink-0 h-6 w-6 text-white" />
              <span className="ml-3 text-base text-white">Everything in Free</span>
            </li>
            <li className="flex items-start">
              <Check className="flex-shrink-0 h-6 w-6 text-white" />
              <span className="ml-3 text-base text-white">All Trading Signals</span>
            </li>
            <li className="flex items-start">
              <Check className="flex-shrink-0 h-6 w-6 text-white" />
              <span className="ml-3 text-base text-white">Real-time Notifications</span>
            </li>
            <li className="flex items-start">
              <Check className="flex-shrink-0 h-6 w-6 text-white" />
              <span className="ml-3 text-base text-white">WebSocket Updates</span>
            </li>
          </ul>
          {!isVIP ? (
            <button
              onClick={handleUpgrade}
              disabled={upgradeMutation.isPending}
              className="mt-8 w-full bg-white text-primary-600 font-semibold py-3 rounded-md hover:bg-primary-50 disabled:opacity-50"
            >
              {upgradeMutation.isPending ? 'Activating...' : 'Upgrade to VIP'}
            </button>
          ) : (
            <div className="mt-8 text-center text-sm text-primary-100">Current Plan</div>
          )}
        </div>
      </div>
    </div>
  )
}



