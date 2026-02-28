// app/api/footer/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getDb } from "../../(presentation-generator)/services/db";

// GET handler to retrieve properties
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get("userId");

    if (!userId) {
      return NextResponse.json(
        { error: "User ID is required" },
        { status: 400 }
      );
    }

    const db = await getDb();
    const result = await db.get(
      "SELECT data FROM settings WHERE key = 'footer' AND userId = ?",
      userId
    );
    await db.close();

    if (result) {
      return NextResponse.json({ properties: JSON.parse(result.data) });
    }

    return NextResponse.json({ properties: null });
  } catch (error) {
    console.error("Error retrieving footer properties:", error);
    return NextResponse.json(
      { error: "Failed to retrieve footer properties" },
      { status: 500 }
    );
  }
}

// POST handler to save properties
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, properties } = body;

    if (!userId || !properties) {
      return NextResponse.json(
        { error: "User ID and properties are required" },
        { status: 400 }
      );
    }

    const db = await getDb();
    const propertiesJson = JSON.stringify(properties);

    await db.run(
      `INSERT OR REPLACE INTO settings (key, userId, data, updated_at) 
       VALUES ('footer', ?, ?, CURRENT_TIMESTAMP)`,
      [userId, propertiesJson]
    );

    await db.close();

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Error saving footer properties:", error);
    return NextResponse.json(
      { error: "Failed to save footer properties" },
      { status: 500 }
    );
  }
}
