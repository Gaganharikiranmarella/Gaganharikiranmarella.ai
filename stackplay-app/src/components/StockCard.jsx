import React from 'react'

const StockCard = ({ stock, onSimulate, onAdd }) => {
  return (
    <div className="bg-white rounded-xl shadow-md w-60 p-4 shrink-0">
      <img src={stock.img} alt={stock.name} className="h-16 mx-auto mb-2" />
      <h3 className="text-lg font-bold">{stock.name}</h3>
      <p className="text-sm text-gray-600">{stock.reason}</p>
      <p className="mt-2 text-green-600 font-semibold">{stock.change}</p>
      <div className="flex justify-between mt-4">
        <button onClick={() => onSimulate(stock)} className="bg-blue-500 text-white px-2 py-1 rounded">Simulate</button>
        <button onClick={() => onAdd(stock)} className="bg-green-500 text-white px-2 py-1 rounded">Add</button>
      </div>
    </div>
  )
}

export default StockCard
