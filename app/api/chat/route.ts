import { NextResponse } from 'next/server';

// Define the expected shape of the incoming request body
interface RequestBody {
  message: string;
}

export async function POST(request: Request) {
  try {
    // Parse the JSON body
    const body: RequestBody = await request.json();
    const { message } = body;

    // --- YOUR LOGIC GOES HERE ---
    // Example: Call OpenAI, query database, etc.
    // For now, we just echo the message back to prove it works.
    
    const botReply = `Brahma System received: "${message}"`;
    
    // ----------------------------

    return NextResponse.json({ reply: botReply });

  } catch (error) {
    console.error("API Error:", error);
    return NextResponse.json(
      { reply: "Error: System Malfunction." }, 
      { status: 500 }
    );
  }
}