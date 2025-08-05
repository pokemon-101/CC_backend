export async function GET() {
  return Response.json({
    status: 'healthy',
    api_version: 'v1',
    timestamp: new Date().toISOString(),
    message: 'ChordCircle API is running'
  })
}

export async function OPTIONS() {
  return new Response(null, { status: 200 })
}