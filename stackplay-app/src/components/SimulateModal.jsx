import React from 'react'

const SimulateModal = ({ stock, onClose }) => {
  const growth = (stock.price * 1.03).toFixed(2)

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-10">
      <div className="bg-white p-6 rounded-xl w-80 text-center">
        <h2 className="text-xl font-bold mb-2">📊 Simulate {stock.name}</h2>
        <p>If you invested ₹500 last month...</p>
        <p className="mt-2 text-green-600 text-lg font-bold">You’d have ₹{growth} today!</p>
        <button onClick={onClose} className="mt-4 bg-red-500 text-white px-4 py-2 rounded">Close</button>
      </div>
    </div>
  )
}

export default SimulateModal
