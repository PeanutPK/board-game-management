import { computed, ref } from 'vue'
import type { PaginatedGamesResponse } from '@/api/games'
import { getGames } from '@/api/games'

interface UsePaginatedGamesOptions {
  storageKey?: string
  defaultPageSize?: number
  defaultSort?: 'title' | 'rating' | 'price_asc' | 'price_desc' | 'stock'
  onFetchError?: (error: unknown) => void
}

export function usePaginatedGames(options: UsePaginatedGamesOptions = {}) {
  const storageKey = options.storageKey ?? 'game-list-page-size'
  const defaultPageSize = options.defaultPageSize ?? 12
  const defaultSort = options.defaultSort ?? 'title'

  // State
  const currentPage = ref(1)
  const pageSize = ref<number | null>(null)
  const totalGames = ref(0)
  const totalPages = ref(1)
  const searchQuery = ref('')
  const sortBy = ref<'title' | 'rating' | 'price_asc' | 'price_desc' | 'stock'>(defaultSort)
  const loading = ref(false)

  // Computed
  const isReady = computed(() => pageSize.value !== null)
  const resolvedPageSize = computed(() => pageSize.value ?? defaultPageSize)

  // Helpers
  function readStoredPageSize(defaultValue: number): number {
    const storedValue = window.localStorage.getItem(storageKey)
    const parsedValue = storedValue ? Number(storedValue) : Number.NaN

    return Number.isFinite(parsedValue) && parsedValue > 0 ? Math.floor(parsedValue) : defaultValue
  }

  function initPageSize(): void {
    pageSize.value = readStoredPageSize(defaultPageSize)
  }

  function resetToFirstPage(): void {
    currentPage.value = 1
  }

  function goToPage(page: number): void {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  function handlePageSizeChange(value: number): void {
    pageSize.value = value
    window.localStorage.setItem(storageKey, String(value))
    resetToFirstPage()
  }

  function handleSearchChange(value: string): void {
    searchQuery.value = value
    resetToFirstPage()
  }

  function handleSortChange(
    value: 'title' | 'rating' | 'price_asc' | 'price_desc' | 'stock',
  ): void {
    sortBy.value = value
    resetToFirstPage()
  }

  async function fetchGames(): Promise<PaginatedGamesResponse | null> {
    if (pageSize.value === null) {
      return null
    }

    loading.value = true
    try {
      const skip = (currentPage.value - 1) * resolvedPageSize.value
      const response = await getGames(
        skip,
        resolvedPageSize.value,
        false,
        searchQuery.value,
        -1,
        -1,
        sortBy.value,
      )

      totalGames.value = response.total
      totalPages.value = response.total_pages
      currentPage.value = response.page

      return response
    } catch (error) {
      console.error('Failed to fetch games:', error)
      if (options.onFetchError) {
        options.onFetchError(error)
      }
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    currentPage,
    pageSize,
    totalGames,
    totalPages,
    searchQuery,
    sortBy,
    loading,

    // Computed
    isReady,
    resolvedPageSize,

    // Methods
    initPageSize,
    resetToFirstPage,
    goToPage,
    handlePageSizeChange,
    handleSearchChange,
    handleSortChange,
    fetchGames,
  }
}
