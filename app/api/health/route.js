export async function GET() {
  return Response.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  })
}

export async function OPTIONS() {
  return new Response(null, { status: 200 })
}