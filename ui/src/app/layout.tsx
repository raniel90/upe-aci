import type { Metadata } from 'next'
import { DM_Mono, Geist } from 'next/font/google'
import { NuqsAdapter } from 'nuqs/adapters/next/app'
import { Toaster } from '@/components/ui/sonner'
import { pt_BR } from '@/lib/i18n'
import './globals.css'
const geistSans = Geist({
  variable: '--font-geist-sans',
  weight: '400',
  subsets: ['latin']
})

const dmMono = DM_Mono({
  subsets: ['latin'],
  variable: '--font-dm-mono',
  weight: '400'
})

export const metadata: Metadata = {
  title: pt_BR.metadata.title,
  description: pt_BR.metadata.description,
  icons: {
    icon: [
      {
        url: '/favicon.png',
        sizes: '32x32',
        type: 'image/png'
      },
      {
        url: '/favicon.ico',
        sizes: '16x16',
        type: 'image/x-icon'
      }
    ],
    shortcut: '/favicon.ico',
    apple: '/favicon.png'
  }
}

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-BR">
      <body className={`${geistSans.variable} ${dmMono.variable} antialiased`}>
        <NuqsAdapter>{children}</NuqsAdapter>
        <Toaster />
      </body>
    </html>
  )
}
