import React, { useState } from 'react'
import StockCard from './components/StockCard'
import SimulateModal from './components/SimulateModal'
import StackView from './components/StackView'

const stockData = [
  {
    id: 1,
    name: 'Tesla',
    price: 755.20,
    change: '+2.34%',
    reason: 'EV demand surging',
    img: 'https://logo.clearbit.com/tesla.com',
  },
  {
    id: 2,
    name: 'Nike',
    price: 115.20,
    change: '+1.14%',
    reason: 'Gen Z fav + sales up',
    img: 'https://logo.clearbit.com/nike.com',
  },
  {
    id: 3,
    name: 'Apple',
    price: 190.30,
    change: '+0.85%',
    reason: 'iPhone sales stable',
    img: 'https://logo.clearbit.com/apple.com',
  },
  {
    id: 4,
    name: 'Amazon',
    price: 132.55,
    change: '+1.75%',
    reason: 'Prime Day success',
    img: 'https://logo.clearbit.com/amazon.com',
  },
  {
    id: 5,
    name: 'Netflix',
    price: 428.10,
    change: '+3.22%',
    reason: 'New shows trending',
    img: 'https://logo.clearbit.com/netflix.com',
  },
  {
    id: 6,
    name: 'Spotify',
    price: 172.40,
    change: '-0.24%',
    reason: 'Slight user drop',
    img: 'https://logo.clearbit.com/spotify.com',
  },
  {
    id: 7,
    name: 'Adobe',
    price: 519.75,
    change: '+0.98%',
    reason: 'AI tools released',
    img: 'https://logo.clearbit.com/adobe.com',
  },
  {
    id: 8,
    name: 'Google',
    price: 2820.99,
    change: '+2.67%',
    reason: 'Search ads booming',
    img: 'https://logo.clearbit.com/google.com',
  },
  {
    id: 9,
    name: 'Meta',
    price: 356.40,
    change: '+1.49%',
    reason: 'Threads growth strong',
    img: 'https://logo.clearbit.com/meta.com',
  },
  {
    id: 10,
    name: 'Microsoft',
    price: 341.75,
    change: '+0.89%',
    reason: 'Copilot launch success',
    img: 'https://logo.clearbit.com/microsoft.com',
  },
]

function App() {
  const [selectedStock, setSelectedStock] = useState(null)
  const [stack, setStack] = useState([])

  const simulate = (stock) => setSelectedStock(stock)
  const addToStack = (stock) => {
    if (!stack.find((s) => s.id === stock.id)) {
      setStack([...stack, stock])
    }
  }

  return (
    <div className="min-h-screen p-4 bg-gradient-to-br from-indigo-100 via-blue-50 to-white animate-gradient bg-[length:400%_400%]">
      <h1 className="text-xl font-bold mb-4 text-center">📈 StackPlay: Simulate Your Stock Moves</h1>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {stockData.map((stock) => (
          <StockCard key={stock.id} stock={stock} onSimulate={simulate} onAdd={addToStack} />
        ))}
      </div>

      <h2 className="text-lg mt-6 font-semibold">📦 My Stack</h2>
      <StackView stack={stack} />

      {selectedStock && <SimulateModal stock={selectedStock} onClose={() => setSelectedStock(null)} />}
    </div>
  )
}

export default App
