import { useCallback, useEffect, useState } from "react";

import { useStockSearch } from "./hooks/useStockSearch";

export default function App() {
  const { searchResults, loading, error, setSearchQuery, refreshStocks } = useStockSearch();
  const [query, setQuery] = useState("");
  const [selectedStocks, setSelectedStocks] = useState<{ symbol: string; name: string }[]>([]);

  const addStockToList = useCallback((stock: { symbol: string; name: string }) => {
    setSelectedStocks((prevStocks) => {
      if (!prevStocks.some((s) => s.symbol === stock.symbol)) {
        return [...prevStocks, stock];
      }
      return prevStocks;
    });
    setQuery("");
  }, []);

  const deleteStockFromList = useCallback((symbol: string) => {
    setSelectedStocks((prevStocks) =>
      prevStocks.filter((stock) => stock.symbol !== symbol)
    );
  }, []);

  useEffect(() => {
    setSearchQuery(query);
  }, [query, setSearchQuery]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-4">Stock Symbol Search</h1>

      <div className="relative w-64">
        <input
          type="text"
          placeholder="Search for a stock symbol..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="p-2 border border-gray-400 rounded-md text-black w-full"
        />

        {searchResults.length > 0 && (
          <ul className="absolute bg-white text-black w-full mt-1 rounded-md shadow-lg z-10 max-h-60 overflow-auto">
            {searchResults.map((result) => (
              <li
                key={result.symbol}
                className="p-2 hover:bg-gray-200 cursor-pointer"
                onClick={() => addStockToList(result)}
              >
                {result.symbol} - {result.name}
              </li>
            ))}
          </ul>
        )}
      </div>

      {loading && <p className="mt-4 text-yellow-400">Loading...</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}

      {selectedStocks.length > 0 && (
        <div className="mt-6 w-full max-w-2xl">
          <h2 className="text-xl font-semibold">Selected Stocks</h2>
          <ul className="mt-2 space-y-2">
            {selectedStocks.map((stock) => (
              <li
                key={stock.symbol}
                className="bg-gray-800 p-3 rounded-md flex justify-between"
              >
                <span className="font-mono">{stock.symbol}</span>
                <span className="font-bold">{stock.name}</span>
                <button
                  onClick={() => deleteStockFromList(stock.symbol)}
                  className="text-red-500 hover:text-red-700"
                >
                  ❌
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
      
    {/* Placeholder pentru trimis catre backend */}
      <button
        onClick={refreshStocks}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
      >
        Refresh Stocks
      </button>
    </div>
  );
}
