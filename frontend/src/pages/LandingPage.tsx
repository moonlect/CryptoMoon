import { Link } from 'react-router-dom'
import { TrendingUp, BarChart3, Bell, Zap, Check } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export default function LandingPage() {
  const { isAuthenticated } = useAuth()

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-primary-600 to-primary-700 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 bg-transparent sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
                  <span className="block xl:inline">CryptoTracker</span>{' '}
                  <span className="block text-primary-200 xl:inline">Crypto Analytics Platform</span>
                </h1>
                <p className="mt-3 text-base text-primary-100 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Real-time cryptocurrency analysis, exchange spread tracking, and trading signals.
                  Get instant notifications about the best arbitrage opportunities.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  {!isAuthenticated ? (
                    <>
                      <div className="rounded-md shadow">
                        <Link
                          to="/register"
                          className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50 md:py-4 md:text-lg md:px-10"
                        >
                          Get started
                        </Link>
                      </div>
                      <div className="mt-3 sm:mt-0 sm:ml-3">
                        <Link
                          to="/login"
                          className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-800 hover:bg-primary-700 md:py-4 md:text-lg md:px-10"
                        >
                          Log in
                        </Link>
                      </div>
                    </>
                  ) : (
                    <div className="rounded-md shadow">
                      <Link
                        to="/market"
                        className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50 md:py-4 md:text-lg md:px-10"
                      >
                        View Market Data
                      </Link>
                    </div>
                  )}
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-primary-600 font-semibold tracking-wide uppercase">Features</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need for crypto trading
            </p>
          </div>

          <div className="mt-10">
            <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <TrendingUp className="h-6 w-6" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Market Data</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Real-time cryptocurrency prices and market data from CoinMarketCap API
                </p>
              </div>

              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <BarChart3 className="h-6 w-6" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Exchange Spreads</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Track price differences between MEXC Spot & Futures, Funding Rate spreads, and DEX prices
                </p>
              </div>

              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <Bell className="h-6 w-6" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Real-time Notifications</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Get instant browser, sound, and email notifications for new trading opportunities
                </p>
              </div>

              <div className="relative">
                <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <Zap className="h-6 w-6" />
                </div>
                <p className="ml-16 text-lg leading-6 font-medium text-gray-900">WebSocket Updates</p>
                <p className="mt-2 ml-16 text-base text-gray-500">
                  Real-time signal updates via WebSocket for VIP subscribers
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing Section */}
      <div className="bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-primary-600 font-semibold tracking-wide uppercase">Pricing</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Choose your plan
            </p>
          </div>

          <div className="mt-10 grid grid-cols-1 gap-8 lg:grid-cols-2 lg:max-w-4xl lg:mx-auto">
            {/* Free Plan */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
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
            </div>

            {/* VIP Plan */}
            <div className="bg-primary-600 rounded-lg shadow-lg border-2 border-primary-700 p-8 relative">
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
              <Link
                to="/pricing"
                className="mt-8 block w-full bg-white text-primary-600 text-center font-semibold py-3 rounded-md hover:bg-primary-50"
              >
                Upgrade Now
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}



