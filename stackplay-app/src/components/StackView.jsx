import React from 'react'

const StackView = ({ stack }) => {
  return (
    <div className="mt-2 grid grid-cols-2 gap-4">
      {stack.map(stock => (
        <div key={stock.id} className="bg-white p-4 rounded-lg shadow">
          <img src={stock.img} alt={stock.name} className="h-10 mx-auto" />
          <h4 className="text-md font-semibold text-center mt-2">{stock.name}</h4>
          <p className="text-green-500 text-sm text-center">{stock.change}</p>
        </div>
      ))}
    </div>
  )
}

export default StackView
