import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'HeyPico AI Maps',
  description: 'AI-powered location search with intelligent transport recommendations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-dark-bg text-text-primary min-h-screen">
        <header className="border-b border-dark-border bg-dark-surface/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <h1 className="text-xl font-semibold">HeyPico AI Maps</h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}
