import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/contexts/AuthContext'
import { AccountProvider } from '@/contexts/AccountContext'
import { Toaster } from '@/components/ui/Toaster'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ChordCircle - Connect Your Music',
  description: 'Seamlessly sync and share your music across Spotify and Apple Music',
  keywords: ['music', 'spotify', 'apple music', 'playlist', 'sync'],
  authors: [{ name: 'ChordCircle Team' }],
  openGraph: {
    title: 'ChordCircle - Connect Your Music',
    description: 'Seamlessly sync and share your music across Spotify and Apple Music',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ChordCircle - Connect Your Music',
    description: 'Seamlessly sync and share your music across Spotify and Apple Music',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased`}>
        <AuthProvider>
          <AccountProvider>
            {children}
            <Toaster />
          </AccountProvider>
        </AuthProvider>
      </body>
    </html>
  )
}