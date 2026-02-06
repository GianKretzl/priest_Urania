import { NextRequest, NextResponse } from 'next/server';

// Configuração de runtime para permitir mais tempo de execução
export const maxDuration = 300; // 5 minutos
export const dynamic = 'force-dynamic';

// Proxy para o backend
export async function GET(request: NextRequest) {
  const path = request.nextUrl.pathname.replace('/api/proxy', '');
  const searchParams = request.nextUrl.searchParams.toString();
  const url = `http://backend:8000/api/v1${path}${searchParams ? `?${searchParams}` : ''}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to fetch data' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  const path = request.nextUrl.pathname.replace('/api/proxy', '');
  const url = `http://backend:8000/api/v1${path}`;
  const body = await request.json();

  try {
    // Timeout maior para operações de geração de horário
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 290000); // 290 segundos (deixa margem para o maxDuration)

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error: any) {
    console.error('Proxy error:', error);
    if (error.name === 'AbortError') {
      return NextResponse.json({ error: 'Request timeout - operação demorou muito tempo' }, { status: 504 });
    }
    return NextResponse.json({ error: 'Failed to post data' }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  const path = request.nextUrl.pathname.replace('/api/proxy', '');
  const url = `http://backend:8000/api/v1${path}`;
  const body = await request.json();

  try {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to update data' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  const path = request.nextUrl.pathname.replace('/api/proxy', '');
  const url = `http://backend:8000/api/v1${path}`;

  try {
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 204) {
      return new NextResponse(null, { status: 204 });
    }

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Failed to delete data' }, { status: 500 });
  }
}
