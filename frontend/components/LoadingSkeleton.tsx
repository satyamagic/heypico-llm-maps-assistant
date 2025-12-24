'use client'

export default function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="bg-dark-surface border border-dark-border rounded-xl p-6">
        <div className="h-6 bg-dark-border rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-dark-border rounded w-1/2"></div>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-dark-surface border border-dark-border rounded-xl p-6">
            <div className="h-5 bg-dark-border rounded w-2/3 mb-3"></div>
            <div className="h-4 bg-dark-border rounded w-full mb-2"></div>
            <div className="h-4 bg-dark-border rounded w-4/5 mb-4"></div>
            <div className="h-10 bg-dark-border rounded w-full"></div>
          </div>
        ))}
      </div>
    </div>
  )
}
