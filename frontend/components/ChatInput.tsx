'use client'

import { useState } from 'react'

interface ChatInputProps {
  onSubmit: (query: string) => void
  isLoading: boolean
}

export default function ChatInput({ onSubmit, isLoading }: ChatInputProps) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim() && !isLoading) {
      onSubmit(query)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Where can I eat ramen near Blok M?"
          disabled={isLoading}
          className="w-full px-6 py-4 bg-dark-surface border border-dark-border rounded-xl 
                   text-text-primary placeholder-text-muted
                   focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent
                   transition-all duration-200
                   disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={!query.trim() || isLoading}
          className="absolute right-2 top-1/2 -translate-y-1/2
                   px-6 py-2 bg-accent text-white rounded-lg
                   hover:bg-blue-600 active:bg-blue-700
                   disabled:opacity-50 disabled:cursor-not-allowed
                   transition-colors duration-200
                   font-medium"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </form>
  )
}
