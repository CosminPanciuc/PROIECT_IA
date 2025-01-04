import { useCallback, useEffect, useMemo, useState } from "react";

import Fuse from "fuse.js";
import { useDebouncedValue } from "./useDebounce";

interface ApiResponseItem {
  symbol: string;
  description: string;
}

interface SearchResult {
  symbol: string;
  name: string;
}

const DEBOUNCE_DELAY = 300;
const MIN_QUERY_LENGTH = 2;
const FUSE_OPTIONS = {
  keys: ["symbol", "name"],
  threshold: 0.3,
  cache: true,
};

const API_KEY = "ctslf2pr01qin3c02ip0ctslf2pr01qin3c02ipg";
const BASE_URL = "https://finnhub.io/api/v1/stock/symbol";

export function useStockSearch() {
  const [allStocks, setAllStocks] = useState<SearchResult[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fuse = useMemo(() => new Fuse(allStocks, FUSE_OPTIONS), [allStocks]);

  const fetchAllStocks = useCallback(async () => {
    try {
      const controller = new AbortController();
      const signal = controller.signal;

      setLoading(true);
      setError(null);

      const response = await fetch(
        `${BASE_URL}?exchange=US&token=${API_KEY}`,
        { signal }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      const stockData = result.map((item: ApiResponseItem) => ({
        symbol: item.symbol,
        name: item.description,
      }));

      setAllStocks(stockData);
      return () => controller.abort();
    } catch (err) {
      if (err instanceof Error) {
        if (err.name !== "AbortError") {
          setError(`Error fetching stock: ${err.message}`);
        }
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const [query, setQuery] = useState(""); 
  const debouncedQuery = useDebouncedValue(query, DEBOUNCE_DELAY); 

  useEffect(() => {
    if (debouncedQuery.trim().length < MIN_QUERY_LENGTH) {
      setSearchResults([]);
      return;
    }

    const results = fuse.search(debouncedQuery, { limit: 50 }).map((result) => result.item);
    setSearchResults(results);
  }, [debouncedQuery, fuse]);

  useEffect(() => {
    const cleanup = fetchAllStocks();
    return () => {
      cleanup?.then((abort) => abort?.());
    };
  }, [fetchAllStocks]);

  return {
    allStocks,
    searchResults,
    loading,
    error,
    setSearchQuery: setQuery,
    refreshStocks: fetchAllStocks,
  };
}
