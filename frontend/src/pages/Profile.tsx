import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import api from '../lib/api'
import { useAuth } from '../contexts/AuthContext'

export default function Profile() {
  const { user } = useAuth()
  const queryClient = useQueryClient()

  const { data: preferences, isLoading: prefsLoading } = useQuery({
    queryKey: ['preferences'],
    queryFn: async () => {
      const response = await api.get('/api/v1/users/me/preferences')
      return response.data
    },
  })

  const { data: subscription } = useQuery({
    queryKey: ['subscription'],
    queryFn: async () => {
      const response = await api.get('/api/v1/users/me/subscription')
      return response.data
    },
  })

  const updatePreferences = useMutation({
    mutationFn: async (data: any) => {
      await api.put('/api/v1/users/me/preferences', data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['preferences'] })
    },
  })

  const updateSubscription = useMutation({
    mutationFn: async (plan: string) => {
      await api.put('/api/v1/users/me/subscription', { plan })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscription'] })
      window.location.reload()
    },
  })

  const [localPrefs, setLocalPrefs] = useState(preferences)

  if (prefsLoading) return <div className="text-center py-8">Loading...</div>

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Profile Settings</h1>

      {/* User Info */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Account Information</h2>
        <div className="space-y-2">
          <div>
            <span className="text-gray-600">Email:</span>
            <span className="ml-2 font-medium">{user?.email}</span>
          </div>
          <div>
            <span className="text-gray-600">Plan:</span>
            <span className="ml-2 font-medium">{subscription?.plan || 'free'}</span>
          </div>
          <div>
            <span className="text-gray-600">Member since:</span>
            <span className="ml-2 font-medium">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
            </span>
          </div>
        </div>
      </div>

      {/* Subscription */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Subscription</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-600">Current Plan: {subscription?.plan || 'free'}</p>
            {subscription?.plan === 'free' && (
              <button
                onClick={() => updateSubscription.mutate('vip')}
                className="mt-2 px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
              >
                Upgrade to VIP
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Notifications Settings */}
      {preferences && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Notification Preferences</h2>
          <div className="space-y-6">
            {/* MEXC Spot & Futures */}
            <div className="border-b pb-4">
              <h3 className="font-medium mb-3">MEXC Spot & Futures</h3>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.mexc_spot_futures_enabled}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        mexc_spot_futures_enabled: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Enable notifications
                </label>
                <input
                  type="number"
                  placeholder="Min spread %"
                  value={preferences.mexc_spot_futures_min_spread}
                  onChange={(e) =>
                    updatePreferences.mutate({
                      mexc_spot_futures_min_spread: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border rounded"
                />
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.mexc_spot_futures_sound}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        mexc_spot_futures_sound: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Sound notification
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.mexc_spot_futures_browser_notif}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        mexc_spot_futures_browser_notif: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Browser notification
                </label>
              </div>
            </div>

            {/* Funding Rate */}
            <div className="border-b pb-4">
              <h3 className="font-medium mb-3">Funding Rate Spread</h3>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.funding_rate_enabled}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        funding_rate_enabled: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Enable notifications
                </label>
                <input
                  type="number"
                  placeholder="Min profit %"
                  value={preferences.funding_rate_min_profit}
                  onChange={(e) =>
                    updatePreferences.mutate({
                      funding_rate_min_profit: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border rounded"
                />
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.funding_rate_sound}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        funding_rate_sound: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Sound notification
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.funding_rate_browser_notif}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        funding_rate_browser_notif: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Browser notification
                </label>
              </div>
            </div>

            {/* MEXC & DEX */}
            <div className="pb-4">
              <h3 className="font-medium mb-3">MEXC & DEX Price Spread</h3>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.mexc_dex_enabled}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        mexc_dex_enabled: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Enable notifications
                </label>
                <input
                  type="number"
                  placeholder="Min spread %"
                  value={preferences.mexc_dex_min_spread}
                  onChange={(e) =>
                    updatePreferences.mutate({
                      mexc_dex_min_spread: e.target.value,
                    })
                  }
                  className="w-full px-3 py-2 border rounded"
                />
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.mexc_dex_sound}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        mexc_dex_sound: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Sound notification
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.mexc_dex_browser_notif}
                    onChange={(e) =>
                      updatePreferences.mutate({
                        mexc_dex_browser_notif: e.target.checked,
                      })
                    }
                    className="mr-2"
                  />
                  Browser notification
                </label>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

