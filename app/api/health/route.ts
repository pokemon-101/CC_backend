import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    service: 'ChordCircle API'
  })
}

export async function OPTIONS() {
  return new NextResponse(null, { status: 200 })
}