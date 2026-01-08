import { NextResponse } from 'next/server';

// Define the structure of the incoming request body
interface RequestBody {
  message: string;
}

export async function POST(request: Request) {
  try {
    const body: RequestBody = await request.json();
    const { message } = body;

    // --- LOGIC: Customize your bot's reply here ---
    const replyText = `Ashwamedha System received: "${message}"`;
    // ----------------------------------------------

    return NextResponse.json({ reply: replyText });

  } catch (error) {
    console.error("Ashwamedha API Error:", error);
    return NextResponse.json(
      { reply: "Signal Lost. System Offline." }, 
      { status: 500 }
    );
  }
}